from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

app.secret_key = 'secretkey'

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(800))

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def __repr__(self):
        return '<Blog %r>' % self.title


@app.route("/blog", methods=['POST', 'GET'])
def display_blog():
    #needs to receive info from new_post
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_post = Blog(title, body)
        db.session.add(new_post)
        db.session.commit()

        all_posts = Blog.query.all()
        last_post = all_posts[-1]
        if new_post == last_post:
            return redirect ('/post_display?id=' + str(new_post.id))
       
    if request.method == 'GET':
   
            all_posts = Blog.query.all()
            return render_template("blog.html", all_posts=all_posts)
        


@app.route("/new_post", methods=['POST', 'GET'])
def create_new_post():
    error = request.args.get('error')
    blog_title = request.args.get('blog_title')
    blog_body = request.args.get('blog_body')
    if error:
        error = error
        blog_title = blog_title
        blog_body = blog_body
    else:
        error = ''
        blog_title = ''
        blog_body = ''
   
    return render_template("new_post.html", error=error, blog_title=blog_title, blog_body=blog_body)

@app.route("/post_display", methods=['POST', 'GET'])
def display_post(): 
    id = request.args.get('id')
    
    blog = Blog.query.get(id)
    blog_title = blog.title
    blog_body = blog.body
    #NEED TO ADD A CREATION DATE/TIME ATTRIBUTE AND ORDER IT IN /BLOG
    if blog_title == '' or blog_body == '':
        error = 'Text fields cannot be left blank'

        return redirect('/new_post?error=' + error + '&blog_title=' + blog_title + '&blog_body=' + blog_body)

    return render_template("post_display.html", blog_title=blog_title, blog_body=blog_body)

if __name__ == '__main__':
    app.run()