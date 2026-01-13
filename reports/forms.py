from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import HazardReport
from .utils import get_risk_level, get_risk_tolerability

# -------------------------------
# Staff Registration Form
# -------------------------------
class StaffRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False  # Deactivate until approved
        if commit:
            user.save()
        return user
        
# -------------------------------
# Hazard Report Form
# -------------------------------
class HazardReportForm(forms.ModelForm):

    class Meta:
        model = HazardReport
        exclude = [
            'reporter',          # Will be set automatically in view
            'risk_level',        # Calculated automatically
            'risk_tolerability', # Calculated automatically
            'status',            # Default is 'Pending'
            'reviewed_by',       # Set when supervisor reviews
        ]

        widgets = {
            # Hazard Details
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full border rounded-lg p-2'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'w-full border rounded-lg p-2'}),
            'location': forms.TextInput(attrs={'class': 'w-full border rounded-lg p-2', 'placeholder': 'Enter location'}),
            'description': forms.Textarea(attrs={'class': 'w-full border rounded-lg p-2', 'rows': 4, 'placeholder': 'Describe the hazard'}),

            # Risk Assessment
            'severity': forms.Select(attrs={'class': 'w-full border rounded-lg p-2'}),
            'probability': forms.Select(attrs={'class': 'w-full border rounded-lg p-2'}),

            # Reporter Info
            'reporter_name': forms.TextInput(attrs={'class': 'w-full border rounded-lg p-2', 'placeholder': 'Your full name'}),
            'contact_info': forms.TextInput(attrs={'class': 'w-full border rounded-lg p-2', 'placeholder': 'Phone or email'}),

            # Actions Taken
            'immediate_actions': forms.Textarea(attrs={'class': 'w-full border rounded-lg p-2', 'rows': 3}),
            'recommended_actions': forms.Textarea(attrs={'class': 'w-full border rounded-lg p-2', 'rows': 3}),
        }

    def save(self, commit=True, user=None):
        """
        Override save to automatically calculate risk and assign reporter.
        """
        report = super().save(commit=False)

        # Calculate backend-controlled risk
        report.risk_level = get_risk_level(report.severity, report.probability)
        report.risk_tolerability = get_risk_tolerability(report.risk_level)

        # Assign reporter if provided
        if user:
            report.reporter = user

        if commit:
            report.save()

        return report
