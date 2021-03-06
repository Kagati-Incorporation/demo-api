import uuid

from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    modified_on = models.DateTimeField(
        help_text="Object modified date and time", blank=True)
    created_on = models.DateTimeField(help_text="Object created date and time", blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        now = timezone.now()
        if not self.pk:
            self.created_on = now
        self.modified_on = now
        super().save(*args, **kwargs)


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class BaseModel(models.Model):
    """
    the base models for homework to store date and time of every object
    creation, modification and deletion
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_deleted = models.BooleanField(default=False,
                                     help_text="Is the object deleted?")
    modified_on = models.DateTimeField(
        help_text="Object modified date and time", blank=True)
    created_on = models.DateTimeField(help_text="Object created date and time", blank=True)

    deleted_on = models.DateTimeField(null=True, default=None,
                                      help_text="Object deleted date and time", blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        now = timezone.now()
        if not self.pk:
            self.created_on = now
        self.modified_on = now
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        now = timezone.now()
        self.deleted_on = now
        self.is_deleted = True
        super().save()


class SEOBaseModel(TimeStampedModel):
    og_url = models.URLField(blank=True, default="https://kunyo.co")
    og_title = models.CharField(max_length=255, blank=True, default="")
    og_description = models.TextField(blank=True, default="")
    og_image = models.ImageField(upload_to='seo-uploads', null=True, blank=True)
    meta_title = models.CharField(max_length=255, default="", blank=True)
    meta_description = models.TextField(default="", blank=True)
    keywords = models.TextField(default="", blank=True)
    tags = models.TextField(default="", blank=True)

    class Meta:
        abstract = True


class FileUpload(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='file_uploads',
        default=None,
        null=True,
        blank=True,

    )
    file = models.FileField(upload_to='files')
