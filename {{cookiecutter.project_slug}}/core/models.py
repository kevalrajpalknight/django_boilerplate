import os
from uuid import uuid4

from django.db import models
from django.utils.translation import gettext as _

from model_utils import FieldTracker
from model_utils.models import TimeStampedModel, UUIDModel, SoftDeletableModel


def file_upload_path(instance, filename):
    """
    Generate a unique file path for the uploaded file.

    This function is used as the `upload_to` argument for the `FileField` in the model.

    Args:
    - instance: The model instance the file is attached to.
    - filename: The original filename of the uploaded file.

    Returns:
    - str: The unique file path.
    """
    # Get the model's class name and convert it to lowercase
    model_name = instance.__class__.__name__.lower()

    # Generate a unique filename using UUID4 and the original file extension
    _, file_extension = os.path.splitext(filename)
    unique_filename = f"{uuid4().hex}{file_extension}"

    # Build the final file path
    return os.path.join(model_name, unique_filename)


class BaseModel(UUIDModel, TimeStampedModel):
    """
    Abstract base model class combining UUID, timestamp, and change tracking.

    This abstract base model class inherits from `UUIDModel` and `TimeStampedModel`
    from the `model_utils` package, providing the model with a UUID field, timestamp
    fields (`created` and `modified`), and change tracking functionality through
    the `FieldTracker`.

    Attributes:
    - `tracker`: An instance of `FieldTracker` to track changes to model fields.

    Meta:
    - `abstract`: Indicates that this model is an abstract base model.
    - `ordering`: Specifies the default ordering for queries, based on the 'created'
      field in ascending order.

    Example:
    ```
    class YourModel(BaseModel):
        # Your model fields and methods go here
    ```
    """

    tracker = FieldTracker()

    class Meta:
        abstract = True
        ordering = ["created"]


class Media(BaseModel, models.Model):
    """
    This table stores information about media files uploaded to the system.

    Columns:
    - `filepath`: A string representing the path of the media file.
    - `mediatype`: A string representing the type of media (e.g. image, video, audio).

    Returns: models.Model.
    """

    MEDIA_TYPE_CHOICE = (
        ("image", "Image"),
        ("video", "Video"),
        ("document", "Document"),
    )
    title = models.CharField(verbose_name=_("Title"), max_length=250, db_column="title", blank=True)
    file_path = models.FileField(
        verbose_name=_("File Path"),
        upload_to=file_upload_path,
        db_column="file_path",
    )
    media_type = models.CharField(
        verbose_name=_("Media Type"),
        max_length=250,
        db_column="media_type",
        choices=MEDIA_TYPE_CHOICE,
        default="image",
    )

    def __str__(self):
        return str(self.file_path)

    class Meta:
        verbose_name = "Media"
        verbose_name_plural = "Media"
        db_table = "Media"
