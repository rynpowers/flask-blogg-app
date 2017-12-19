from flask import Flask, render_template, request, g, redirect
import sqlite3

app = Flask(__name__)

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

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        photo = request.form['photo']
        title = request.form['title']
        about = request.form['about']

        db = get_db()
        db.execute('''
        insert into blog (first_name, last_name, photo, blog_title, about_blog)
            values (?, ?, ?, ?, ?)
        ''', [first_name, last_name, photo, title, about])
        db.commit()

        return redirect('profile')

    return render_template('settings.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():

    db = get_db()

    if request.method == 'POST':
        blog_id = request.form['blog_id']
        post_title = request.form['title']
        post_date = request.form['date']
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

    if request.method == 'GET':
        post_id = request.args.get('post_id')
        db.execute('delete from posts where id = ?',[post_id])

    if request.method == 'POST':
        post_id = request.form['post_id']
        blog_id = request.form['blog_id']
        post_title = request.form['title']
        post_date = request.form['date']
        post = request.form['blog-post']

        db.execute('delete from posts where id = ?',[post_id])
        db.execute(
        '''
        insert into posts (id, blog_id, post_date, post_title, post)
            values (?, ?, ?, ?, ?)
        ''', [post_id, blog_id, post_date, post_title, post])

    db.commit()

    return redirect('profile')




if __name__ == '__main__':
    app.run(debug=True)
