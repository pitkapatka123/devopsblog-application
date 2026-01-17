from flask import Flask, render_template, abort, redirect, url_for
from flask_flatpages import FlatPages
import datetime

app = Flask(__name__)

app.config['FLATPAGES_ROOT'] = 'content'         
app.config['FLATPAGES_EXTENSION'] = '.md'        
app.config['FLATPAGES_AUTO_RELOAD'] = True       
flatpages = FlatPages(app)

@app.route('/')
def index():

    return redirect(url_for('list_posts'))


@app.route('/posts')
def list_posts():

    posts = [p for p in flatpages if p.path.startswith('posts/')]

    posts.sort(key=lambda p: p.meta.get('date') or datetime.date.min, reverse=True)
    return render_template('posts.html', posts=posts)

@app.route('/post/<slug>')
def post_detail(slug):

    page = flatpages.get(f'posts/{slug}')
    if not page:
        abort(404)
    return render_template('post_detail.html', post=page)


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

@app.route('/health')
def health():
    return {"status": "ok"}, 200

if __name__ == '__main__':
    app.run(debug=True)
