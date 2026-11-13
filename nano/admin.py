from django.contrib import admin
from .models import DCv2User, CustomPoints, SharedPoints, Reminder


admin.site.register(DCv2User)
admin.site.register(CustomPoints)
admin.site.register(SharedPoints)
admin.site.register(Reminder)