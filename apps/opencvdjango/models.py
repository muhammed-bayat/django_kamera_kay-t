from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.common.mixins import AuditMixin


class Cevap(AuditMixin):
    """
    Cevap modeli
    """
    cevap = models.CharField(max_length=500)
    dogru = models.BooleanField(default=False)

    def __str__(self):
        return self.cevap



# Create your models here.
class UserEntry(AuditMixin):
    Rating = [
        ('Video', 'Video'),
        ('test', 'Test')
    ]

    header = models.CharField(max_length=50)
    description = models.TextField(max_length=300)
    created_date = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(max_length=15, choices=Rating)

    video_time = models.IntegerField(default=00, verbose_name="Video Süresi Dakika: ",
                                     validators=[MinValueValidator(0), MaxValueValidator(60)])
    video_sec = models.IntegerField(default=00, verbose_name="Video Süresi Saniye: ",
                                    validators=[MinValueValidator(0), MaxValueValidator(60)])

 
    cevaplar= models.ManyToManyField(Cevap, blank=True)
    def __str__(self) -> str:
        return f"{self.header}"

class UserAnswer(AuditMixin):
    header = models.CharField(max_length=50)
    doc = models.FileField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.header}"