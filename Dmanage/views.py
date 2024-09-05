from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from .models import User, Disaster_report
from .forms import DisasterReportForm

def index(request):
    reports = Disaster_report.objects.all()  # Fetch all disaster reports
    reports_json = serialize('json', reports, fields=('latitude', 'longitude', 'disaster_type', 'location', 'description'))
    return render(request, "Dmanage/index.html", {"reports": reports_json})

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("post_login"))  # Redirect to post_login
        else:
            return render(request, "Dmanage/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "Dmanage/login.html")

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
    

from geopy.geocoders import Nominatim
from django.shortcuts import render, redirect
from .models import Disaster_report
from .forms import DisasterReportForm

@login_required
def report_view(request):
    if request.method == 'POST':
        form = DisasterReportForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the disaster report but don't save it yet
            disaster_report = form.save(commit=False)

            # Geocode the location entered by the user
            geolocator = Nominatim(user_agent="disaster_management")
            location = geolocator.geocode(disaster_report.location)

            if location:
                # If geocoding is successful, set the latitude and longitude
                disaster_report.latitude = location.latitude
                disaster_report.longitude = location.longitude
            else:
                # If location is invalid, set default or raise an error
                return render(request, 'Dmanage/report_form.html', {
                    'form': form,
                    'error_message': 'Could not find the location. Please enter a valid location.'
                })

            # Save the report with geocoded latitude and longitude
            disaster_report.save()
            return redirect('report_success')
    else:
        form = DisasterReportForm()

    return render(request, 'Dmanage/report_form.html', {'form': form})


    return render(request, 'Dmanage/report_form.html', {'form': form})

def report_success_view(request):
    return render(request, 'Dmanage/report_success.html')

def report_list_view(request):
    reports = Disaster_report.objects.all().order_by('-reported_at')
    return render(request, 'Dmanage/report_list.html', {'reports': reports})

def about(request):
    return render(request, 'Dmanage/about.html')

def contact(request):
    return render(request, 'Dmanage/contact.html')

from django.core.serializers import serialize
from .models import Disaster_report

@login_required
def post_login(request):
    # Fetch all disaster reports
    reports = Disaster_report.objects.all()
    
    # Serialize the reports into JSON format
    reports_json = serialize('json', reports, fields=('latitude', 'longitude', 'disaster_type', 'location'))
    
    return render(request, 'Dmanage/post_login.html', {"reports": reports_json})



from django.http import JsonResponse
from .models import Disaster_report

def disaster_reports_data(request):
    reports = Disaster_report.objects.all().values('latitude', 'longitude', 'disaster_type', 'location')
    return JsonResponse(list(reports), safe=False)

