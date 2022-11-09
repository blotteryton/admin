from django.db import models


class Notification(models.Model):
    class Category(models.TextChoices):
        SALE = "SALE", "SALE"
        DRAW = "DRAW", "DRAW"
        COLLECTION = "COLLECTION", "COLLECTION"

    header = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to="notifications/%Y/%m/%d/")

    category = models.CharField(max_length=10, choices=Category.choices, blank=True, null=True)

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
