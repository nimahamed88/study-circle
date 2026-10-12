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
        ("journal_club", "Journal Club"),
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
class SessionResource(models.Model):
    RESOURCE_TYPES = [
        ("presentation", "Presentation"),
	("paper", "Paper"),
        ("book", "Book"),
        ("article", "Article"),
        ("website", "Website"),
        ("other", "Other"),
    ]

    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name="resources",
    )
    title = models.CharField(max_length=250)
    resource_type = models.CharField(
        max_length=20,
        choices=RESOURCE_TYPES,
        default="paper",
    )
    url = models.URLField(blank=True)
    file = models.FileField(
        upload_to="sessions/resources/",
        blank=True,
        null=True,
    )
    summary = models.TextField(blank=True)

    class Meta:
        ordering = ["resource_type", "title"]

    def __str__(self):
        return self.title


class Essay(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    title = models.CharField(max_length=250)

    slug = models.SlugField(unique=True)

    author = models.ForeignKey(
        Speaker,
        on_delete=models.PROTECT,
        related_name="essays",
    )

    excerpt = models.TextField(
        blank=True,
        help_text="A short introduction displayed in essay previews.",
    )
    featured_image = models.ImageField(
    upload_to="essays/covers/",
    blank=True,
    null=True,
    help_text="Optional cover image for the essay.",
)
    content = models.TextField(
        help_text=(
            "Write in Markdown. Use $...$ for inline LaTeX "
            "and $$...$$ for display equations."
        ),
    )

    subgroups = models.ManyToManyField(
        Subgroup,
        blank=True,
        related_name="essays",
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="draft",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    published_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-published_at", "-created_at"]
        verbose_name = "Essay"
        verbose_name_plural = "Essays"

    def __str__(self):
        return self.title

    @property
    def reading_time(self):
        word_count = len(self.content.split())
        return max(1, (word_count + 199) // 200)

