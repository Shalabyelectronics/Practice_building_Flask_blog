# Practice building Flask blog
We are going to explain very important topics with this day 69 from [100 days of code: The complete python BootCamp by D.Angela Yu](https://www.udemy.com/course/100-days-of-code/) milestone project where we will practice protecting routes from anonymous users, building relationships between tables and using Gravatar.

**First** before you start install the requirements framework and all tools you need to get an overview about what we are going to focus on with this practice?

Lets check this gif that gave you a quick overview for our end goal.

![quick_overview_3](https://user-images.githubusercontent.com/57592040/169954833-0e4eec7e-12e9-42d7-b3ec-7db7a9cfba20.gif)


As you see it is cool right, but behind the sine there are a lot of works you have to do, so make a cup of coffee and get ready.

## **First Step** _ Get Familiar with The tasks.

When you start anything in life you need first to discover what do you up to? and what tools do you going to use to achieve all tasks that related to this project?

## [Task number 1 : Register New users](#task-1)

That mean we need to do 4 steps as the rest are already set to us when downloading the starter project file:

**step 1:** Create a Register Form by using Flask WTForm 

**step 2:** Create a `/register` endpoint with the register route that will render our register template web page.

**step 3:** Use Flask-Bootstrap to render a wtf quick_form.

**step 4:** Use the User table to add registered users to blog database.

**Step 5:** When the user is registered we will hide the login and register button and show the logout button.

**Step 6:** Redirect the User to the home page

## [Task number 2 : Login Registered Users](#task-2)

After we are done from register route and it functionality now we need to login our users by their email and password as well and to do so you need to do another 6 steps:

**Step 1 :** Create a login Form that include the email, password and submit button.

**Step 2:** Use Flask-Bootstrap to render a wtf quick_form.

**Step 3:** Search if the user email exist in User table if yes check then if the password is match.

**Step 4:** Use `login_user` Method from Flask_login tool to login your user.

**step 5 and step 6 will be the same when the user logged in as above task number 1**

### [Task number 3: Logout The User](#task-3)

Now we need to add a logout route that will logout the user from the session and we have just 3 steps here.

**Step 1:** Use the `logout_user` from Flask_login tool 

**Step 2:** Return the login and register button back to the navbar and hide the logout button.

**Step 3:** Redirect the User to the home page.

### [Task number 4: Protect Routes](#task-4)

Now we will protect our administrator routes and it is `add_new_post`, `edit_post` and `delete_post`, and here you need 4 steps to achieve this task:

**Step 1:** We need the user who's id equal to 1 to become an admin so only him can `add_new_post`, `edit_post` and `delete_post`.

**Step 2:** We need to edit our home page and post page that will control showing the control button only for and admin and hide them from any other users.

**Step 3:** Even we hide the control buttons from the normal users Still they can use the routes end points to reach the control routes, So we need here to protect them (Routes) by customize our only_admin decorator.

**Step 4:** We need to combine `login_required` and `admin_only ` decorators so we can control the situation where if any anonymous user try to reach any of control routes first it will ask that user to log in by using `login_required` then we need to check if that user is an admin or not by `admin_only` decorator. 

### [Task number 5: Creating Relational Databases](#task-5)

Here we will take our experience with ORM or Object relational Mapping to the next stage we we need to figure out how to connect two or more table together by build a relationships between them, we need 2 steps and we are going gradually with these steps because we need to do some experiments until we reach the idle point where all functionalities are works as our expectations .

**Step 1:** We have a `User` table and `BlogPost` table and we want to make a relationship between this two table and it will be One-to-Many that mean one user can have many posts.

**Step 2:** We need to recreating our database after changes to the schema So we will delete the database and create it again.

### Task number 6: Allow Any User to Add Comments to BlogPosts

At this point we need to expand our web application by allow other users to comment to any blog posts, 

So we need to do 3 steps to achieve that:

**Step 1:** Create a comment table, where we are going to save all comments.

**Step 2:** Add a relationship between BlogPost table and comment table so each blog have it's own comments

**Step 3:** Add a relationship between User table and comment table so each user has many comments.

**Step 4:** Create a comment WtForm so we can add it underneath the post and the text filed have to be CKEditor

**Step 5:** recreate your database.

**Step 6:** Update the code in post.html to display all the comments associated with blog post.

### Task number 7: Add an image for each commenters by using Gravatar.

Gravatar is really a fun idea where we can convert an email to an image and use it to each user who comment underneath of the post, I like the idea and to know more about Gravatar you can check their documentation about it [here](https://pythonhosted.org/Flask-Gravatar/).

This task need need just one step that will add our app Flask instance to our Gravatar class and us that object in our post.html by using jinja

#### Lets start explaining each Tasks and it's steps 
# Task 1
**step 1:** Create a Register Form by using Flask WTForm

With the form.py create a new form and call it RegisterForm as below:

```python
class RegistrationForm(FlaskForm):
    username = StringField("User Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm password", validators=[EqualTo("password")])
    submit = SubmitField("Submit")
```

**step 2:** Create a `/register` endpoint with the register route that will render our register template register.html and we will pass our register form to the render_template method as below:

```python
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_existed = User.query.filter_by(email=form.email.data).first()
        if user_existed:
            flash("You've already signed up with that email, log in instead!.")
            return redirect(url_for("login"))
        else:
            user = User(username=form.username.data,
                        email=form.email.data,
                        password=generate_password_hash(form.password.data, "pbkdf2:sha256", 8))
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("get_all_posts"))
    return render_template("register.html", form=form)
```

**step 3:** Use Flask-Bootstrap to render a wtf quick_form. as below

```jinja2
{% import "bootstrap/wtf.html" as wtf %}
{{ wtf.quick_form(form, novalidate=True, button_map={"submit": "primary"}) }}
```

So first you need to import the wtf from `bootstrap/wtf.html` then add `wtf.quick_form` to the form location in the register.html, just take a look about it.

**step 4:** Use the User table to add registered users to blog database > That was explained in **Step 2**.

**Step 5:** When the user is registered we will hide the login and register button and show the logout button.

And this changes will happen in the header.html where the navbar includes the `login`,`register` and `logout` we will use `is_authenticated` attribute from `current_user` object as below.

```jinja2
{% if current_user.is_authenticated %}
            <li class="nav-item">
            <a class="nav-link" href="{{ url_for('logout') }}">Log Out</a>
          </li>
          {% else %}
          <li class="nav-item">
            <a class="nav-link" href="{{ url_for('login') }}">Login</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="{{ url_for('register') }}">Register</a>
          </li>
          {% endif %}
```

**Step 6:** Redirect the User to the home page > It mentioned in step 2 here our home page called get_all_post route and it's endpoint the the root `/`

# Task 2
**Step 1 :** Create a login Form that include the email, password and submit button, so here we are going to create another form as we did before with the register form and it will look like the code below:

```python
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Sign In")
```

**Step 2:** Use Flask-Bootstrap to render a wtf quick_form, here we will do the same as we did with adding the register form in our register.html with step 3.

and we will create the login route to get the data from the login form and check if the user email is existed in the database if yes then we will add that user to login session by using `login_user` method. so we combined all steps of task 2 together as login route below:

```python
@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get("next")
                return redirect(next_page) if next_page else redirect(url_for("get_all_posts"))
            else:
                flash("Login unsuccessful, please check your password.", "danger")
        else:
            flash("Login unsuccessful, please check your email.")
    return render_template("login.html", form=form)
```

Here I want to mention something interesting and it is when you try to reach any of pages that required login you will see that there is something additional appeared to your link bar as below:

![next_concept](https://user-images.githubusercontent.com/57592040/169966989-e60aace1-60ee-4e2b-97c9-c2a027950100.gif)

So the key `next ` will hold the endpoint as appeared `next=%2Fedit-post%2F1` here the endpoint is `/edit-post/1` So I checked first the next value by this code `next_page = request.args.get("next")` then if the next is not none it will redirect the user to that page.

# Task 3

Here we will use `logout_user` from Flask_login tool to logout the current user then redirect the user to the home page as below:

```python
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))
```

and regarding the step 2 where we need to show the login and register button instead of logout button we explained that within task 1 by using `is_authenticated` attribute from `current_user` object.

# Task 4

I think this very important task where we need to protect our sanative blog routes and they are `add_new_post`, `edit_post`, `delete_comment` and `delete_post`, so even we use the `current_user` object with `get_id()` method we still can access blog control routes by request each route by it's end point so to protect our blog control routes from this scenario we need to create our own decorator and this how I do it:

```python
def admin_only(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        if current_user.get_id() is None:
            next_page = request.args.get("next")
            return redirect(url_for("login"))
        elif current_user.get_id() != "1":
            return abort(403)
        return func(*args, **kwargs)
    return wrapper_func
```

That logic need to become familiar with two concept to understand how this decorator actually work they are :

- first class function 
- closure 

When you understand both of them you well be familiar with decorators, so lets explain how this decorator actually work:

**First** I used wraps decorator from functools module that will help us to avoid any conflicts will happen with our namespace later as it always return the name of the original function name instead of wrapper.

**Second** we checked if there is any user loaded to our session if there is no user loaded it will redirect the user to login route to login first then above our `admin_only` decorator we are going to use `login_required` decorator so it will flash a warning message and prevent the next keyword to redirect the user to that page after logged in as below:

![protect routes](https://user-images.githubusercontent.com/57592040/170173277-f7b5b818-aa1e-4b0a-b546-b65c39db5a34.gif)

else if the user is already loaded in the session we will check if it an admin as admin id number is 1 so if we got and different number we will return the user to `403` https page.

**Finally** if everything went well we will return the original route 

and here is an example how we stack `admin_only` and `login_required` decorators together.

```py
@app.route("/delete/<int:post_id>")
@login_required
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))
```

# Task 5

This step is very important as we need to understand the logic about how to connect two table together as one user may have many posts so the relationship between the two of them are one-to-many. 

so to simplify this concept lets say we have two class as below:

```python
class User:
    def __init__(self,id,name,email,password,posts):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.posts = []
        
class Post:
    def __init__(self,title,body)
    self.title = title 
    self.body = body
    
```

So when we need to create a user object from User class that has some posts created by this user we can do it like this:

```python
shalaby = User(
    id=1,
    name="shalaby",
    email="shalaby@email.com",
    password="123",
    posts = [
        Post(
        	title="Hallo World",
            body="I love coding"
        )
    ]
)
```

So here the user called shalaby can have many posts and to translate that to our tables we need to use two methods `relationship` and `ForeignKey` as showing below:

```python
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    posts = relationship("BlogPost", backref="user")
    
    
class BlogPost(db.Model):
    __tablename__ = "blog_post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
```

So as we can see that `User` table is a parent and `BlogPost` is a child as we said one user can have many posts so we create a `posts ` variable that will create a relationship with `BlogPost` table by adding a user column within the `BlogPost` table.

on other hand we need to connect the user table to the child BlogPost table and we name the result to  ` author_id`  column, I know it sound weird but focus with me because it took me maybe three days to solve this puzzle but still not fully understanding working with ORM.

lets see first how we add `author_id ` to the child `BlogPost` table??!

```python
new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            date=date.today().strftime("%B %d, %Y"),
            user=user
        )
```

First question you going to ask is Where is an `authour_id` column and why we assigned `user` parameter to user object ???  You are totally right,  me too I was writing it like below:

```python
new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            date=date.today().strftime("%B %d, %Y"),
            author_id=user.id
        )
```

But it always throw errors that I could not understand until I watched a video about doing the same thing so i understand that the Column name we actually added it  when we create a relationship with our `User` table as a parent `posts = relationship("BlogPost", backref="user")` and the `backref` parameter will establish a bidirectional relationship in one-to-many, where the “reverse” side is a many to one, specify an additional as mentioned in their documentation [here](https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html) 

And `author_id = db.Column(db.Integer, db.ForeignKey("user.id"))` from the Child `BlogPost` mean that it will create a column called author id that will save the foreign key as we chose here `user.id` 

until this point and we modified our tables we need to delete the database and create it again to confirm the new modification.
