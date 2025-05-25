from django.db import models
from django.conf import settings

class Ad(models.Model):
    class ProductStatus(models.TextChoices):
        New = "ne", "новый"
        Used = "us", "б/у"

    class AdCategory(models.TextChoices):
        OTHER = "ot", "другое"
        ELECTRONICS = "el", "электроника"
        CLOTHING = "cl", "одежда"
        FURNITURE = "fu", "мебель"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    category = models.CharField(max_length=2, choices=AdCategory, default=AdCategory.OTHER)
    condition = models.CharField(max_length=2, choices=ProductStatus, default=ProductStatus.New)
    created_at = models.DateField(auto_now_add=True)

class ExchangeProposal(models.Model):
    class ExchangeStatus(models.TextChoices):
        WAITING = "wa", "ожидает"
        ACCEPTED = "ac", "принята"
        DENIED = "de", "отклонена"

    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="sender")
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="receiver")
    comment = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=2, choices=ExchangeStatus, default=ExchangeStatus.WAITING)
    created_at = models.DateField(auto_now_add=True)
