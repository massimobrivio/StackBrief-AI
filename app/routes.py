from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, SubscriptionForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, SoftwareTool, UserSoftware
from urllib.parse import urlparse


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/manage_tools', methods=['GET', 'POST'])
@login_required
def manage_tools():
    form = SubscriptionForm()
    # Populate the select field with software tools not already subscribed to
    subscribed_software_ids = [subscription.software_id for subscription in current_user.subscriptions]
    available_software = SoftwareTool.query.filter(~SoftwareTool.id.in_(subscribed_software_ids)).all()
    form.software.choices = [(software.id, software.name) for software in available_software]

    if form.validate_on_submit():
        software_id = form.software.data
        subscription = UserSoftware(user_id=current_user.id, software_id=software_id)
        db.session.add(subscription)
        db.session.commit()
        flash('Software tool subscribed successfully.')
        return redirect(url_for('manage_tools'))

    # Get the user's current subscriptions
    user_subscriptions = current_user.subscriptions
    return render_template('manage_tools.html', title='Manage Subscriptions', form=form, subscriptions=user_subscriptions)

@app.route('/unsubscribe/<int:subscription_id>', methods=['POST'])
@login_required
def unsubscribe(subscription_id):
    subscription = UserSoftware.query.filter_by(id=subscription_id, user_id=current_user.id).first()
    if subscription:
        db.session.delete(subscription)
        db.session.commit()
        flash('Subscription removed.')
    else:
        flash('Subscription not found.')
    return redirect(url_for('manage_tools'))