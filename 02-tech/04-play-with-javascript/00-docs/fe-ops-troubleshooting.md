# Frontend Operations & Troubleshooting

## Day 3 (PM Session) — Jul 31, 2026

---

## 1. Page Load

### How a Browser Loads a Page
- **Step 1: DNS Lookup** — browser resolves domain name (e.g., example.com) to an IP address
- **Step 2: TCP Connection** — 3-way handshake (SYN → SYN-ACK → ACK) establishes connection
- **Step 3: TLS Handshake** — if HTTPS, browser and server negotiate encryption
- **Step 4: HTTP Request** — browser sends GET request for the HTML document
- **Step 5: Server Response** — server sends back HTML with status code (200, 301, 404, etc.)
- **Step 6: HTML Parsing** — browser reads HTML top-to-bottom, builds the DOM (Document Object Model)
- **Step 7: CSS Parsing** — browser parses CSS files/inline styles, builds the CSSOM (CSS Object Model)
- **Step 8: Render Tree** — DOM + CSSOM combined into a render tree (only visible elements)
- **Step 9: Layout** — browser calculates exact position and size of every element
- **Step 10: Paint** — browser draws pixels on the screen (text, colors, borders, shadows, images)
- **Step 11: Composite** — layers are composited together (for transforms, opacity, etc.)

### Critical Rendering Path (CRP)
- The sequence of steps the browser takes to convert HTML, CSS, and JS into pixels on screen
- **DOM** — parsed from HTML, constructed incrementally as HTML is received
- **CSSOM** — CSS is render-blocking; browser won't render until all CSS is parsed
- **JavaScript** — parser-blocking by default; pauses DOM construction until script is downloaded and executed
- **Render Tree** — combines DOM + CSSOM, excludes invisible elements (`display: none`, `<head>`, etc.)
- **Goal:** minimize the critical rendering path length to achieve faster first paint

### Script Loading Strategies
- **Default `<script>`** — blocks HTML parsing; browser stops, downloads, executes, then resumes parsing
- **`<script defer>`** — downloads in parallel with HTML parsing; executes after DOM is fully parsed; maintains order
- **`<script async>`** — downloads in parallel; executes immediately when ready; does NOT maintain order
- **Best practice:** use `defer` for app scripts, `async` for independent scripts (analytics, ads)
- **Placement:** place `<script>` at the end of `<body>` or use `defer` in `<head>`

### Optimization Techniques
- **Minification** — removes whitespace, comments, shortens variable names; tools: Terser, UglifyJS, cssnano
- **Compression** — server compresses files before sending; Gzip (60-70% reduction), Brotli (20% better than Gzip)
- **Bundling** — combine multiple JS/CSS files into fewer files; reduces HTTP requests; tools: Webpack, Vite, esbuild
- **CDN (Content Delivery Network)** — serves static assets from geographically nearest edge server; reduces latency
- **Caching** — browser stores files locally; controlled by HTTP headers (Cache-Control, ETag, Last-Modified)
- **Preloading** — `<link rel="preload" href="font.woff2" as="font">` tells browser to fetch critical resources early
- **Preconnect** — `<link rel="preconnect" href="https://api.example.com">` establishes early connection to external origins
- **DNS Prefetch** — `<link rel="dns-prefetch" href="https://cdn.example.com">` resolves DNS ahead of time
- **HTTP/2** — multiplexing (multiple requests over single connection), header compression, server push
- **Tree Shaking** — removes unused code from bundles; works with ES module `import/export` syntax
- **Image Optimization** — use WebP/AVIF format, compress, specify width/height, use `srcset` for responsive images

### Measuring Page Load Performance
- **Navigation Timing API** — `performance.getEntriesByType("navigation")` gives detailed timing breakdown
- **DOMContentLoaded event** — fires when HTML is fully parsed (DOM ready); CSS, images may still be loading
- **Load event** — fires when everything is loaded (images, CSS, scripts, iframes)
- **Core Web Vitals (Google):**
  - **LCP (Largest Contentful Paint)** — time to render largest visible element; target: < 2.5 seconds
  - **FID (First Input Delay)** — time from user's first interaction to browser response; target: < 100ms
  - **CLS (Cumulative Layout Shift)** — visual stability; how much layout shifts during load; target: < 0.1
- **Lighthouse** — Chrome DevTools audit tool; scores Performance, Accessibility, Best Practices, SEO
- **WebPageTest** — online tool for detailed page load waterfall analysis
- **Chrome DevTools Performance panel** — record and analyze runtime performance frame by frame

---

## 2. Lazy Loading

### What is Lazy Loading?
- A design pattern that defers loading of non-critical resources until they are actually needed
- Reduces initial page load time, bandwidth usage, and memory consumption
- Opposite of eager loading (loading everything upfront)
- Improves perceived performance — user sees content faster

### Image Lazy Loading
- **Native `loading="lazy"`** — built into modern browsers (Chrome 76+, Firefox 75+, Edge 79+)
  - `<img src="photo.jpg" loading="lazy" alt="Photo" />`
  - Browser decides when to load based on scroll position and viewport distance
  - No JavaScript required
  - Always include `width` and `height` to prevent layout shift (CLS)
- **`loading="eager"`** — default behavior, loads immediately (use for above-the-fold images)
- **Placeholder strategies:**
  - Low-quality image placeholder (LQIP) — tiny blurred version shown first
  - Solid color placeholder matching image's dominant color
  - Skeleton/shimmer animation

### Intersection Observer API
- Modern browser API to detect when elements enter or leave the viewport
- Replaces old scroll event listener approach (which was expensive and janky)
- **How it works:**
  - Create an observer with a callback function
  - Observe target elements
  - Callback fires when target enters/exits viewport (or a defined root)
  - `entry.isIntersecting` — true when element is visible
  - `observer.unobserve(element)` — stop watching after loaded
- **Configuration options:**
  - `root` — scrollable ancestor (null = viewport)
  - `rootMargin` — margin around root ("100px" = start loading 100px before visible)
  - `threshold` — how much of element must be visible (0 = any pixel, 1 = fully visible)
- **Use cases beyond images:**
  - Infinite scroll (load more items when user reaches bottom)
  - Animate elements on scroll
  - Track ad impressions / visibility analytics

### JavaScript Code Splitting
- **Static import** — `import { fn } from './module'` — bundled together, loaded upfront
- **Dynamic import** — `import('./module')` — returns a Promise, loaded on demand
- **Route-based splitting** — load each page's code only when user navigates there
- **Component-based splitting** — load heavy components (charts, editors) only when rendered
- **Vendor splitting** — separate third-party libraries into their own bundle (cached separately)
- **Webpack magic comments:**
  - `import(/* webpackChunkName: "dashboard" */ './Dashboard')` — names the chunk
  - `import(/* webpackPrefetch: true */ './Dashboard')` — prefetch in idle time

### React Lazy Loading
- **`React.lazy()`** — lazily loads a component; takes a function returning dynamic `import()`
- **`<Suspense>`** — wrapper that shows fallback UI while lazy component loads
- **Works with React Router** — lazy load route components for automatic code splitting
- **Limitations:** React.lazy currently only supports default exports
- **Error boundaries** — wrap Suspense with ErrorBoundary to handle load failures

### What to Lazy Load
- Images below the fold (not visible on initial viewport)
- Heavy JavaScript modules (chart libraries, rich text editors, PDF viewers)
- Route components (each page loads its own bundle)
- Third-party widgets (chat widgets, social media embeds)
- Videos and iframes (`<iframe loading="lazy">`)
- Comments section (load on scroll)

### What NOT to Lazy Load
- Above-the-fold images (hero images, logos) — these should load immediately
- Critical CSS and fonts — needed for first paint
- Core application logic — needed for interactivity
- SEO-critical content — search engines may not execute lazy loading JS

---

## 3. Security (Frontend)

### XSS (Cross-Site Scripting)
- **What:** Attacker injects malicious scripts into a web page viewed by other users
- **Impact:** steal cookies/tokens, redirect users, deface website, keylogging, session hijacking
- **Three types:**
  - **Stored XSS** — malicious script saved in database (e.g., a comment), served to every user who views it
  - **Reflected XSS** — script in URL parameters, reflected back in server response (e.g., search results)
  - **DOM-based XSS** — client-side JS inserts untrusted data into DOM without sanitization
- **Common vulnerable points:**
  - `innerHTML` — interprets string as HTML, executes `<script>` or event handlers
  - `document.write()` — writes raw HTML to document
  - `eval()` — executes arbitrary JavaScript code
  - `outerHTML`, `insertAdjacentHTML` — same risk as innerHTML
  - URL parameters injected into page without encoding
- **Prevention:**
  - Use `textContent` instead of `innerHTML` for displaying user text
  - Sanitize HTML input with libraries like DOMPurify
  - Encode output: `&lt;` instead of `<`, `&amp;` instead of `&`
  - Content Security Policy (CSP) header — restricts which scripts can execute
  - Validate and whitelist input on both client and server
  - Use template literals carefully — never insert user input into HTML strings
  - HttpOnly cookies — prevents JavaScript from accessing session cookies

### CSRF (Cross-Site Request Forgery)
- **What:** Attacker tricks authenticated user into submitting unintended requests
- **How:** User is logged into bank.com; visits attacker.com which has hidden form that POSTs to bank.com/transfer
- **Browser sends cookies automatically** — bank.com thinks the request is legitimate
- **Prevention:**
  - **CSRF tokens** — unique random token per session/form; server validates it on every state-changing request
  - **SameSite cookie attribute:**
    - `Strict` — cookie never sent on cross-site requests
    - `Lax` — cookie sent on top-level navigations (GET only), not on POST/iframe/AJAX
    - `None` — cookie sent on all cross-site requests (requires `Secure` flag)
  - **Double-submit cookie pattern** — send token in both cookie and request body; server compares
  - **Check Referer/Origin header** — verify request originates from your own domain

### Dangerous JavaScript Patterns
- **`eval(userInput)`** — executes arbitrary code; never use with user input
- **`innerHTML = userInput`** — XSS vector; use `textContent` for plain text
- **`document.write()`** — blocks parsing, can overwrite entire page; avoid entirely
- **`new Function(userInput)`** — similar to eval; creates function from string
- **`setTimeout(userString, 1000)`** — if string form is used, acts like eval
- **`window.location = userInput`** — open redirect vulnerability
- **`<a href="javascript:...">`** — can execute JS; sanitize href attributes

### CORS (Cross-Origin Resource Sharing)
- **Same-Origin Policy** — browser blocks requests from one origin to a different origin
- **Origin** = protocol + domain + port (e.g., `https://example.com:443`)
- **CORS headers** — server explicitly allows specific origins to access its resources
  - `Access-Control-Allow-Origin: https://myapp.com` — allows this specific origin
  - `Access-Control-Allow-Methods: GET, POST, PUT` — allowed HTTP methods
  - `Access-Control-Allow-Headers: Content-Type, Authorization` — allowed request headers
  - `Access-Control-Allow-Credentials: true` — allows cookies to be sent
- **Preflight request** — browser sends OPTIONS request first for non-simple requests (PUT, DELETE, custom headers)
- **Common error:** "No 'Access-Control-Allow-Origin' header" — server needs to add CORS headers
- **Never use `Access-Control-Allow-Origin: *` with credentials** — security risk

### HTTPS
- **What:** HTTP over TLS/SSL — encrypts data between browser and server
- **Prevents:**
  - Man-in-the-middle attacks (eavesdropping on data in transit)
  - Data tampering (modifying content between server and browser)
  - Impersonation (fake server pretending to be legitimate)
- **Required for:** service workers, geolocation API, camera/microphone access, HTTP/2
- **Mixed content** — HTTPS page loading HTTP resources is blocked by browsers
- **HSTS (HTTP Strict Transport Security)** — forces browsers to always use HTTPS

### Cookie Security Flags
- **`HttpOnly`** — cookie inaccessible to JavaScript (`document.cookie` won't show it); prevents XSS cookie theft
- **`Secure`** — cookie only sent over HTTPS connections
- **`SameSite`** — controls when cookie is sent on cross-site requests (Strict/Lax/None)
- **`Domain`** — limits which domains receive the cookie
- **`Path`** — limits which URL paths receive the cookie
- **`Max-Age` / `Expires`** — controls cookie lifetime; session cookies are deleted when browser closes

### Content Security Policy (CSP)
- HTTP response header that controls which resources the browser is allowed to load
- `script-src 'self'` — only allow scripts from same origin (blocks inline scripts, eval)
- `style-src 'self' 'unsafe-inline'` — allow same-origin styles and inline styles
- `img-src 'self' https://cdn.example.com` — allow images from self and specific CDN
- `default-src 'none'` — block everything by default; whitelist explicitly
- **Report-only mode** — `Content-Security-Policy-Report-Only` logs violations without blocking

### Input Validation
- **Client-side validation** — provides fast feedback to user; NOT a security measure (easily bypassed)
- **Server-side validation** — the real security boundary; validate, sanitize, escape on the server
- **Whitelist approach** — define what IS allowed rather than what is NOT (more secure)
- **Validate:** data type, length, range, format (regex), allowed characters
- **Sanitize:** remove/encode dangerous characters before processing or storing
- **Escape:** encode output based on context (HTML, URL, JavaScript, CSS)

### Frontend Security Checklist
- [ ] Escape/sanitize all user input before rendering in DOM
- [ ] Use `textContent` not `innerHTML` for displaying user-generated text
- [ ] Set Content Security Policy (CSP) headers
- [ ] Use `HttpOnly`, `Secure`, `SameSite` on all cookies
- [ ] Validate input on both client AND server sides
- [ ] Use HTTPS everywhere; enable HSTS
- [ ] Keep npm dependencies updated; run `npm audit` regularly
- [ ] Never store sensitive data (passwords, tokens) in localStorage
- [ ] Avoid `eval()`, `document.write()`, `innerHTML` with dynamic data
- [ ] Implement CORS properly on the server; don't use `*` with credentials
- [ ] Use Subresource Integrity (SRI) for CDN scripts
- [ ] Sanitize URL parameters before using in DOM or redirects

---

## 4. Logging & Monitoring

### Console Logging Methods
- **`console.log()`** — general purpose logging; used for debugging during development
- **`console.info()`** — informational messages; semantically similar to log
- **`console.warn()`** — warning messages; displayed in yellow in browser console
- **`console.error()`** — error messages; displayed in red with stack trace
- **`console.debug()`** — verbose debug info; hidden by default in most browsers (must enable "Verbose" level)
- **`console.table()`** — displays arrays/objects as a sortable table; great for data inspection
- **`console.group()` / `console.groupEnd()`** — groups related logs under a collapsible header
- **`console.groupCollapsed()`** — same as group but starts collapsed
- **`console.time()` / `console.timeEnd()`** — measures execution time between start and end
- **`console.count()`** — counts how many times it's been called with a given label
- **`console.assert(condition, message)`** — logs message only when condition is false
- **`console.trace()`** — prints the full call stack at the point of invocation
- **`console.dir()`** — displays an interactive view of a JavaScript object (useful for DOM elements)
- **`console.clear()`** — clears the console

### Structured Logging Best Practices
- **Include context** — always log what operation was attempted, not just that it failed
- **Use consistent format** — structured JSON logs are easier to search and filter
- **Log levels matter:**
  - `debug` — verbose development-only info (variable values, flow tracing)
  - `info` — normal operations (user logged in, page loaded, API called)
  - `warn` — something unexpected but not breaking (deprecated API, slow response)
  - `error` — something failed and needs attention (API error, unhandled exception)
- **Include identifiers** — user ID, session ID, request ID for traceability
- **Include timestamps** — `new Date().toISOString()` for consistent time format
- **Never log sensitive data** — passwords, credit card numbers, tokens, PII (personal identifiable information)

### Browser DevTools for Monitoring
- **Console panel** — view logs, errors, warnings; filter by level; execute JavaScript
- **Network panel:**
  - Inspect every HTTP request (URL, method, status code, timing, size)
  - View request/response headers and body
  - Filter by type: XHR, JS, CSS, Img, Media, Font, WS (WebSocket)
  - Throttle network speed (3G, offline) to test slow connections
  - Check waterfall chart for bottlenecks
  - Look for red entries (failed requests) and large payloads
- **Performance panel:**
  - Record runtime performance; analyze frame by frame
  - Identify long tasks (> 50ms blocks main thread)
  - Spot layout thrashing (forced reflows)
  - Check frames per second (target: 60fps)
  - Memory usage over time (detect memory leaks)
- **Lighthouse panel:**
  - Automated audits for Performance, Accessibility, Best Practices, SEO, PWA
  - Provides actionable recommendations with priority
  - Generates a score (0-100) for each category
- **Application panel:**
  - Inspect localStorage, sessionStorage, cookies, IndexedDB
  - View and debug service workers
  - Check cache storage contents
  - Manage permissions

### Global Error Handling
- **`window.onerror`** — catches all unhandled JavaScript errors
  - Receives: message, source URL, line number, column number, error object
  - Return `true` to prevent default browser error logging
- **`window.addEventListener("error", handler)`** — alternative to onerror; also catches resource load failures (images, scripts)
- **`window.addEventListener("unhandledrejection", handler)`** — catches unhandled Promise rejections
  - Critical: unhandled rejections crash Node.js and cause silent failures in browsers
  - `event.reason` contains the rejection reason (usually an Error object)
- **Error Boundaries (React)** — class components that catch errors in child component tree
  - `componentDidCatch(error, errorInfo)` — log error details
  - `static getDerivedStateFromError(error)` — render fallback UI

### Performance Monitoring APIs
- **Navigation Timing API** — detailed metrics for page load phases (DNS, TCP, request, response, DOM parsing)
- **Resource Timing API** — timing for every resource (scripts, stylesheets, images, fonts, XHR)
- **User Timing API** — custom marks and measures for application-specific operations
  - `performance.mark("operation-start")` — create a timestamp marker
  - `performance.mark("operation-end")` — create another marker
  - `performance.measure("operation", "operation-start", "operation-end")` — measure duration
- **PerformanceObserver** — observe specific entry types in real-time
  - `longtask` — detects tasks blocking main thread for > 50ms
  - `largest-contentful-paint` — tracks LCP for Core Web Vitals
  - `layout-shift` — tracks CLS for Core Web Vitals
  - `first-input` — tracks FID for Core Web Vitals
- **`navigator.sendBeacon(url, data)`** — reliable way to send analytics data
  - Works even during page unload (unlike fetch/XHR which may be cancelled)
  - Non-blocking; doesn't delay page navigation
  - Ideal for sending final analytics/log batch before user leaves

### Production Monitoring Tools
- **Sentry** — error tracking with stack traces, breadcrumbs (user actions before error), release tracking
- **LogRocket** — session replay (video of user's session), console logs, network requests, Redux state
- **Datadog RUM (Real User Monitoring)** — performance metrics from real users, error tracking, user journeys
- **New Relic Browser** — real user monitoring, JavaScript error analytics, AJAX monitoring
- **Google Analytics** — user behavior, page views, bounce rates, conversions, demographics
- **Lighthouse CI** — automated Lighthouse audits in CI/CD pipeline; fail builds if performance drops
- **Web Vitals library** — Google's official JS library to measure Core Web Vitals in the field

### Logging vs Monitoring vs Alerting
- **Logging** — recording events as they happen (what happened, when, where)
- **Monitoring** — continuously observing system health using dashboards and metrics (is it healthy?)
- **Alerting** — automated notifications when metrics exceed thresholds (something is wrong, act now)
- **Best practice flow:** Log everything → Monitor key metrics → Alert on anomalies → Investigate using logs

### Monitoring Best Practices
- [ ] Use appropriate log levels; don't `console.error` for informational messages
- [ ] Include contextual data: user ID, session ID, URL, timestamp, browser info
- [ ] Never log sensitive data (passwords, tokens, credit card numbers, PII)
- [ ] Set up global error handlers for both sync errors and unhandled promise rejections
- [ ] Monitor Core Web Vitals (LCP, FID, CLS) with real user data
- [ ] Use `navigator.sendBeacon()` for reliable analytics delivery on page unload
- [ ] Set up alerts for error rate spikes (e.g., error rate > 5% in 5 minutes)
- [ ] Track API response times and failure rates from the frontend
- [ ] Remove excessive `console.log` before deploying to production
- [ ] Use source maps in production error tracking (upload to Sentry/etc.) for readable stack traces
- [ ] Monitor bundle sizes to catch unexpected growth
- [ ] Review and rotate logs to manage storage costs

---

## Quick Reference Card

| Topic | Key Takeaway |
|-------|-------------|
| Page Load | Minimize critical rendering path; use `defer`, compress, cache, CDN |
| Lazy Loading | Load on demand; `loading="lazy"`, Intersection Observer, dynamic `import()` |
| Security | Never trust user input; sanitize, escape, use CSP, HTTPS, HttpOnly cookies |
| Logging | Structured logs with context; global error handlers; monitor Core Web Vitals |
