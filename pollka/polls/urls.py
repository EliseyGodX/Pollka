from django.urls import path
from polls.views import (CreatePollView, CreateVoteView, DestroyPollView,
                         RetrievePollView, DestroyVoteView, RetrieveRespondentsPollView)

app_name = 'polls'

urlpatterns = [
    path('create/', CreatePollView.as_view(), name='create'),
    path('delete/<str:pk>/', DestroyPollView.as_view(), name='delete'),
    path('<str:pk>/', RetrievePollView.as_view(), name='retrieve'),
    path('vote/create', CreateVoteView.as_view(), name='vote/create'),
    path('vote/delete', DestroyVoteView.as_view(), name='vote/delete'),
    path(
        'respondents/<str:pk>', RetrieveRespondentsPollView.as_view(),
        name='respondents'
    )
]
