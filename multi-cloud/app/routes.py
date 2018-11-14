from flask import render_template, flash, redirect, url_for, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, ResourceForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from app.price import *



@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created for ' + str(form.username.data) + '.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login failed. Please check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('account.html', title='Account', form=form)


@app.route('/workload')
def workload_defined():
    return render_template('workload.html', title='Workload-based')


@app.route('/custom', methods=['GET', 'POST'])
def custom():
    # os
    # storage
    # memory
    # cpu
    form = ResourceForm()
    if form.validate_on_submit():
        instance, top_three, valid_instances = find_instance(int(form.memory.data), int(form.storage.data))

        types = []
        for i in top_three:
            types.append(detect_type(i))

        instance_provider = detect_type(instance)

        return render_template('options.html', title='Options', instance=instance,
                               top_three=top_three, instance_provider=instance_provider, types=types,
                               length=len(top_three))

    return render_template('custom.html', title='User-based', form=form)


@app.route('/custom/deploy', methods=['POST'])
def deployment():
    print(request.form['button1'])

    return render_template('home.html', title='Home')
    print("here")









