# LibraryProject/middleware.py
from django.conf import settings

class ContentSecurityPolicyMiddleware:
    """
    Simple CSP middleware. For complex sites use django-csp.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.csp_policy = getattr(settings, "CSP_HEADER", "default-src 'self';")

    def __call__(self, request):
        response = self.get_response(request)
        response.setdefault("Content-Security-Policy", self.csp_policy)
        return response
