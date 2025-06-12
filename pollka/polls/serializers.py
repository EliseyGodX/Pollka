import uuid

from django.contrib.auth.models import User
from polls.models import Option, Poll, Vote
from rest_framework.serializers import (CharField, ModelSerializer, Serializer,
                                        ValidationError)


class OptionSerializer(ModelSerializer):

    class Meta:
        model = Option
        fields = ('text', )


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class CreatePollSerializer(ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Poll
        fields = (
            'name', 'description', 'is_anonymous', 'is_revotable',
            'expired_at', 'deleted_at', 'options'
        )

    def validate_options(self, value):
        if not value:
            raise ValidationError("At least one option is required.")
        return value

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        validated_data['owner'] = self.context['request'].user
        validated_data['id'] = uuid.uuid4()
        poll = super().create(validated_data)
        Option.objects.bulk_create([
            Option(poll=poll, **option) for option in options_data
        ])
        return poll

    def to_representation(self, instance):
        poll = super().to_representation(instance)
        poll['id'] = instance.id
        return poll


class RetrievePollSerializer(ModelSerializer):
    owner_username = CharField(source='owner.username', read_only=True)
    owner_first_name = CharField(source='owner.first_name', read_only=True)
    owner_last_name = CharField(source='owner.last_name', read_only=True)
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = (
            'id', 'name', 'description', 'is_anonymous', 'is_revotable',
            'created_at', 'expired_at', 'deleted_at', 'owner_username',
            'owner_first_name', 'owner_last_name', 'options'
        )


class CreateVoteSerializer(ModelSerializer):

    class Meta:
        model = Vote
        fields = ('option', )

    def create(self, validated_data):
        user = self.context['request'].user
        option = validated_data['option']
        poll = option.poll
        early_vote = Vote.objects.filter(option__poll=poll, user=user)

        if early_vote.exists():
            if not poll.is_revotable:
                raise ValidationError(
                    'It is not possible to change the vote in this poll'
                )
            early_vote.delete()

        validated_data['user'] = user
        return super().create(validated_data)


class DestroyVoteSerializer(ModelSerializer):

    class Meta:
        model = Vote
        fields = ('option',)


class RetrieveRespondentsPollSerializer(Serializer):
    respondents = UserSerializer(many=True, read_only=True)
