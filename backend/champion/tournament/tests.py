from django.test import TestCase
# Create your tests here.
from tournament.models import Match, Participant, Participant_Match

Match.objects.filter(date__year=2022)

from tournament.views import EventSerializator

Event.objects.filter(date_begin__year == 2021)
