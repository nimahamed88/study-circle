from django.db import models


class Speaker(models.Model):

    name = models.CharField(max_length=150)

    title = models.CharField(
        max_length=200,
        blank=True,
    )

    bio = models.TextField(
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )
    instagram = models.URLField(
    blank=True,
    )
    
    linkedin = models.URLField(
        blank=True,
    )

    photo = models.ImageField(
        upload_to="speakers/",
        blank=True,
        null=True,
    )

    slug = models.SlugField(
        unique=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Member"
        verbose_name_plural = "Members"

    def __str__(self):
        return self.name


class Subgroup(models.Model):

    name = models.CharField(
        max_length=150,
    )

    slug = models.SlugField(
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    head = models.ForeignKey(
        Speaker,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="headed_subgroups",
    )

    members = models.ManyToManyField(
        Speaker,
        blank=True,
        related_name="subgroups",
    )

    email = models.EmailField(
        blank=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Session(models.Model):

    SESSION_TYPES = [
        ("main", "Main Session"),
        ("extensive", "Extensive Session"),
    ]

    title = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    speakers = models.ManyToManyField(
    Speaker,
    blank=True,
    related_name="sessions",
)

    start_time = models.DateTimeField()

    end_time = models.DateTimeField()

    session_type = models.CharField(
        max_length=20,
        choices=SESSION_TYPES,
        default="main",
    )

    room = models.CharField(
        max_length=200,
        default="Online — Google Meet",
    )

    meeting_link = models.URLField(
        blank=True,
    )
    recording_url = models.URLField(
    blank=True,
    )
    
    pdf_file = models.FileField(
        upload_to="sessions/pdfs/",
        blank=True,
        null=True,
    )

    subgroups = models.ManyToManyField(
        Subgroup,
        blank=True,
        related_name="sessions",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["start_time"]

    def __str__(self):
        return self.title