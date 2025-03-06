from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import ValidationError

from custom_auth import security


class ProtectedPathsMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest) -> None:
        protected = "/api/protected/"

        if request.path.startswith(protected):
            access_jwt = request.headers.get("access_jwt", "")
            if not access_jwt:
                raise ValidationError("access_jwt not found")
            access_payload = security.decode_and_verify_jwt(access_jwt)
            if not access_payload:
                raise ValidationError("access _jwt is invalid")
            request.custom_data = access_payload

        return None

