from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

app = Flask(__name__)
app.config["SERCET_KEY"] = "super_serct_key_values"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

csrf = CSRFProtect(app)

# create table sql
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False) 

class RegisterForm(FlaskForm):
	username = StringField(validators=[InputRequired(),Length(min=4 , max = 20)], render_kw={"placeholder":"Username"})
	password = StringField(validators=[InputRequired(),Length(min=4 , max = 20)], render_kw={"placeholder":"Password"})
	submit = SubmitField("Register")

	def validatate_username(self, username):
		existing_username = User.query.filter_by(
			username=username.data).first()

		if existing_username:
			raise ValidationError("That username already exists.")
class LoginForm(FlaskForm):
	username = StringField(validators=[InputRequired(),Length(min=4 , max = 20)], render_kw={"placeholder":"Username"})
	password = StringField(validators=[InputRequired(),Length(min=4 , max = 20)], render_kw={"placeholder":"Password"})
	submit = SubmitField("Login")

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/login", methods=["GET","POST"])
def login():
	form = LoginForm()
	return render_template("login.html",form = form)

@app.route("/register", methods=["GET","POST"])
def register():
	form = RegisterForm()
	return render_template("register.html",form = form)

if __name__ == '__main__':
	app.run(debug=True)	



# from flask import Flask, render_template, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin, LoginManager, login_user,current_user, logout_user
# from flask_wtf import FlaskForm
# from  wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import InputRequired, Length, ValidationError  


# app = Flask(__name__)
# app.config["SECRET_KEY"] = "your_strong_secret_key"  
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# db = SQLAlchemy(app)

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view  = 'login'  

# # User model
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), nullable=False, unique=True)
#     password = db.Column(db.String(80), nullable=False)  


# # Registration form
# class RegisterForm(FlaskForm):
#     username = StringField('Username', validators=[InputRequired(),Length(
#     	min=4, max=20)], render_kw={"placeholder": "Username"})
#     password = PasswordField('Password', validators=[InputRequired(),  Length(
#     	min=4, max=20)], render_kw={"placeholder": "Password"})
#     submit = SubmitField('Register')

#     def validate_username(self, username):
#         existing_username = User.query.filter_by(username=username.data).first()
#         if existing_username:
#             raise ValidationError("That username already exists.")  


# # Login form
# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[InputRequired(), Length(
#     	min=4, max=20)], render_kw={"placeholder": "Username"})
#     password = PasswordField('Password', validators=[InputRequired(),  Length(
#     	min=4, max=20)], render_kw={"placeholder": "Password"})
#     submit = SubmitField('Login')

# # Routes

# @app.route("/")
# def  home():
#     if current_user.is_authenticated:
#         return render_template("home.html", logged_in=True)
#     else:
#         return render_template("home.html", logged_in=False)

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if  user and user.check_password(form.password.data):
#             login_user(user)
#             return redirect(url_for('home'))
#         else:
#             flash('Invalid username or password.')  
#     return render_template("login.html", form=form)

# @app.route("/logout")
# def logout():
#     logout_user()
#     return redirect(url_for('home'))

# @app.route("/register", methods=["GET", "POST"])  

# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         new_user = User(username=form.username.data, password=form.password.data)
#         db.session.add(new_user)
#         db.session.commit()
#         return  redirect(url_for('login'))
#     return render_template("register.html", form=form)

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()  
#     app.run(debug=True)