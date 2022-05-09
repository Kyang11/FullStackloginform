from flask import render_template, request, flash, redirect, url_for
from .forms import EditProfileForm, LoginForm, RegisterForm
from  .import bp as auth
from ...models import User
from flask_login import current_user, logout_user, login_user, login_required

# ROUTES
@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit():
        # Do Login stuff
        email = form.email.data.lower()
        password = form.password.data

        #Look up user by email address that is trying to log in
        u=User.query.filter_by(email=email).first()
        if u and u.check_hashed_password(password):
            login_user(u)
            flash('Welcome to Fakebook!','success')
            return redirect(url_for('main.home'))
        flash('Incorrect Email Password Combo', 'danger')
        return render_template('login.html.j2', form=form)
    return render_template("login.html.j2", form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method =='POST' and form.validate_on_submit():
        try:
            new_user_data={
                "first_name":form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data,
                "icon":form.icon.data
            }
            # Create an empty User
            new_user_object = User()
            #build user with the form data
            new_user_object.from_dict(new_user_data)
            #save user to the database
            new_user_object.save()

        except:
            flash("There was an unexpected Error creating you account Please Try again Later","danger")
            return render_template('register.html.j2', form=form)
        flash('You have successfully registered!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html.j2', form=form)

@auth.route('/edit-profile', methods=['GET','POST'])
def edit_Profile():
    form = EditProfileForm()  ### need to check why is not green 

    if request.method == 'POST' and form.validate_on_submit():
        new_user_data={
            "first_name":form.first_name.data.title(),
            "last_name": form.last_name.data.title(),
            "email":form.email.data.lower(),
            "password":form.password.data,
            "icon":int(form.icon.data) if int(form.icon.data) != 9000 else current_user.icon
            }
        user = User.query.filter_by(email=new_user_data["email"]).first()
        if user and user.email != current_user.email:
            flash('The email alreadu in use','danger' ) ## someone name is same email and they use that email already
            return redirect(url_for('auth.edit_profile'))
        try:
            current_user.from_dict(new_user_data)
            current_user.save()
            flash('Profile updated successfully', 'Success')


        except:

            flash('An error occurred', 'danger')
            return redirect(url_for('auth.edit_profile'))
        return redirect(url_for('main.index'))

    return render_template('register.html.j2', form=form)



@auth.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out','warning')
        return redirect(url_for('auth.login'))