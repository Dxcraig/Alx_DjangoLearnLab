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

Deployment & HTTPS (Nginx example)
---------------------------------
The application should be served behind a web server (nginx) or load
balancer that terminates TLS. Example minimal `nginx` server block:

```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    # Redirect all HTTP to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name example.com www.example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    location /static/ {
        alias /path/to/project/static/;
    }

    location /media/ {
        alias /path/to/project/media/;
    }

    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://127.0.0.1:8000;
    }
}
```

Notes:
- Enable `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')` in
  `settings.py` if you use the `X-Forwarded-Proto` header (and you trust the
  proxy). Do not enable it if untrusted traffic can set that header.
- Obtain certificates via Let's Encrypt / Certbot or a commercial CA and
  configure automatic renewal.
- Test HSTS carefully: once you enable long HSTS and preload, browsers will
  enforce HTTPS for your domain for the configured period.

Security Review
---------------
- Enforcing `SECURE_SSL_REDIRECT` ensures all clients are redirected to
  HTTPS, preventing accidental plaintext transmission of cookies and data.
- HSTS (`SECURE_HSTS_SECONDS` etc.) instructs browsers to use HTTPS for the
  site for the given duration and reduces downgrade attacks.
- Secure cookies (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`) prevent
  session and CSRF cookies from being sent over plaintext channels.
- Headers such as `X-Frame-Options`, `X-Content-Type-Options`, and a
  `Content-Security-Policy` further reduce the risk of clickjacking, MIME
  sniffing, and XSS attacks respectively.

Potential improvements
----------------------
- Configure `CSRF_TRUSTED_ORIGINS` if your site is accessed via different
  hostnames or when behind certain reverse proxies/load balancers.
- Integrate monitoring for certificate expiration and CSP violation reports.
- Harden TLS configuration (ciphers, protocols) on the web server side
  according to current best practices (Mozilla SSL Configuration Generator).

Testing
- Use the test users created by `python manage.py setup_groups` to verify permission behavior.
- Manually test forms for CSRF by removing the token and verifying the server rejects POSTs.
- Use browser devtools to verify the CSP header appears and blocks disallowed resources.
