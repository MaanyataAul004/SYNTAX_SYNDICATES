from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User


def index(request):
    return render(request,"Dmanage/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "Dmanage/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request,"Dmanage/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request,"Dmanage/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request,"Dmanage/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request,"Dmanage/register.html")


from django.shortcuts import render, redirect
from .forms import DisasterReportForm
from .models import Disaster_report

def report_view(request):
    if request.method == 'POST':
        form = DisasterReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('report_success')
    else:
        form = DisasterReportForm()
    return render(request, 'report_form.html', {'form': form})

def report_success_view(request):
    return render(request, 'report_success.html')

def report_list_view(request):
    reports = Disaster_report.objects.all().order_by('-reported_at')
    return render(request, 'report_list.html', {'reports': reports})
