from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:beproductive@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "abc123"


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    #completed = db.Column(db.Boolean)

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/blogpost')
def get_blogpost():

    blog_id = request.args.get("id")
    blog = Blog.query.get(int(blog_id))
    return render_template('blog_post.html', blog=blog)

"""
return redirect("/welcome?username=" + username)
            #return render_template('welcome.html', username=username)

@app.route("/welcome")
def welcome():
        username = request.args['username']
        return render_template('welcome.html', username=username)
"""


@app.route('/blog', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_title = request.form['blog']
        if blog_title == "":
            flash("Please, fill in the field", "error_title")
            return redirect("/newpost")
        blog_body = request.form['body']
        if blog_body == "":
            flash("Please, fill in the field", "error_body")
            return redirect("/newpost")
        new_blog = Blog(blog_title,blog_body)
        db.session.add(new_blog)
        db.session.commit()
        id_new = str(new_blog.id)
        return redirect("/blogpost?id=" + id_new)

    blogs = Blog.query.all()
    return render_template('blog-main.html', blogs=blogs)

@app.route("/newpost")
def post_newpost():

    return render_template("newpost.html")

@app.route("/")
def home_redirect():

    return redirect("/blog")

if __name__ == '__main__':
    app.run()

