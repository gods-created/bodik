from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import RedirectResponse

class IfRouteNotFoundMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if response.status_code == 404:
            return RedirectResponse(url='/docs')
        return response