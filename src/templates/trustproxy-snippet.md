# Reverse-Proxy TLS Trust Snippet

The two-line fix for the mixed-content blank-screen class (protocol A1).
Output location: the app's middleware bootstrap + production env config.

Behind ANY TLS-terminating edge (Railway, Cloudflare, a load balancer), the app
receives plain HTTP and — untold — generates `http://` asset URLs that browsers
block on an https page. The page 200s to curl and renders white in browsers.

```php
// bootstrap/app.php (Laravel 11+)
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustProxies(at: '*');
})
```

```php
// app/Providers/AppServiceProvider.php — belt-and-suspenders URL scheme
public function boot(): void
{
    if ($this->app->environment('production')) {
        \Illuminate\Support\Facades\URL::forceScheme('https');
    }
}
```

## Field Documentation

| Field | Description |
|-------|-------------|
| `at: '*'` | Trust all proxies — correct on PaaS where the edge IP range is platform-managed and unknowable. On self-managed infra, list the LB IPs instead. |

## Section Specifications

- **Other stacks:** Express → `app.set('trust proxy', true)`; Django →
  `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')` — see the
  stack-adapters framework for the full rows.
- **Verification:** only a real-browser smoke proves this fix (curl does not
  enforce mixed-content policy — the A1 diagnosis trap).

*Built with Skillsmith · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
