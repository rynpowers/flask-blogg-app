from flask import Flask, render_template, request, g, redirect
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
import datetime
import sqlite3

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

def connect_db():
    sql = sqlite3.connect('/Users/hillarywoolley/codingdocs/flaskcourse/blogapp/database.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite3_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite3_db'):
        g.sqlite_db.close()

@app.route('/create_profile', methods=['GET', 'POST'])
def create_profile():

    if request.method == 'POST' and 'photo' in request.files:
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        photo = photos.save(request.files['photo'])
        title = request.form['title']
        about = request.form['about']

        db = get_db()
        db.execute('''
        insert into blog (first_name, last_name, photo, blog_title, about_blog)
            values (?, ?, ?, ?, ?)
        ''', [first_name, last_name, photo, title, about])
        db.commit()

        return redirect('profile')

    return render_template('create_profile.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():

    db = get_db()
    now = datetime.datetime.now()

    if request.method == 'POST':
        blog_id = request.form['blog_id']
        post_title = request.form['title']
        post_date = now.strftime("%B %d, %Y")
        post = request.form['blog-post']

        db.execute('''
        insert into posts (blog_id, post_date, post_title, post)
            values (?, ?, ?, ?)''', [blog_id, post_date, post_title, post])
        db.commit()

    settings_cur = db.execute('select * from blog where id = 1')
    settings_results = settings_cur.fetchone()
    posts_cur = db.execute('select * from posts where blog_id = 1 order by id desc')
    posts_results = posts_cur.fetchall()

    return render_template('profile.html', results=settings_results, posts=posts_results)

@app.route('/blog')
def blog():

    db = get_db()

    settings_cur = db.execute('select * from blog where id = 1')
    settings_results = settings_cur.fetchone()
    posts_cur = db.execute('select * from posts where blog_id = 1 order by id desc')
    posts_results = posts_cur.fetchall()

    return render_template('blog.html', results=settings_results, posts=posts_results)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    db = get_db()

    if request.method == 'POST':
        post_id = request.form['post_id']

        cur = db.execute('select * from posts where id = ?', [post_id])
        results = cur.fetchone()

    return render_template('edit.html', results=results)

@app.route('/update', methods=['GET', 'POST'])
def update():
    db = get_db()

    post_id = request.form['post_id']
    db.execute('delete from posts where id = ?',[post_id])

    if 'edit' in request.form:
        blog_id = request.form['blog_id']
        post_title = request.form['title']
        post_date = request.form['date']
        post = request.form['blog-post']

        db.execute(
        '''
        insert into posts (id, blog_id, post_date, post_title, post)
            values (?, ?, ?, ?, ?)
        ''', [post_id, blog_id, post_date, post_title, post])

    db.commit()

    return redirect('profile')

if __name__ == '__main__':
    app.run(debug=True)
