from django.http import HttpResponsePermanentRedirect

from src.pages.models import LegacyRedirect


class LegacyRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'GET':
            redirect = self._find_redirect(request.path)
            if redirect:
                return HttpResponsePermanentRedirect(redirect.new_path)
        return self.get_response(request)

    @staticmethod
    def _find_redirect(path):
        candidates = {path, path.rstrip('/') or '/', path.rstrip('/') + '/'}
        return LegacyRedirect.objects.filter(old_path__in=candidates, is_active=True).first()
