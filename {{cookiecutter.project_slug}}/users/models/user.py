from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from users.managers.user import UserManager
from core.models import BaseModel

class User(AbstractUser):
    first_name = models.CharField(
        max_length=200,
        verbose_name=_('First name'),
        blank=True,
        null=True
    )
    last_name = models.CharField(
        max_length=200,
        verbose_name=_('Last name'),
        blank=True,
        null=True
    )
    {%- if cookiecutter.username_type == "email" %}
    email = models.EmailField(_("Email address"), unique=True)
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    {%- endif %}
    objects = UserManager()

    def __str__(self):
        return f'{self.email} -#{self.id}'


class UserSession(BaseModel):
    """
    Model to store user sessions with IP address, user agent, and expiration time.

    This model represents a user session with associated user, IP address,
    user agent, and expiration time.

    Attributes:
    - `user`: ForeignKey to the User model.
    - `ip_address`: IP address of the user during the session.
    - `agent`: User agent information stored as JSON.
    - `expire_at`: Date and time when the session will expire.

    Methods:
    - `__str__`: Returns a string representation of the user session.

    Meta:
    - `verbose_name`: "User Session"
    - `verbose_name_plural`: "User Sessions"
    - `db_table`: "UserSession"
    - `ordering`: Default ordering based on the 'created' field.

    Example:
    ```
    session = UserSession.objects.create(user=user_instance, ip_address="192.168.1.1", agent={"browser": "Chrome"})
    ```

    Note: User sessions are ordered by their creation time.
    """

    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        db_column="user",
        related_name="user_sessions",
    )
    ip_address = models.GenericIPAddressField(
        verbose_name=_("IP Address"), protocol="both", unpack_ipv4=False, null=True, blank=True, db_column="ip_address"
    )
    agent = models.JSONField(verbose_name=_("Agent"), null=True, db_column="agent")
    expire_at = models.DateTimeField(verbose_name=_("Expire At"), blank=True, null=True, db_column="expire_at")

    def __str__(self):
        return str(self.ip_address) + "(" + str(self.agent) + ")"

    class Meta:
        verbose_name = "User Session"
        verbose_name_plural = "User Sessions"
        db_table = "UserSession"
        ordering = ["created"]

    def delete(self):
        self.expire_at = now()
        super().delete()
