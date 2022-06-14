from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.common.mixins import AuditMixin





# Create your models here.
class UserEntry(AuditMixin):

    header = models.CharField(max_length=600)
    description = models.TextField(max_length=1500)
    created_date = models.DateTimeField(auto_now_add=True)
    video_time = models.IntegerField(default=00, verbose_name="Video Süresi Dakika: ",
                                     validators=[MinValueValidator(0), MaxValueValidator(60)])
    video_sec = models.IntegerField(default=00, verbose_name="Video Süresi Saniye: ",
                                    validators=[MinValueValidator(0), MaxValueValidator(60)])

    def __str__(self) -> str:
        return f"{self.header}"

    class Meta:
        verbose_name = "Soru Girişi"
        verbose_name_plural = "Soru Girişleri"
        ordering = ["id"]



class UserAnswer(AuditMixin):
    header = models.CharField(max_length=50)
    doc = models.FileField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.header}"
