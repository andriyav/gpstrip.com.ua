from django.db import models
from django.conf import settings
class Feedback(models.Model):
    feedback_text = models.TextField(max_length=5000, null=True, blank=True)
    user_feedback = models.CharField(max_length=200,  blank=True, null=True)
    time_feedback = models.DateTimeField(null=True)
    slug = models.CharField(max_length=20, blank=True, null=True)
    rate = models.CharField(max_length=2, blank=True, null=True)

    def __str__(self):
        return self.user_feedback


# Create your models here.
