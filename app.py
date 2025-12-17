from flask import Flask, render_template, abort, redirect, url_for
from flask_flatpages import FlatPages

app = Flask(__name__)
# Configuration for Flask-FlatPages
app.config['FLATPAGES_ROOT'] = 'content'         # Markdown files directory (relative to app)
app.config['FLATPAGES_EXTENSION'] = '.md'        # File extension for markdown files:contentReference[oaicite:2]{index=2}
app.config['FLATPAGES_AUTO_RELOAD'] = True       # Auto-reload pages in development
flatpages = FlatPages(app)

# Home page route - redirects to the posts listing for simplicity
@app.route('/')
def index():
    # Redirect to the posts listing page
    return redirect(url_for('list_posts'))

# Posts list route - lists all blog posts
@app.route('/posts')
def list_posts():
    # Filter FlatPages to get only those in the "posts/" subdirectory
    posts = [p for p in flatpages if p.path.startswith('posts/')]
    # Sort posts by date (assuming 'date' metadata is in YYYY-MM-DD format)
    posts.sort(key=lambda p: p.meta.get('date', ''), reverse=True)
    return render_template('posts.html', posts=posts)

# Post detail route - displays a single post identified by slug
@app.route('/post/<slug>')
def post_detail(slug):
    # Each post's path in FlatPages is "posts/<slug>"
    page = flatpages.get(f'posts/{slug}')
    if not page:
        abort(404)
    return render_template('post_detail.html', post=page)

# Static page routes (e.g. About, Contact)
@app.route('/about')
def about_page():
    page = flatpages.get('about')
    if not page:
        abort(404)
    return render_template('page.html', page=page)

@app.route('/contact')
def contact_page():
    page = flatpages.get('contact')
    if not page:
        abort(404)
    return render_template('page.html', page=page)

# Run the Flask development server for testing (not used in production with Gunicorn)
if __name__ == '__main__':
    app.run(debug=True)
