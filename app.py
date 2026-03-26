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
 
    csp = (
        "default-src 'self'; "
        "style-src 'self' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "form-action 'self'; "
        "frame-ancestors 'self'; "
        "base-uri 'self';"
    )
    response.headers['Content-Security-Policy'] = csp

    response.headers['X-Frame-Options'] = 'SAMEORIGIN'

    response.headers['X-Content-Type-Options'] = 'nosniff'

    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

    response.headers['Permissions-Policy'] = "geolocation=(), microphone=(), camera=()"

    response.headers['Cross-Origin-Resource-Policy'] = 'same-origin'

    response.headers['Cross-Origin-Embedder-Policy'] = 'credentialless'
    
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'

    return response

@app.errorhandler(500)
def internal_server_error(e):
    return "500 Internal Server Error: Something went wrong.", 500


@app.errorhandler(404)
def page_not_found(e):
    return "404 Page Not Found", 404



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
    return render_template("about.html")


@app.route("/contact")
def contact_page():
    return render_template("contact.html")


@app.route("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)