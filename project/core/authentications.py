from django.utils.translation import gettext as _

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken

from project.settings.common import Common

from user.models import UserSession


class CustomJWTAuthentication(JWTAuthentication):
    claim_id = Common.SIMPLE_JWT.get('USER_ID_CLAIM', 'user_id')

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
        except KeyError:
            raise InvalidToken({"message":_("Token contained no recognizable user identification")})
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed({"message":_("User not found")})

        if not user.is_active:
            raise AuthenticationFailed({"message":_("User is inactive")})
        
        if user_session.expire_at is not None:
            raise AuthenticationFailed({"message":_("Session is expired")})

        return user