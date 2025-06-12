from django.contrib import admin
from polls.models import Option, Poll, Vote

admin.site.register([Poll, Option, Vote])
