from typing import NoReturn

from django.shortcuts import get_object_or_404
from polls.models import Poll, Vote
from polls.serializers import (CreatePollSerializer, CreateVoteSerializer,
                               DestroyVoteSerializer, RetrievePollSerializer,
                               RetrieveRespondentsPollSerializer)
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     RetrieveAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


class CreatePollView(CreateAPIView):
    serializer_class = CreatePollSerializer
    permission_classes = [IsAuthenticated]


class RetrievePollView(RetrieveAPIView):
    serializer_class = RetrievePollSerializer
    queryset = Poll.objects.all()
    permission_classes = [AllowAny]


class DestroyPollView(DestroyAPIView):
    queryset = Poll.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != self.request.user:
            raise PermissionDenied()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateVoteView(CreateAPIView):
    serializer_class = CreateVoteSerializer
    queryset = Vote.objects.all()
    permission_classes = [IsAuthenticated]


class DestroyVoteView(DestroyAPIView):
    serializer_class = DestroyVoteSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs) -> NoReturn:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        option = serializer.validated_data['option']
        vote = get_object_or_404(Vote, option=option, user=request.user)

        if vote.user != self.request.user:
            raise PermissionDenied()

        poll = option.poll
        if not poll.is_revotable:
            raise ValidationError('It is not possible to change the vote in this poll')

        self.perform_destroy(vote)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RetrieveRespondentsPollView(RetrieveAPIView):
    serializer_class = RetrieveRespondentsPollSerializer
    permission_classes = [AllowAny]
    queryset = Poll.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_anonymous:
            raise ValidationError('This poll is anonymous')
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
