import time
import sys

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response


from HiccupApp.users import NewHackathon, HackathonForm
from HiccupApp.forms import *


@login_required
def index(request):

    query_results = NewHackathon.objects.filter(user_id=request.user).order_by('title')
    print query_results
    return render_to_response("index.html",
                               {"query_results" : query_results, 'user':request.user})

@login_required
def addview(request):
    if request.method == 'POST':
            form = NewEventForm(request.POST)
            if form.is_valid():
                model = NewHackathon(
                    title= form.cleaned_data['title'],
                    sponsors= form.cleaned_data['sponsors'],
                    schedule= form.cleaned_data['schedule'],
                    announcements= form.cleaned_data['announcements']
                )
                model.save()
                return HttpResponseRedirect('/HiccupApp')
            else:
                print form.errors
    else:
        form = NewEventForm()

    return render(request, 'newEvent.html', {'form': form})


@login_required
def delete(request,id):
    server = NewHackathon.objects.get(uniqueId=id).delete()
    return HttpResponseRedirect('/HiccupApp')

@login_required()
def edit(request,id):
    event = NewHackathon.objects.get(uniqueId=id)
    if request.method == 'POST':
        form = NewEventForm(request.POST)
        if form.is_valid():
            form = HackathonForm(form, instance=event)
            model = NewHackathon(
                title = request.POST.get('title'),
                sponsors = request.POST.get('sponsors'),
                schedule =request.POST.get('schedule'),
                announcements = request.POST.get('announcements')
            )
            event.delete()
            model.save()
            return HttpResponseRedirect('/HiccupApp')
    else:
        form = HackathonForm(instance=event)

    return render(request, 'editForm.html', {"event" : event,'form': form})


@login_required
def password(request):
    passed = ""
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if request.POST.get("password") is None or len(request.POST.get("password")) == 0:
            passed = "Missing current password"
        if form.is_valid():
            user = authenticate(username = request.user, password = request.POST.get('password'))
            if user is not None:
                u = User.objects.get(username = request.user)
                u.set_password(request.POST.get('password1'))
                u.save()
                HttpResponseRedirect("/HiccupApp")
            else:
                print form.errors.values
    else:
        form = RegistrationForm()

    return render(request, "changePassword.html", {"form":form, "pass":passed})