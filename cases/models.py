from django.db import models
from django.conf import settings  # This is used to reference the custom user model (AppUser)

class Case(models.Model):
    CATEGORY_CHOICES = [
        ('Surgery', 'Surgery'),
        ('Medicine', 'Medicine'),
        # Add other categories as needed
    ]
    
    app_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cases')  # Link to AppUser
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    case_title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='case_images/', blank=True, null=True)
    signalment_and_history = models.TextField(blank=True, null=True)
    clinical_examination = models.TextField(blank=True, null=True)
    clinical_findings = models.TextField(blank=True, null=True)
    differential_diagnoses = models.TextField(blank=True, null=True)
    tentative_diagnoses = models.TextField(blank=True, null=True)
    management = models.TextField(blank=True, null=True)
    diagnostic_plan = models.TextField(blank=True, null=True)
    advice_to_clients = models.TextField(blank=True, null=True)
    assistants = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.case_title


class LaboratoryReport(models.Model):
    case = models.ForeignKey(Case, related_name='laboratory_reports', on_delete=models.CASCADE)
    report_title = models.CharField(max_length=200)
    report_details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.report_title


class Comment(models.Model):
    case = models.ForeignKey(Case, related_name='comments', on_delete=models.CASCADE)
    app_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)  # Self-referencing FK for replies
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.app_user} on {self.case}"


    @property
    def is_reply(self):
        return self.parent is not None



