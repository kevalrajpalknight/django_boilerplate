from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from project.settings.common import Common

USER_ID_CLAIM = 'user_id'
SESSION_ID_CLAIM = 'session_id'

class SessionTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer class that extends the functionality of TokenObtainPairSerializer.
    The class adds the session_id to the token data.
    
    Args:
    user (User): The User model instance.
    session_id (str): The session id that needs to be added to the token data.
    
    Returns:
    dict: The token data with added session_id.
    """
    @classmethod
    def get_token(cls, user, session_id):
        """
        Method to generate token data by calling the parent class's `get_token` method and adding the session_id to it.
        
        Args:
        user (User): The User model instance.
        session_id (str): The session id that needs to be added to the token data.
        
        Returns:
        dict: The token data with added session_id.
        """
        token = super().get_token(user)
        token[SESSION_ID_CLAIM] = str(session_id)

        return token

class SessionTokenObtainPairView(TokenObtainPairView):
    """
    View class that extends the functionality of TokenObtainPairView.
    The class sets the serializer class as `SessionTokenObtainPairSerializer` which adds the session_id to the token data.
    """
    serializer_class = SessionTokenObtainPairSerializer

class PasswordResetTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer class that extends the functionality of TokenObtainPairSerializer.
    The class adds the user_id to the token data.
    
    Args:
    user (User): The User model instance.
    user_id (str): The user id that needs to be added to the token data.
    
    Returns:
    dict: The token data with added user_id.
    """
    @classmethod
    def get_token(cls, user, user_id):
        """
        Method to generate token data by calling the parent class's `get_token` method and adding the user_id to it.
        
        Args:
        user (User): The User model instance.
        user_id (str): The user id that needs to be added to the token data.
        
        Returns:
        dict: The token data with added user_id.
        """
        token = super().get_token(user)
        del token[SESSION_ID_CLAIM]
        token[USER_ID_CLAIM] = str(user_id)
        return token

class PasswordResetTokenObtainPairView(TokenObtainPairView):
    """
    View class that extends the functionality of TokenObtainPairView.
    The class sets the serializer class as `PasswordResetTokenObtainPairSerializer` which adds the user_id to the token data.
    """
    serializer_class = PasswordResetTokenObtainPairSerializer

class PasswordChangeTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer class that extends the functionality of TokenObtainPairSerializer.
    The class adds the user_id to the token data.
    
    Args:
    user (User): The User model instance.
    user_id (str): The user id that needs to be added to the token data.
    
    Returns:
    dict: The token data with added user_id.
    """
    @classmethod
    def get_token(cls, user, user_id, otp):
        """
        Method to generate token data by calling the parent class's `get_token` method and adding the user_id to it.
        
        Args:
        user (User): The User model instance.
        user_id (str): The user id that needs to be added to the token data.
        
        Returns:
        dict: The token data with added user_id.
        """
        token = super().get_token(user)
        del token[SESSION_ID_CLAIM]
        token[USER_ID_CLAIM] = str(user_id)
        return token

class PasswordChangeTokenObtainPairView(TokenObtainPairView):
    """
    View class that extends the functionality of TokenObtainPairView.
    The class sets the serializer class as `PasswordChangeTokenObtainPairSerializer` which adds the user_id to the token data.
    """
    serializer_class = PasswordChangeTokenObtainPairSerializer