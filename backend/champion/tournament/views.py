from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
from django.http import HttpResponseNotFound
from datetime import date


class EventSerializator(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ['pk', 'name', 'description', 'date_finish', 'date_begin', 'country', 'city', 'status', 'admin_id', 'system_id', 'sport_type_id']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.date_finish = validated_data.get('date_finish', instance.date_finish)
        instance.date_begin = validated_data.get('date_begin', instance.date_begin)
        instance.country = validated_data.get('country', instance.country)
        instance.city = validated_data.get('city', instance.city)
        instance.status = validated_data.get('status', instance.status)
        instance.admin_id = validated_data.get('admin_id', instance.admin_id)
        instance.system_id = validated_data.get('system_id', instance.system_id)
        instance.sport_type_id = validated_data.get('sport_type_id', instance.sport_type_id)
        instance.save()
        return instance

    def create(self, validated_data):
        instance = models.Event.objects.create(
            name=validated_data.get('name'),
            description=validated_data.get('description'),
            date_finish=validated_data.get('date_finish'),
            date_begin=validated_data.get('date_begin'),
            country=validated_data.get('country'),
            city=validated_data.get('city'),
            status=validated_data.get('status'),
            admin_id=validated_data.get('admin_id'),
            system_id=validated_data.get('system_id'),
            sport_type_id=validated_data.get('sport_type_id')
        )


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


class MatchSerializator(serializers.ModelSerializer):
    class Meta:
        model = models.Match
        fields = ['pk', 'number', 'date', 'subevent_id']


class SportTypes(APIView):
    def get(self, *args, **kwargs):
        all_types = models.Sport_type.objects.all()
        serialized_types = Sport_type_Serializator(all_types, many=True)
        return Response(serialized_types.data)


class FindSports(APIView):
    def get(self, request, name, format=None):
        st = models.Sport_type.objects.filter(name=name)
        if not st:
            return HttpResponseNotFound()
        serialized_types = Sport_type_Serializator(st, many=True)
        return Response(serialized_types.data)


class Events(APIView):
    def get(self, request, st, format=None):
        events = models.Event.objects.filter(sport_type_id=st)
        if not events:
            return HttpResponseNotFound()

        serialized_events = EventSerializator(events, many=True)
        return Response(serialized_events.data)


class Event(APIView):
    def get(self, request, pk, format=None):
        event = models.Event.objects.filter(pk=pk)
        if not event:
            return HttpResponseNotFound()

        serialized_events = EventSerializator(event, many=True)
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


class Participant(APIView):
    def get(self, request, pk, format=None):
        participant = models.Participant.objects.filter(pk=pk)
        if not participant:
            return HttpResponseNotFound

        ser_participant = ParticipantSerializator(participant, many=True)
        return Response(ser_participant.data)


class SportData(APIView):
    def get(self, request, pk):
        sport = models.Sport_type.objects.get(pk=pk)
        if not sport:
            return HttpResponseNotFound
        else:
            count_event = sport.count
            today_year = date.today().year
            count_events_in_year = []
            avg_count_participant_in_year = []
            for i in range(5):
                events = models.Event.objects.filter(sport_type_id=pk,
                                                     date_begin__gt=date(today_year - i, 1, 1),
                                                     date_begin__lt=date(today_year - i + 1, 1, 1)
                                                     )

                count_events_in_year.append(len(events))
                list_counts_participants_in_year = []
                for event in events:
                    subevents = models.Subevent.objects.filter(event_id=event.pk)
                    count = 0
                    for subevent in subevents:
                        count += models.Participant.objects.filter(subevent_id=subevent.id).count()
                    list_counts_participants_in_year.append(count)

                if (len(events) != 0):
                    avg_count_participant_in_year.append(
                        sum(list_counts_participants_in_year) / len(list_counts_participants_in_year)
                    )
                else:
                    avg_count_participant_in_year.append(
                        0.0
                    )


            events_cur_year = models.Event.objects.filter(sport_type_id=pk, date_begin__gt=date(today_year, 1, 1), date_begin__lt=date(today_year + 1, 1, 1))
            count_event_cur_year = len(events_cur_year)
            events_last_year = models.Event.objects.filter(sport_type_id=pk, date_begin__gt=date(today_year-1, 1, 1), date_begin__lt=date(today_year, 1, 1))
            count_event_last_year = len(events_last_year)
            list_counts_participants_cur_year = []
            for event in events_cur_year:
                subevents = models.Subevent.objects.filter(event_id=event.pk)
                count = 0
                for subevent in subevents:
                    count += models.Participant.objects.filter(subevent_id=subevent.id).count()
                list_counts_participants_cur_year.append(count)
            avg_count_participant_cur_year = sum(list_counts_participants_cur_year) / len(list_counts_participants_cur_year)
            list_counts_participants_last_year = []
            for event in events_last_year:
                subevents = models.Subevent.objects.filter(event_id=event.pk)
                count = 0
                for subevent in subevents:
                    count += models.Participant.objects.filter(subevent_id=subevent.id).count()
                list_counts_participants_last_year.append(count)
            avg_count_participant_last_year = sum(list_counts_participants_last_year) / len(list_counts_participants_last_year)
            return Response({
                "name": f"{sport.name}",
                "count_events": f"{count_event}",
                "count_events_cur_year": f"{count_event_cur_year}",
                "count_events_last_year": f"{count_event_last_year}",
                "avg_participants_cur_year": f"{avg_count_participant_cur_year}",
                "avg_participants_last_year": f"{avg_count_participant_last_year}",
                "count_events_in_year": count_events_in_year,
                "avg_count_participant_in_year": avg_count_participant_in_year
            })




class CountSubevents(APIView):
    def get(self, request, evid, format=None):
        count = models.Subevent.objects.filter(event_id=evid).count()
        return Response({"message": f"{count}"})


class CountParticipants(APIView):
    def get(self, request, evid, format=None):
        subevents = models.Subevent.objects.filter(event_id=evid)
        count = 0
        for subevent in subevents:
            count += models.Participant.objects.filter(subevent_id=subevent.id).count()
        return Response({"message": f"{count}"})


class Matches(APIView):
    def get(self, request, sid, format=None):
        matches = models.Match.objects.filter(subevent_id=sid)
        matches_lst = []
        for match in matches:
            links = models.Participant_Match.objects.filter(match_id=match.pk)
            data = {"pk": match.pk,
                    "number": match.number,
                    "date": match.date,
                    "first_participant": links[0].participant_id.name,
                    "second_participant": links[1].participant_id.name,
                    "score": f"{links[0].score}:{links[1].score}"
                    }
            matches_lst.append(data)
        return Response(matches_lst)


class Match(APIView):
    def get(self,request, pk, format=None):
        match = models.Match.objects.get(pk=pk)
        links = models.Participant_Match.objects.filter(match_id=match.pk)
        data = {"pk": match.pk,
                "number": match.number,
                "date": match.date,
                "first_participant": links[0].participant_id.name,
                "second_participant": links[1].participant_id.name,
                "score": f"{links[0].score}:{links[1].score}"
                }
        return Response(data)


class AvgCounts(APIView):
    def get(self, request, pk, format=None):
        event = models.Event.objects.get(pk=pk)
        subevents = models.Subevent.objects.filter(event_id=event.pk)
        count = []
        for subevent in subevents:
            count.append(models.Participant.objects.filter(subevent_id=subevent.id).count())
        avg = sum(count) / len(count)
        return Response({"avg_count": [f"{avg}", 0]})
