from flask import render_template, request, redirect, url_for, flash
from .forms import LoginForm, RegisterForm, EditProfileForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from .import bp as auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = request.form.get("email").lower()
        password = request.form.get("password")

        u = User.query.filter_by(email=email).first()

        if u and u.check_password_hash(password):
            login_user(u)
            # give user feedback that you logged in successfully
            flash('You have logged in trainer', 'success')
            return redirect(url_for("main.index"))
        error_string = "Invalid Email and Password combo"
        return render_template('login.html.j2', error=error_string, form=form)
    return render_template('login.html.j2', form=form)


@auth.route('/logout')
def logout():
    if current_user:
        logout_user()
        flash('You have logged out', 'danger')
        return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data = {
                "first_name": form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "email": form.email.data.lower(),
                "password": form.password.data,
                "icon": int(form.icon.data)
            }
            # create and empty user
            new_user_object = User()
            # build user with form data
            new_user_object.from_dict(new_user_data)
            # save user to database
            new_user_object.save()
        except:
            error_string = "There was an unexpected Error while creating your account. Try again later"
            # when we had an error creating a user
            return render_template('register.html.j2', form=form, error=error_string)
        # on a post request that successfully creates a new user. redirect is for when wrong redirect back to the page that you want
        return redirect(url_for('auth.login'))
    # the render template on the GEt request
    return render_template('register.html.j2', form=form)


@auth.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_user_data = {
            "first_name": form.first_name.data.title(),
            "last_name": form.last_name.data.title(),
            "email": form.email.data.lower(),
            "password": form.password.data,
            "icon": int(form.icon.data) if int(form.icon.data) != 9000 else current_user.icon
        }
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and current_user.email != user.email:
            flash('Email is already in use', 'danger')
            return redirect(url_for('auth.edit_profile'))
        try:
            current_user.from_dict(new_user_data)
            current_user.save()
            flash('Profile has been Updated', 'success')
        except:
            flash('There was an unexpected error', 'danger')
            return redirect(url_for('auth.edit_profile'))
    return render_template('register.html.j2', form=form)
