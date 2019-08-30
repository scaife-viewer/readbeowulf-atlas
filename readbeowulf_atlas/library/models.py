from django.contrib.postgres.fields import JSONField
from django.db import models


class Version(models.Model):
    """
    urn:cts:
    """

    urn = models.CharField(max_length=255)
    name = models.CharField(blank=True, null=True, max_length=255)
    metadata = JSONField(encoder="", default=dict, blank=True)
    """
    {
        "work_urn": "urn:cts:greekLit:tlg1271.tlg001.1st1K-grc1",
        "work_title": "The First Epistle of Clement",
        "type": "version"
    }
    """

    class Meta:
        ordering = ["urn"]

    def __str__(self):
        return self.name
