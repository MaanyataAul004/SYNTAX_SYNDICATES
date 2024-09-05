
from django.contrib import admin
from .models import Disaster_report

@admin.register(Disaster_report)
class DisasterReportAdmin(admin.ModelAdmin):
    list_display = ('disaster_type', 'location', 'latitude', 'longitude', 'reported_at')
