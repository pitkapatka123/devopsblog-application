from flask import Flask, render_template, abort, redirect, url_for
import datetime

from posts import S3ContentProvider

app = Flask(__name__)
provider = S3ContentProvider()


# --- START OF SECURITY FIXES ---

@app.after_request
def add_security_headers(response):
    """
    Add security headers to every response to fix ZAP alerts.
    """
    # Fix: Content Security Policy (CSP) Header Not Set 
    # Restricts resources (scripts, styles, images) to the same origin ('self').
    response.headers['Content-Security-Policy'] = "default-src 'self'"

    # Fix: Strict-Transport-Security Header Not Set 
    # Enforces HTTPS for one year (31536000 seconds) including subdomains.
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

    # Fix: Missing Anti-clickjacking Header 
    # Prevents the site from being embedded in iframes on other sites.
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'

    # Fix: X-Content-Type-Options Header Missing 
    # Prevents the browser from MIME-sniffing a response away from the declared content-type.
    response.headers['X-Content-Type-Options'] = 'nosniff'

    # Fix: Permissions Policy Header Not Set 
    # Explicitly disables sensitive features like geolocation and microphone.
    response.headers['Permissions-Policy'] = "geolocation=(), microphone=(), camera=()"

    # Fix: Insufficient Site Isolation Against Spectre Vulnerability 
    # Restricts who can load this resource to the same origin.
    response.headers['Cross-Origin-Resource-Policy'] = 'same-origin'

    return response


@app.errorhandler(500)
def internal_server_error(e):
    # Fix: Application Error Disclosure  & Information Disclosure - Debug Error Messages [cite: 60]
    # Returns a generic error message instead of a stack trace or default server page.
    return "500 Internal Server Error: Something went wrong.", 500


@app.errorhandler(404)
def page_not_found(e):
    # Good practice: Handle 404s cleanly.
    return "404 Page Not Found", 404

# --- END OF SECURITY FIXES ---


def _date_sort_key(p):
    v = p.meta.get("date")
    if isinstance(v, datetime.date):
        return v
    if isinstance(v, str):
        try:
            return datetime.date.fromisoformat(v)
        except ValueError:
            return datetime.date.min
    return datetime.date.min


@app.route("/")
def index():
    return redirect(url_for("list_posts"))


@app.route("/posts")
def list_posts():
    posts = provider.list_posts()
    posts.sort(key=_date_sort_key, reverse=True)
    return render_template("posts.html", posts=posts)


@app.route("/post/<slug>")
def post_detail(slug):
    post = provider.get_post(slug)
    if not post:
        abort(404)
    return render_template("post_detail.html", post=post)


@app.route("/about")
def about_page():
    page = provider.get_page("about")
    if not page:
        abort(404)
    return render_template("page.html", page=page)


@app.route("/contact")
def contact_page():
    page = provider.get_page("contact")
    if not page:
        abort(404)
    return render_template("page.html", page=page)


@app.route("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)