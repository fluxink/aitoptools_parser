from django.db import models


class Link(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, unique=True)
    parsed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Link"
        verbose_name_plural = "Links"


class Info(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    summary = models.TextField(null=True)
    key_features = models.CharField(max_length=255, null=True)
    media = models.CharField(max_length=255, null=True)
    rating = models.FloatField(null=True)
    tags = models.CharField(max_length=255, null=True)
    pricing = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Info"
        verbose_name_plural = "Infos"
