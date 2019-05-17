from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:beproductive@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "abc123"


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


#copied from get-it-done !!!!
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship("Blog", backref="owner")

    def __init__(self, username, password):
        self.username = username
        self.password = password

##### Class definition ends here. ###########################################

@app.before_request
def require_login():

    allowed_routes = ["index", "get_blog_posts", "login", "signup", "index_blogs", "get_singleuser"]
    if request.endpoint not in allowed_routes and "username" not in session:
        return redirect("/login")



@app.route("/login", methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        # Checks if there's an user with those data.
        user = User.query.filter_by(username=username).first()
        if not user:
            flash("User does not exist", "error")
            return render_template("/login.html")
        if user and user.password == password:
            # TODO - remember that the user has logged in.
            session["username"] = username
            #flash("Logged in")
            return redirect("/newpost")
        else:
            # TODO - explain why login failed.
            flash("User password incorrect", "error")

    return render_template("/login.html")


@app.route("/signup", methods=['POST', 'GET'])
def signup():

    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        verify = request.form["verify"]

        # TODO - validate user's data !!
        if username is None or password is None or verify is None:
            flash("One or more fields are invalid", "error")
            return render_template("/signup.html")

        if len(username) < 3:
            flash("Invalid username", "error")
            return render_template("/signup.html")

        if len(password) < 3:
            flash("Invalid password", "error")
            return render_template("/signup.html")

        if password != verify:
            flash("Passwords do not match", "error")
            return render_template("/signup.html")

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists")
            return render_template("/signup.html")
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            # TODO - "remember" the user
            session["username"] = username
            return redirect("/newpost")
        else:
            # TODO = user better response messaging
            flash("Duplicate user", "error")
            return render_template("/signup.html")

    return render_template("/signup.html")


@app.route("/index")
def index():

    users = User.query.all()
    return render_template('index.html', users=users)

@app.route("/logout")
def logout():

    del session["username"]
    return redirect("/index")

@app.route("/blogposts")
def get_blog_posts():

    blog_id = request.args.get("id")
    if blog_id is not None:
        bloggy = Blog.query.get(int(blog_id))
        return render_template('blog_posts.html', blog=bloggy)
    else:
        blogs = Blog.query.all()
        return render_template('blog_posts.html', blogs=blogs)

@app.route('/blog', methods=['POST', 'GET'])
def index_blogs():

    if request.method == 'POST':
        blog_title = request.form['blog']
        if blog_title == "":
            flash("Please, fill in the title", "error_title")
            return redirect("/newpost")
        blog_body = request.form['body']
        if blog_body == "":
            flash("Please, fill in the body", "error_body")
            return redirect("/newpost")

        username = session["username"]
        blog_owner = User.query.filter_by(username=username).first()
        new_blog = Blog(blog_title,blog_body,blog_owner)
        db.session.add(new_blog)
        db.session.commit()
        id_new = str(new_blog.id)
        return redirect("/blog?id=" + id_new)

    #blogs = Blog.query.all()
    return redirect("/index")

# And think about what you'll need to do in your /newpost route handler function 
# since there is a new parameter to consider when creating a blog entry.
@app.route("/newpost")
def post_newpost():

    return render_template("newpost.html")

@app.route("/singleuser")
def get_singleuser():

    blogs = Blog.query.all()
    singleuser_id = int(request.args.get("id"))
    return render_template("singleUser.html", blogs=blogs, singleuser_id=singleuser_id)

@app.route("/")
def home_redirect():

    return redirect("/index")

if __name__ == '__main__':
    app.run()

