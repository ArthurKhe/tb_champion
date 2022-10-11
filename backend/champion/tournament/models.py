from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db.models import ForeignKey


class Sport_type(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class TB_user(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class System(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


class Subevent(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Participant(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    progress = models.CharField(max_length=255)
    result = models.CharField(max_length=255)
    subevent_id = models.ForeignKey(Subevent, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Match(models.Model):
    number = models.IntegerField(default=0)
    date = models.DateField()
    subevent_id = models.ForeignKey(Subevent, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)


class Participant_Match(models.Model):
    participant_id = models.ForeignKey(Participant, on_delete=models.CASCADE)
    match_id = models.ForeignKey(Match, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)


class User_Event(models.Model):
        tb_user_id = models.ForeignKey(TB_user, on_delete=models.CASCADE)
        event_id = models.ForeignKey(Event, on_delete=models.CASCADE)

