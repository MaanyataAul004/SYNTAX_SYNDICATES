from django import forms
from .models import DisasterReport

class DisasterReportForm(forms.ModelForm):
    class Meta:
        model = DisasterReport
        fields = ['disaster_type', 'location', 'description', 'image']
        widgets = {
            'disaster_type': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
