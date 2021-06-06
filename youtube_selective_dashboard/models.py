from django.db import models


# This models stores Youtube API response
class YoutubeFeed(models.Model):
    title = models.CharField(max_length=300, unique=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    published_at = models.DateTimeField(db_index=True)
    thumbnails_URLs = models.CharField(max_length=200, unique=True)
    videoId = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
