# OWASP ZAP Security Scan Remediation Plan

This document outlines a structured plan to address the security findings from the OWASP ZAP scan report, broken down into manageable Pull Requests.

## **CRITICAL FINDING: Security Headers Not Applied in Production**

⚠️ **UPDATE (2026-02-05):** The ZAP scan reveals that despite security headers being implemented in the codebase (PR #29), **they are NOT being applied on the production website**.

**Root Cause:** PR #29 was merged but **NOT deployed to production**. The deployment workflow only runs on pushes to the `main` branch, and the security headers code has not reached `main` yet.

**Evidence from ZAP Scan:**
- Server header leaks version: "Werkzeug/3.1.5 Python/3.11.14" 
- No CSP header returned
- No X-Frame-Options returned
- No X-Content-Type-Options returned
- No HSTS returned
- No Permissions-Policy returned
- Session cookies missing Secure flag and SameSite attribute

**Immediate Action Required:** Ensure PR #29 changes are merged to `main` branch and deployed to production before addressing other issues.

## Scan Summary

The OWASP ZAP scan identified multiple security issues across the website. The security headers were implemented in PR #29 but have not yet been deployed to production.

## Status of Security Issues

### ✅ Already Fixed (PR #29: Security Headers & Cookie Protection)

The following issues have been resolved through the implementation of security headers in `app.py`:

1. **Content Security Policy (CSP) Header Not Set** ✅
   - Status: FIXED
   - Implementation: CSP header added in `add_security_headers` middleware
   - Location: app.py lines 47-59

2. **Missing Anti-clickjacking Header** ✅
   - Status: FIXED
   - Implementation: X-Frame-Options set to 'SAMEORIGIN'
   - Location: app.py line 62

3. **X-Content-Type-Options Header Missing** ✅
   - Status: FIXED
   - Implementation: X-Content-Type-Options set to 'nosniff'
   - Location: app.py line 65

4. **Strict-Transport-Security Header Not Set** ✅
   - Status: FIXED
   - Implementation: HSTS header with 1-year max-age
   - Location: app.py line 68

5. **Permissions Policy Header Not Set** ✅
   - Status: FIXED
   - Implementation: Permissions-Policy header added
   - Location: app.py line 71

6. **Server Leaks Version Information** ✅
   - Status: FIXED
   - Implementation: Server header removed from responses
   - Location: app.py line 79

7. **Insufficient Site Isolation Against Spectre Vulnerability** ✅
   - Status: FIXED
   - Implementation: Cross-Origin policies added
   - Location: app.py lines 74-76

8. **Cookie Without Secure Flag** ✅
   - Status: FIXED
   - Implementation: SESSION_COOKIE_SECURE configured
   - Location: app.py line 36

9. **Cookie without SameSite Attribute** ✅
   - Status: FIXED
   - Implementation: SESSION_COOKIE_SAMESITE set to 'Lax'
   - Location: app.py line 38

## Remaining Issues to Address

### 🔴 High Priority Issues

#### PR #2: Subresource Integrity (SRI) Implementation
**Issue**: Sub Resource Integrity Attribute Missing [90003]
**Risk Level**: Medium
**Effort**: Low
**Files Affected**: `templates/base.html`

**Description**: External resources from CDNs (Bootstrap, Font Awesome, Google Fonts) lack integrity attributes, making the site vulnerable to CDN compromise.

**Tasks**:
- [ ] Add SRI hashes to Bootstrap CSS and JS
- [ ] Add SRI hashes to Font Awesome CSS
- [ ] Add crossorigin="anonymous" attributes
- [ ] Document how to update SRI hashes when upgrading libraries
- [ ] Test that all resources load correctly with SRI

**Implementation Details**:
```html
<!-- Example with SRI -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" 
      rel="stylesheet" 
      integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" 
      crossorigin="anonymous">
```

**Note**: Google Fonts don't support SRI as they dynamically generate CSS. Consider self-hosting fonts or accepting this limitation.

#### PR #3: Code Comments Cleanup
**Issue**: Information Disclosure - Suspicious Comments [10027]
**Risk Level**: Low
**Effort**: Low
**Files Affected**: `static/js/script.js`

**Description**: The JavaScript file contains comments that may reveal implementation details or TODO items.

**Tasks**:
- [ ] Review all comments in script.js
- [ ] Remove or rephrase comments that reveal sensitive implementation details
- [ ] Remove TODOs or move them to issue tracker
- [ ] Keep necessary documentation comments
- [ ] Verify functionality remains unchanged

### 🟡 Medium Priority Issues

#### PR #4: Cache Control Headers
**Issue**: Re-examine Cache-control Directives [10015]
**Risk Level**: Low-Medium
**Effort**: Medium
**Files Affected**: `app.py`

**Description**: Cache control headers need to be optimized for different types of content (static vs. dynamic, sensitive vs. public).

**Tasks**:
- [ ] Add route-specific cache headers for static assets
- [ ] Ensure no-cache for sensitive pages (login, register, cart, orders)
- [ ] Set appropriate max-age for public pages
- [ ] Add cache headers for API endpoints
- [ ] Test caching behavior in browser
- [ ] Document caching strategy

**Implementation Strategy**:
```python
@app.after_request
def add_cache_headers(response):
    if request.endpoint in ['login', 'register', 'cart', 'orders', 'admin']:
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, private'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    elif request.endpoint == 'static':
        response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
    return response
```

#### PR #5: Input Validation Enhancement
**Issue**: User Controllable HTML Element Attribute (Potential XSS) [10031]
**Risk Level**: Medium
**Effort**: Medium
**Files Affected**: `app.py`, form templates

**Description**: Form inputs on login/register pages may be vulnerable to XSS through user-controllable attributes.

**Tasks**:
- [ ] Review all form inputs for proper validation
- [ ] Ensure Flask-WTF CSRF protection is active on all forms
- [ ] Verify Jinja2 auto-escaping is enabled
- [ ] Add input sanitization where needed
- [ ] Test with XSS payloads
- [ ] Add CSP reporting endpoint to catch violations

**Areas to Review**:
- Login form inputs
- Registration form inputs
- Search functionality
- Product forms
- Any user-generated content display

### 🟢 Low Priority / Informational

#### PR #6: Documentation & Best Practices
**Issues**: 
- Base64 Disclosure [10094]
- Timestamp Disclosure - Unix [10096]
- Authentication Request Identified [10111]
- Session Management Response Identified [10112]
- Storable and Cacheable Content [10049]

**Risk Level**: Informational
**Effort**: Low
**Files Affected**: Documentation files

**Description**: These are mostly informational alerts that don't necessarily require code changes.

**Tasks**:
- [ ] Document why Base64 encoding is used (if in images or data URIs)
- [ ] Review if Unix timestamps expose sensitive information
- [ ] Document authentication and session management approach
- [ ] Create security documentation for future developers
- [ ] Add comments explaining security decisions

### ❌ Non-Issues (Browser-Controlled)

The following alerts are related to browser-sent headers and cannot be fixed server-side:
- **Sec-Fetch-Dest Header is Missing** [90005]
- **Sec-Fetch-Mode Header is Missing** [90005]
- **Sec-Fetch-Site Header is Missing** [90005]
- **Sec-Fetch-User Header is Missing** [90005]

**Action**: None required - these headers are sent by modern browsers automatically.

### Issues Requiring Investigation

#### Cross-Domain JavaScript Source File Inclusion [10017]
**Status**: Needs Review
**Files**: All templates using CDN resources

**Analysis**: This alert is related to using CDN-hosted libraries (Bootstrap, Font Awesome). This is a common and accepted practice when:
1. Using reputable CDNs
2. Implementing SRI (addressed in PR #2)
3. Using HTTPS
4. Having appropriate CSP policies (already implemented)

**Decision**: Accept as acceptable risk with SRI implementation.

## Implementation Timeline

### Phase 1: Critical Security Fixes (Week 1)
- PR #2: SRI Implementation

### Phase 2: Code Quality & Hardening (Week 2)
- PR #3: Code Comments Cleanup
- PR #4: Cache Control Headers

### Phase 3: Input Validation & XSS Prevention (Week 3)
- PR #5: Input Validation Enhancement

### Phase 4: Documentation & Polish (Week 4)
- PR #6: Documentation & Best Practices

## Testing Strategy

For each PR:
1. Manual testing of affected functionality
2. Re-run OWASP ZAP scan to verify fixes
3. Review browser console for CSP violations
4. Test in multiple browsers (Chrome, Firefox, Safari, Edge)
5. Verify no regressions in functionality

## Success Metrics

After all PRs are merged:
- [ ] All High severity issues resolved
- [ ] All Medium severity issues resolved
- [ ] Documentation complete
- [ ] Clean OWASP ZAP scan (only informational alerts remaining)
- [ ] No functionality regressions
- [ ] Security best practices documented

## Notes

- The application already has excellent security foundation from PR #29
- Focus should be on maintaining this security posture
- All changes should be minimal and targeted
- Preserve existing functionality
- Document all security decisions for future maintenance

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)
- [MDN Web Security](https://developer.mozilla.org/en-US/docs/Web/Security)
- [CSP Reference](https://content-security-policy.com/)
- [Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)
