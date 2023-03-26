from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator

from model_utils import models as misc_models

from core.models import (
    BaseModel, SoftDeleteModel, Media
)

from .managers import UserManager

# Create Auth User Model Start
class User(AbstractUser, BaseModel, SoftDeleteModel):
    '''
    A model class representing a user in the system.

    Attributes:
    - `username`: This attribute is set to None because the email address is used as the username instead.
    - `email`: An EmailField instance representing the email address of the user.
    - `country_code`: A CharField instance representing the country code of the user's phone number. It is optional, but if it is provided, it should be in the format of '+[1-9]\d{0,2}', where the '+' sign is followed by one to three digits.
    - `image`: A OneToOneField instance representing the user's profile image. It is related to the Media model.
    - `REQUIRED_FIELDS`: A list of field names that are required when creating a user. It includes 'first_name'.
    - `objects`: An instance of UserManager class which provides helper methods for creating and managing user accounts.

    Methods:
    - `__str__`(self): Returns the string representation of the User instance by using its ID as the value.
    - `Meta`: A class representing metadata about the model. It sets the verbose name and plural name of the model as well as the name of the database table.
    '''
    
    username = None
    email = models.EmailField(
        verbose_name=_("Email"),
        max_length=250,
        unique=True,
        null=False,
        blank=False,
        db_column="email",
    )
    country_code = models.CharField(
        verbose_name=_('Country Code'),
        max_length=250,
        blank=True,
        null=True,
        db_column="country_code",
        validators=[
            RegexValidator(
                regex='^\+[1-9]\d{0,2}$',
                message='Invalid country code',
            ),
        ]
    )
    image = models.OneToOneField(
        Media,
        verbose_name=_('Image'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        db_column="image",
        related_name='%(app_label)s_%(class)s_image'
    )
    USERNAME_FIELD = 'email'  # set email as a username
    REQUIRED_FIELDS = ['first_name',]

    objects = UserManager()

    def __str__(self):
        return str(self.id)  # return value when call model as primary key

    class Meta:
        verbose_name = "User"  # display table name
        verbose_name_plural = "Users"  # display table name as plural
        db_table = 'User'  # table name in DB

class TimeStampedModel(misc_models.TimeStampedModel, models.Model):
    """
    This abstract base model is used to store timestamps for model creation and modification in a Django Model.

    Columns:
    - `created`: A datetime object representing the creation time of the model.
    - `modified`: A datetime object representing the last modification time of the model.
    - `created_by`: A string representing the user who created the model.
    - `modified_by`: A string representing the user who last modified the model.
    """

    created_by = models.ForeignKey(
        User,
        verbose_name=_('Created By'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='created_items'
    )
    modified_by = models.ForeignKey(
        User,
        verbose_name=_('Modified By'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="modified_items",
    )

    class Meta:
        abstract = True
        ordering = ['created']  # table order in DB

class UserSession(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    This model is used to store user session details in a Django Model.

    Columns:

    - `user`: A foreign key refrence with user table.
    - `ip_address`: IP address of the user when they logged in.
    - `agent`: A json data for the user-agent (i.e. Browser) when the user logged in.
    - `expired_at`: A datetime object representing the expiration time of the login.
    """
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='sessions'
    )
    ip_address = models.GenericIPAddressField(
        verbose_name=_('IP Address'),
        protocol='both',
        unpack_ipv4=False,
        null=True,
        blank=True,
        db_column="ip_address"
    )
    agent = models.JSONField(
        verbose_name=_('Agent'),
        null=True,
        db_column="agent"
    )
    expire_at = models.DateTimeField(
        verbose_name=_('Expire At'),
        blank=True,
        null=True,
        db_column="expire_at"
    )

    def __str__(self):
        return str(self.ip_address) + "(" + str(self.agent) + ")"

    class Meta:
        verbose_name = "User Session"
        verbose_name_plural = "User Sessions"
        db_table = "UserSession"
        ordering = ['created']
