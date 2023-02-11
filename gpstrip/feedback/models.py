from django.db import models
from django.conf import settings
class Feedback(models.Model):
    feedback_text = models.TextField(max_length=5000, null=True, blank=True)
    user_feedback = models.CharField(max_length=200,  blank=True, null=True)

    def __str__(self):
        return self.feedback_text


# Create your models here.
