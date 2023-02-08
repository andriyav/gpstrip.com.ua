from django.db import models
from django.conf import settings
class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True, blank=True)
    feedback_text = models.TextField(max_length=5000, null=True, blank=True)



# Create your models here.
