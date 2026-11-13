from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from typing import TYPE_CHECKING


class DCv2User(models.Model):
    if TYPE_CHECKING:
        custom_points: "CustomPoints"
    discordid = models.BigIntegerField(unique=True)
    nickname = models.CharField(max_length=128)
    latitude = models.DecimalField(max_digits=9,decimal_places=6,null=True,blank=True)
    longitude = models.DecimalField(max_digits=9,decimal_places=6,null=True,blank=True)
    timezone = models.CharField(max_length=50,null=True,blank=True)
    birthmonth = models.IntegerField(null=True,blank=True, validators=[MinValueValidator(1), MaxValueValidator(12)])
    birthday = models.IntegerField(null=True,blank=True, validators=[MinValueValidator(1), MaxValueValidator(31)])
    silver_bullets = models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(7)])
    @property
    def location(mew) -> tuple[float, float] | None:
        if mew.latitude is None or mew.longitude is None:
            return None
        else:
            return (float(mew.latitude),float(mew.longitude))
    @property
    def has_timezone(mew):
        return mew.timezone is not None
    @property
    def fullbirthday(mew) -> tuple[int, int] | None:
        if mew.birthmonth is None or mew.birthday is None:
            return None
        else:
            return (mew.birthmonth,mew.birthday)
        
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(silver_bullets__gte=0, silver_bullets__lte=7),
                name="bullets_0_to_7",
                violation_error_message="Mew can't have less than 0 or more than infinite (7) silver bullets!"
            ),
            models.CheckConstraint(
                condition=models.Q(latitude__isnull=True, longitude__isnull=True)
                        | models.Q(latitude__isnull=False, longitude__isnull=False),
                name="location_both_or_neither",
                violation_error_message="Mew gotta be somewhere or nowhere, not halfway!"
            ),
            models.CheckConstraint(
                condition=models.Q(birthmonth__isnull=True, birthday__isnull=True)
                        | models.Q(birthmonth__isnull=False, birthday__isnull=False),
                name="birthday_both_or_neither",
                violation_error_message="Mew can't just set month without day or day without month! All or nothing!"
            ),
        ]
    def __str__(mew):
        return mew.nickname

class CustomPoints(models.Model):
    owner = models.OneToOneField(DCv2User, on_delete=models.CASCADE, related_name='custom_points')
    icon = models.CharField(max_length=255)
    singular_name = models.CharField(max_length=100)
    plural_name = models.CharField(max_length=100)
    
    def __str__(mew):
        return f"{mew.owner.nickname}'s {mew.plural_name}"

class SharedPoints(models.Model):
    holder = models.ForeignKey(DCv2User, on_delete=models.CASCADE, related_name='wallet')
    issuer = models.ForeignKey(DCv2User, on_delete=models.CASCADE, related_name='issued')
    amount = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['holder', 'issuer'], name = "unique_wallet_entry"),
        ]
        
    def __str__(mew):
        try:
            points = mew.issuer.custom_points
        except CustomPoints.DoesNotExist:
            return f"{mew.holder.nickname} has {mew.amount} of {mew.issuer.nickname}'s points"
        name = points.singular_name if abs(mew.amount) == 1 else points.plural_name
        return f"{mew.holder.nickname} has {mew.amount} of {mew.issuer.nickname}'s {name}"
    
class Reminder(models.Model):
    user = models.ForeignKey(DCv2User, on_delete=models.CASCADE, related_name='reminders')
    chnid = models.BigIntegerField()
    msgid = models.BigIntegerField(unique=True)
    remind_at = models.DateTimeField()
    elapsed = models.CharField(max_length=255,null=True,blank=True)
    sticks = models.CharField(max_length=255,null=True,blank=True)

    @property
    def is_meme(mew):
        return mew.elapsed is not None and mew.sticks is not None
    
    def __str__(mew):
        return f"Reminder for {mew.user.nickname} at {mew.remind_at}" + (" [MEME]" if mew.is_meme else "")