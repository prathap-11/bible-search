from django import forms
from .models import Correction

class CorrectionForm(forms.ModelForm):
    class Meta:
        model = Correction
        fields = ['suggested_correction']
        widgets = {
            'suggested_correction': forms.Textarea(attrs={'rows': 2, 'cols': 50}),
        }
