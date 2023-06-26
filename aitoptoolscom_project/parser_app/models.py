from django.db import models


class Link(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'


class Info(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    summary = models.TextField()
    key_features = models.TextField()
    media = models.TextField()
    rating = models.FloatField()
    tags = models.CharField(max_length=255)
    pricing = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Info'
        verbose_name_plural = 'Infos'