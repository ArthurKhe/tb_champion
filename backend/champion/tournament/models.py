from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db.models import ForeignKey


class Sport_type(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    count = models.IntegerField()


class TB_user(models.Model):
    name = models.CharField(max_length=255)


class System(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    date_begin = models.DateField()
    date_finish = models.DateField()
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    admin_id: ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    system_id = models.ForeignKey(System, on_delete= models.CASCADE)
    sport_type_id = models.ForeignKey(Sport_type, on_delete= models.CASCADE)


class Subevent(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)


class Participant(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    progress = models.CharField(max_length=255)
    result = models.CharField(max_length=255)
    subevent_id = models.ForeignKey(Subevent, on_delete=models.CASCADE)



class Match(models.Model):
    date = models.DateField()
    score_one = models.IntegerField()
    score_two = models.IntegerField()
    subevent_id = models.ForeignKey(Subevent, on_delete=models.CASCADE)


class Participant_Match(models.Model):
    participant_id = models.ForeignKey(Participant, on_delete=models.CASCADE)
    match_id = models.ForeignKey(Match, on_delete=models.CASCADE)


class User_Event(models.Model):
        tb_user_id = models.ForeignKey(TB_user, on_delete=models.CASCADE)
        event_id = models.ForeignKey(Event, on_delete=models.CASCADE)