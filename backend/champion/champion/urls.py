"""champion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tournament import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('types/', views.SportTypes.as_view()),
    path('events/<int:st>', views.Events.as_view()),
    path('event/<int:pk>', views.Event.as_view()),
    path('findsports/<str:name>', views.FindSports.as_view()),
    path('subevents/<int:ev>', views.Subevents.as_view()),
    path('participants/<int:sid>', views.Participants.as_view()),
    path('participant/<int:pk>', views.Participant.as_view()),
    path('countsubevent/<int:evid>', views.CountSubevents.as_view()),
    path('countparticipants/<int:evid>', views.CountParticipants.as_view()),
    path('matches/<int:sid>', views.Matches.as_view()),
    path('match/<int:pk>', views.Match.as_view()),
    path('sport/<int:pk>', views.SportData.as_view()),
    path('avg/<int:pk>', views.AvgCounts.as_view()),
]
