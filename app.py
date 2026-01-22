from flask import Flask, render_template, abort, redirect, url_for
import datetime

from posts import S3ContentProvider

app = Flask(__name__)
provider = S3ContentProvider()


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
