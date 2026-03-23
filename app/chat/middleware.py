
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

class QueryParamJWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        params = parse_qs(query_string)
        raw_token = params.get("token", [None])[0]

        scope["user"] = await self.get_user(raw_token)
        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, raw_token):
        # Ленивая загрузка импортов, чтобы Django apps уже были готовы
        from django.contrib.auth.models import AnonymousUser
        from rest_framework_simplejwt.authentication import JWTAuthentication

        if not raw_token:
            return AnonymousUser()

        auth = JWTAuthentication()
        try:
            validated_token = auth.get_validated_token(raw_token)
            return auth.get_user(validated_token)
        except Exception:
            return AnonymousUser()