import jwt
import os

from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin

from core.tokens import SessionTokenObtainPairSerializer
from project.settings.common import Common
from user.models import UserSession

# Get JWT secret key
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

class JWTMiddleware(MiddlewareMixin):
    """
    Custom Middleware Class to process a request before it reached the endpoint.
    It decodes the Authorization Token from the header and if the decode successfull
    we forward the response to endpoint.

    Else, We send the response with `401` status code.
    """

    user_model = get_user_model()  # Get the user model define in the settings `AUTH_USER_MODEL`
    refresh_token_lookup = 'x-refresh'
    access_token_lookup = 'x-access'
    claim_id = Common.SIMPLE_JWT.get('USER_ID_CLAIM', 'user_id')
    algorithms = Common.SIMPLE_JWT.get('ALGORITHM', ['HS256', ])

    @staticmethod
    def decode_token(token):
        try:
            # If the token expired this raise jwt.ExpiredSignatureError
            payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=JWTMiddleware.algorithms)
            return payload
        except (
            jwt.ExpiredSignatureError,
            jwt.DecodeError
        ):
            return None

    def get_session(self, payload):
        '''
        Get the session for the given token.
        '''
        try:
            session_id = payload[self.claim_id]
            session = UserSession.objects.get(id=session_id)
            return session
        except UserSession.DoesNotExist:
            return None

    def process_response(self, request, response):
        """
        Custom middleware handler to check authentication for a user with JWT authentication
        :param request: Request header containing authorization tokens
        :type request: Django Request Object
        :return: HTTP Response if authorization fails, else response.status_code = 401
        """
        if 'Authorization' not in request.headers:
            return response

        access_token = request.headers.get('Authorization').replace('Bearer ', '')
        access_token_payload = self.decode_token(access_token)

        if not access_token_payload:
            response.status_code = 401
            return response

        session = self.get_session(access_token_payload)
        if not session:
            response.status_code = 401
            return response

        try:
            self.get_session(access_token_payload)
            return response
        except jwt.ExpiredSignatureError:
            refresh_token = request.headers.get(self.refresh_token_lookup)
            if not refresh_token:
                response.status_code = 401
                return response

            refresh_token_payload = self.decode_token(refresh_token)
            if not refresh_token_payload:
                response.status_code = 401
                return response

            session = self.get_session(refresh_token_payload)
            if not session:
                response.status_code = 401
                return response

            new_access_token = self.get_access_token_for_user(session.user, session.id)
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_access_token}'
            request.META[self.access_token_lookup] = new_access_token
            response.headers.setdefault(self.access_token_lookup, new_access_token)
            return response

    def get_access_token_for_user(self, user, session_id):
        '''
        Return the access token for the user.
        '''
        refresh = SessionTokenObtainPairSerializer.get_token(
            user=user,
            session_id=session_id
        )
        return str(refresh.access_token)
