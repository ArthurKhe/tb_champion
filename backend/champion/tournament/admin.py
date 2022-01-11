from django.contrib import admin
from . import models

class EventsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'description', 'country', 'city', 'status', 'date_finish', 'date_begin']
    list_editable = ['name', 'description', 'status', 'date_finish']


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'country', 'city', 'progress', 'result', 'subevent_id']
    list_editable = ['name', 'country', 'city', 'progress', 'result', 'subevent_id']


class SubeventAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'description', 'event_id']
    list_editable = ['name', 'description', 'event_id']


class Sport_typeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'description', 'count']
    list_editable = ['name', 'description', 'count']


class SystemAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'description']
    list_editable = ['name', 'description']


class MatchAdmin(admin.ModelAdmin):
    list_display = ['pk', 'number', 'date', 'subevent_id']
    list_editable = ['number', 'date', 'subevent_id']


class Participant_matchAdmin(admin.ModelAdmin):
    list_display = ['pk', 'participant_id', 'match_id', 'score']
    list_editable = ['participant_id', 'match_id', 'score']

# Register your models here.


admin.site.register(models.Event, EventsAdmin)
admin.site.register(models.Participant, ParticipantAdmin)
admin.site.register(models.Subevent, SubeventAdmin)
admin.site.register(models.Sport_type, Sport_typeAdmin)
admin.site.register(models.System, SystemAdmin)
admin.site.register(models.Match, MatchAdmin)
admin.site.register(models.Participant_Match, Participant_matchAdmin)


