from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView

urlpatterns = [
    path('new/', views.create_report, name='create_report'),
    path('my-reports/', views.my_reports, name='my_reports'),
    path('dashboard/', views.supervisor_dashboard, name='dashboard'),
    path('review/<int:report_id>/', views.review_report, name='review_reports'),
    path('approve-staff/', views.approve_staff, name='approve_staff'),

    # Auth URLs
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register_staff, name='register'),  
]
