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

### Task number 3: Logout The User

Now we need to add a logout route that will logout the user from the session and we have just 3 steps here.

**Step 1:** Use the `logout_user` from Flask_login tool 

**Step 2:** Return the login and register button back to the navbar and hide the logout button.

**Step 3:** Redirect the User to the home page.

### Task number 4: Protect Routes

Now we will protect our administrator routes and it is `add_new_post`, `edit_post` and `delete_post`, and here you need 4 steps to achieve this task:

**Step 1:** We need the user who's id equal to 1 to become an admin so only him can `add_new_post`, `edit_post` and `delete_post`.

**Step 2:** We need to edit our home page and post page that will control showing the control button only for and admin and hide them from any other users.

**Step 3:** Even we hide the control buttons from the normal users Still they can use the routes end points to reach the control routes, So we need here to protect them (Routes) by customize our only_admin decorator.

**Step 4:** We need to combine `login_required` and `admin_only ` decorators so we can control the situation where if any anonymous user try to reach any of control routes first it will ask that user to log in by using `login_required` then we need to check if that user is an admin or not by `admin_only` decorator. 

### Task number 5: Creating Relational Databases

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
