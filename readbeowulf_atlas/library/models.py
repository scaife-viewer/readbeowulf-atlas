from django.contrib.postgres.fields import JSONField
from django.db import models


class Version(models.Model):
    """
    urn:cts:angLit:anon.beowulf
    """

    urn = models.CharField(max_length=255)
    name = models.CharField(blank=True, null=True, max_length=255)
    metadata = JSONField(encoder="", default=dict, blank=True)
    """
    {
        "work_urn": "urn:cts:angLit:anon.beowulf.perseus-ang1",
        "work_title": "Beowulf",
        "type": "version"
    }
    """

    class Meta:
        ordering = ["urn"]

    def __str__(self):
        return self.name


class Fitt(models.Model):
    """
    urn:cts:angLit:anon.beowulf.1
    """

    position = models.IntegerField()
    idx = models.IntegerField(help_text="0-based index")

    version = models.ForeignKey(
        "library.Version", related_name="fitts", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["idx"]

    @property
    def label(self):
        return f"{self.position}"

    def __str__(self):
        return f"{self.version} [fitt={self.position}]"


class Paragraph(models.Model):
    """
    urn:cts:angLit:anon.beowulf.1.1
    """

    position = models.IntegerField()
    idx = models.IntegerField(help_text="0-based index")

    fitt = models.ForeignKey(
        "library.Fitt", related_name="paragraphs", on_delete=models.CASCADE
    )
    version = models.ForeignKey(
        "library.Version", related_name="paragraphs", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["idx"]

    @property
    def label(self):
        return f"{self.fitt}:{self.position}"

    def __str__(self):
        return f"{self.version} [paragraph={self.position}]"


class Line(models.Model):
    """
    urn:cts:angLit:anon.beowulf.1.1.1
    """

    position = models.IntegerField()
    idx = models.IntegerField(help_text="0-based index")

    paragraph = models.ForeignKey(
        "library.Paragraph", related_name="lines", on_delete=models.CASCADE
    )
    fitt = models.ForeignKey(
        "library.Fitt", related_name="lines", on_delete=models.CASCADE
    )
    version = models.ForeignKey(
        "library.Version", related_name="lines", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["idx"]

    @property
    def label(self):
        return f"{self.fitt}:{self.paragraph}:{self.position}"

    def __str__(self):
        return f"{self.version} [line={self.position}]"


class HalfLine(models.Model):
    """
    urn:cts:angLit:anon.beowulf.1.1.1.a
    """

    position = models.CharField(max_length=1)
    idx = models.IntegerField(help_text="0-based index")

    line = models.ForeignKey(
        "library.Line", related_name="halflines", on_delete=models.CASCADE
    )
    paragraph = models.ForeignKey(
        "library.Paragraph", related_name="halflines", on_delete=models.CASCADE
    )
    fitt = models.ForeignKey(
        "library.Fitt", related_name="halflines", on_delete=models.CASCADE
    )
    version = models.ForeignKey(
        "library.Version", related_name="halflines", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["idx"]

    @property
    def label(self):
        return f"{self.fitt}:{self.paragraph}:{self.line}:{self.position}"

    def __str__(self):
        return f"{self.version} [halfline={self.line.position}:{self.position.upper()}]"


class Token(models.Model):
    """
    urn:cts:angLit:anon.beowulf.1.1.1.a.1
    """

    pre_punctuation = models.CharField(max_length=2, null=True, blank=True)
    text_content = models.CharField(max_length=16)
    post_punctuation = models.CharField(max_length=11, null=True, blank=True)
    syntax = models.CharField(max_length=3, null=True, blank=True)
    parse = models.CharField(max_length=6, null=True, blank=True)
    lemma = models.CharField(max_length=17)
    part_of_speech = models.CharField(max_length=2)
    o = models.CharField(max_length=2, null=True, blank=True)
    gloss = models.CharField(max_length=44)
    with_length = models.CharField(max_length=66)
    first_in_paragraph = models.BooleanField()
    non_verse = models.BooleanField()
    caesura_boundary = models.BooleanField()

    position = models.IntegerField()
    idx = models.IntegerField(help_text="0-based index")

    halfline = models.ForeignKey(
        "library.HalfLine", related_name="tokens", on_delete=models.CASCADE
    )
    line = models.ForeignKey(
        "library.Line", related_name="tokens", on_delete=models.CASCADE
    )
    paragraph = models.ForeignKey(
        "library.Paragraph", related_name="tokens", on_delete=models.CASCADE
    )
    fitt = models.ForeignKey(
        "library.Fitt", related_name="tokens", on_delete=models.CASCADE
    )
    version = models.ForeignKey(
        "library.Version", related_name="tokens", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["idx"]

    @property
    def label(self):
        return f"{self.fitt}:{self.paragraph}:{self.line}:{self.halfline}:{self.position}"

    def __str__(self):
        return f"{self.version} [token={self.position}]"
