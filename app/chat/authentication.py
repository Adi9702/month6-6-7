from rest_framework_simplejwt.authentication import JWTAuthentication

class QueryParamJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        query_params = getattr(request, "query_params", None)
        if query_params is None:
            query_params = getattr(request, "GET", {})

        raw_token = query_params.get("token")
        if raw_token:
            validated_token = self.get_validated_token(raw_token)
            return self.get_user(validated_token), validated_token
        return super().authenticate(request)
