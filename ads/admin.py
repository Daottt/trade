from django.contrib import admin
from ads import models

admin.site.register([models.Ad, models.ExchangeProposal])
