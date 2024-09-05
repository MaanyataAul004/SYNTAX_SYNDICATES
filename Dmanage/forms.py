from django import forms
from .models import Disaster_report

class DisasterReportForm(forms.ModelForm):
    class Meta:
        model = Disaster_report
        fields = ['disaster_type', 'location', 'description', 'image', 'latitude', 'longitude']
        widgets = {
            'disaster_type': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'latitude': forms.HiddenInput(),  # Hidden fields for latitude
            'longitude': forms.HiddenInput(),  # Hidden fields for longitude
        }

