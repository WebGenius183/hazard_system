from django.db import models
from django.contrib.auth.models import User

class HazardReport(models.Model):

    SEVERITY_CHOICES = [
        ('A', 'Catastrophic'),
        ('B', 'Hazardous'),
        ('C', 'Major'),
        ('D', 'Minor'),
        ('E', 'Negligible')
    ]

    PROBABILITY_CHOICES = [
        (5, 'Frequent'),
        (4, 'Occasional'),
        (3, 'Remote'),
        (2, 'Improbable'),
        (1, 'Extremely Improbable'),
    ]

    RISK_LEVEL_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    STATUS_CHOICES = [
        ('Submitted', 'Submitted'),
        ('Reviewed', 'Reviewed'),
        ('Closed', 'Closed'),
    ]

    # Hazard Details
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    description = models.TextField()

    # Risk Assessment
    severity = models.CharField(max_length=1, choices=SEVERITY_CHOICES)
    probability = models.IntegerField(choices=PROBABILITY_CHOICES)
    risk_level = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES)
    risk_tolerability = models.CharField(max_length=50)

    # Reporter Info
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    reporter_name = models.CharField(max_length=255)  # optional, if you want extra name
    contact_info = models.CharField(max_length=255)

    # Actions Taken
    immediate_actions = models.TextField()
    recommended_actions = models.TextField()  # fixed typo

    # Status & Review
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Submitted')
    supervisor_notes = models.TextField(blank=True, null=True)
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_reports'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Hazard at {self.location} - {self.risk_level}"
