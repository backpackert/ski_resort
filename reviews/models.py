from django.db import models
import uuid
from datetime import datetime, timedelta
from django.utils import timezone
from rental.models import RegisteredUser


class Review(models.Model):
    brief = models.CharField(max_length=100)
    full_text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/reviews', null=True, blank=True, default=None)

    def __str__(self):
        return self.brief

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
