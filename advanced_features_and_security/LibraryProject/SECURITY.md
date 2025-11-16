Security Notes

This project includes a set of security hardenings and examples demonstrating safer coding practices.

1) Settings hardenings (see `LibraryProject/settings.py`)
- `DEBUG` is set to `False` by default to avoid exposing debug information in production.
- `SECURE_BROWSER_XSS_FILTER = True` enables XSS protection in compatible browsers.
- `SECURE_CONTENT_TYPE_NOSNIFF = True` prevents MIME sniffing.
- `X_FRAME_OPTIONS = 'DENY'` prevents the site from being framed (clickjacking protection).
- `CSRF_COOKIE_SECURE` and `SESSION_COOKIE_SECURE` are set to `True` so cookies are only sent via HTTPS.
- `SESSION_COOKIE_HTTPONLY = True` to prevent client-side scripts from accessing session cookies.

2) Content Security Policy
- A small middleware `LibraryProject.middleware.security.SecurityHeadersMiddleware` injects a basic
  `Content-Security-Policy` header based on `CSP_DEFAULT_SRC`, `CSP_SCRIPT_SRC`, and `CSP_STYLE_SRC`.
  You should customize these directives to match allowed domains (CDNs, analytics, etc.) for your app.

3) Views and forms
- `bookshelf` now uses a `BookForm` (`bookshelf/forms.py`) which validates and sanitizes input.
- Create/Edit actions use POST and require permission checks. Delete requires POST as well.
- Templates include `{% csrf_token %}` to protect forms from CSRF attacks.

4) Templates
- Templates use `{{ value|escape }}` or rely on Django autoescaping to avoid XSS.

5) Further recommendations
- Add `SECURE_SSL_REDIRECT = True` behind an HTTPS-enabled production stack.
- Configure `CSRF_TRUSTED_ORIGINS` when using a domain/hostname that differs from request host.
- Integrate a reporting endpoint for CSP violations during rollout with `report-uri` or `report-to`.
- Consider using `django-csp` for a richer CSP configuration experience.

Testing
- Use the test users created by `python manage.py setup_groups` to verify permission behavior.
- Manually test forms for CSRF by removing the token and verifying the server rejects POSTs.
- Use browser devtools to verify the CSP header appears and blocks disallowed resources.
