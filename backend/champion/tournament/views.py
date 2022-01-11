from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
from django.http import HttpResponseNotFound


class EventSerializator(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ['pk', 'name', 'description', 'date_finish', 'date_begin', 'country', 'city', 'status', 'admin_id', 'system_id', 'sport_type_id']


class SubeventSerializator(serializers.ModelSerializer):
    class Meta:
        model = models.Subevent
        fields = ['pk', 'name', 'description', 'event_id']


class Sport_type_Serializator(serializers.ModelSerializer):
    class Meta:
        model = models.Sport_type
        fields = ['pk', 'name', 'description', 'count']


class ParticipantSerializator(serializers.ModelSerializer):
    class Meta:
        model = models.Participant
        fields = ['pk', 'name', 'country', 'city', 'progress', 'result', 'subevent_id']


class SportTypes(APIView):
    def get(self, *args, **kwargs):
        all_types = models.Sport_type.objects.all()
        serialized_types = Sport_type_Serializator(all_types, many=True)
        return Response(serialized_types.data)


class Events(APIView):
    def get(self, request, st, format=None):
        events = models.Event.objects.filter(sport_type_id=st)
        if not events:
            return HttpResponseNotFound()

        serialized_events = EventSerializator(events, many=True)
        return Response(serialized_events.data)


class Subevents(APIView):
    def get(self, request, ev, format=None):
        subevents = models.Subevent.objects.filter(event_id=ev)
        if not subevents:
            return HttpResponseNotFound
        ser_subevents = SubeventSerializator(subevents, many=True)
        return Response(ser_subevents.data)


class Participants(APIView):
    def get(self, request, sid, format=None):
        participants = models.Participant.objects.filter(subevent_id=sid)
        if not participants:
            return HttpResponseNotFound
        ser_participants = ParticipantSerializator(participants, many=True)
        return Response(ser_participants.data)


class CountSubevents(APIView):
    def get(self, request, evid, format=None):
        count = models.Subevent.objects.filter(event_id=evid).count()
        return Response({"message": f"{count}"})


class CountParticipants(APIView):
    def get(self, request, sid, format=None):
        count = models.Participant.objects.filter(subevent_id=sid).count()
        return Response({"message": f"{count}"})