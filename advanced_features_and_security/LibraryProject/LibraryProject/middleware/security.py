from django.conf import settings


class SecurityHeadersMiddleware:
    """Middleware to add security headers like Content-Security-Policy.

    This is a lightweight approach to add CSP without external deps.
    Configure CSP via `CSP_DEFAULT_SRC`, `CSP_SCRIPT_SRC`, `CSP_STYLE_SRC` in settings.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Build CSP header from settings
        try:
            default_src = ' '.join(settings.CSP_DEFAULT_SRC)
        except Exception:
            default_src = "'self'"
        try:
            script_src = ' '.join(settings.CSP_SCRIPT_SRC)
        except Exception:
            script_src = default_src
        try:
            style_src = ' '.join(settings.CSP_STYLE_SRC)
        except Exception:
            style_src = default_src

        csp_value = f"default-src {default_src}; script-src {script_src}; style-src {style_src};"
        response.setdefault('Content-Security-Policy', csp_value)

        # Other helpful headers
        response.setdefault('X-Content-Type-Options', 'nosniff')
        response.setdefault('X-Frame-Options', getattr(settings, 'X_FRAME_OPTIONS', 'DENY'))
        response.setdefault('Referrer-Policy', 'no-referrer-when-downgrade')

        return response
