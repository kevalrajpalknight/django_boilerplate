from django.conf import settings
from django.utils.translation import gettext as _

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from user.models import UserSession


class CustomJWTAuthentication(JWTAuthentication):
    claim_id = settings.SIMPLE_JWT.get("USER_ID_CLAIM", "user_id")

    def get_user(self, validated_token):
        """
        This function attempts to find and return a user using the given validated token.

        Args:
            validated_token (Dict[str, Any]): The validated JWT token.

        Returns:
            User: The user associated with the given token if found and active, otherwise raises an exception.

        Raises:
            InvalidToken: If the token contains no recognizable user identification.
            AuthenticationFailed: If the user is not found or is inactive.
        """
        try:
            session_id = validated_token[self.claim_id]
            user_session = UserSession.objects.get(id=session_id)
            user = UserSession.objects.get(id=session_id).user
        except UserSession.DoesNotExist:
            raise AuthenticationFailed({"error": [_("Session not found")]})
        except KeyError:
            raise InvalidToken({"error": [_("Token contained no recognizable user identification")]})
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed({"error": [_("User not found")]})

        if not user.is_active:
            raise AuthenticationFailed({"error": [_("User is inactive")]})

        if user.is_deleted:
            raise AuthenticationFailed({"error": [_("User is deleted")]})

        if user.is_blocked:
            raise AuthenticationFailed({"error": [_("User is blocked")]})

        if user_session.expire_at is not None:
            raise AuthenticationFailed({"error": [_("Session is expired")]})

        return user
