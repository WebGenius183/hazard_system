from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView
from django.contrib import messages

from .forms import HazardReportForm, StaffRegistrationForm
from .models import HazardReport

# -------------------------
# Helper: check if supervisor
# -------------------------
def is_supervisor(user):
    return user.groups.filter(name='Supervisor').exists()


# -------------------------
# Custom Login
# -------------------------
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        """Block login for inactive users (pending approval)."""
        user = form.get_user()
        if not user.is_active:
            messages.error(self.request, "Your account is not approved yet.")
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        if is_supervisor(self.request.user):
            return 'dashboard/'
        return 'my-reports/'


# -------------------------
# Staff Registration
# -------------------------
def register_staff(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # don’t save yet
            user.is_active = False           # must be approved by supervisor
            user.save()                      # now save

            staff_group, _ = Group.objects.get_or_create(name='Staff')
            user.groups.add(staff_group)

            messages.success(request, "Your account is created but needs supervisor approval.")
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = StaffRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


# -------------------------
# Supervisor Approval Page
# -------------------------
@login_required
@user_passes_test(is_supervisor)
def approve_staff(request):
    pending_users = User.objects.filter(groups__name='Staff', is_active=False)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        user.is_active = True
        user.save()
        messages.success(request, f"{user.username} has been approved.")
        return redirect('approve_staff')

    return render(request, 'reports/approve_staff.html', {'pending_users': pending_users})

# -------------------------
# Create Report (Staff)
# -------------------------
@login_required
def create_report(request):
    if request.method == 'POST':
        form = HazardReportForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            messages.success(request, "Report submitted successfully.")
            return redirect('my_reports')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = HazardReportForm()

    return render(request, 'reports/create_report.html', {'form': form})


# -------------------------
# My Reports (Staff)
# -------------------------
@login_required
def my_reports(request):
    reports = HazardReport.objects.filter(reporter=request.user).order_by('-created_at')
    return render(request, 'reports/my_reports.html', {'reports': reports})


# -------------------------
# Supervisor Dashboard
# -------------------------
@login_required
@user_passes_test(is_supervisor)
def supervisor_dashboard(request):
    reports = HazardReport.objects.all().order_by('-created_at')

    # Optional filter by risk level
    risk_filter = request.GET.get('risk')
    if risk_filter in ['High', 'Medium', 'Low']:
        reports = reports.filter(risk_level=risk_filter)

    return render(request, 'reports/supervisor_dashboard.html', {'reports': reports})


# -------------------------
# Review Report (Supervisor)
# -------------------------
@login_required
@user_passes_test(is_supervisor)
def review_report(request, report_id):
    report = get_object_or_404(HazardReport, id=report_id)

    if request.method == 'POST':
        report.status = request.POST.get('status', 'Reviewed')  # default to "Reviewed"
        report.supervisor_notes = request.POST.get('notes', '')
        report.reviewed_by = request.user  # THIS is critical
        report.save()
        messages.success(request, "Report has been reviewed.")
        return redirect('dashboard')

    return render(request, 'reports/review_report.html', {'report': report})
