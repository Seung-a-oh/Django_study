from django.contrib import admin
from .models import Candidate, Choice, Poll
# Register your models here.

admin.site.register(Candidate)
admin.site.register(Poll)
admin.site.register(Choice)

