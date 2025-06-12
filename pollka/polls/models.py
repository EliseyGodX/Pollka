from django.contrib.auth.models import User
from django.db.models import (CASCADE, AutoField, BooleanField, CharField,
                              DateTimeField, ForeignKey, Model)


class Poll(Model):
    id = CharField(max_length=36, primary_key=True)
    name = CharField(max_length=48)
    description = CharField(max_length=2048, null=True, blank=True)
    is_anonymous = BooleanField(default=False)
    is_revotable = BooleanField(default=True)
    owner = ForeignKey(
        'auth.User', null=True, on_delete=CASCADE, related_name='poll'
    )
    created_at = DateTimeField(auto_now_add=True)
    expired_at = DateTimeField(null=True, blank=True)
    deleted_at = DateTimeField(null=True, blank=True)

    @property
    def respondents(self):
        return User.objects.filter(vote__option__poll=self).distinct()


class Option(Model):
    id = AutoField(primary_key=True)
    text = CharField(max_length=200)
    poll = ForeignKey(
        'polls.Poll', on_delete=CASCADE, related_name='options'
    )


class Vote(Model):
    id = AutoField(primary_key=True)
    user = ForeignKey('auth.User', on_delete=CASCADE, related_name='vote')
    option = ForeignKey(
        'polls.Option', on_delete=CASCADE, related_name='vote'
    )
    voted_on = DateTimeField(auto_now_add=True)
