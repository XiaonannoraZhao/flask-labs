


from re import S
from this import s
from flask import Flask, render_template,url_for, request, flash,redirect,jsonify
from flask_login import logout_user
from markupsafe import re
from sqlalchemy import asc,desc
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect
from flask_app import app, db
from flask_app.models import Rating, User, Post, Comment 
from flask_app.forms import RegistrationForm,LoginForm,CommentForm,SelectOrderForm
from flask_login import login_user, current_user, logout_user, login_required
@app.route("/", methods=["GET","POST"])
def home_function ():
    form = SelectOrderForm()
    posts = []
    if form.date.data == 'date_asc':
        posts = Post.query.order_by(asc(Post.date)).all()
    elif form.date.data == 'date_desc' or form.date.data==None:
        posts = Post.query.order_by(desc(Post.date)).all()
    else:
        posts = Post.query.all()
    
    return render_template('home.html', form=form, posts=posts)

    

@app.route("/register", methods=["GET","POST"])
def register():
    form =RegistrationForm()
    if request.method == 'GET':
        flash("WELCOME")
        return render_template("register.html", form=form)
    else:
        if form.validate_on_submit():
          
            user = User(
                username=form.first_name_new.data,
                email=form.email_new.data,
                hashed_password = generate_password_hash(form.password_new.data),
                
            )
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('login'))
        else:
            print("not ok")
        
            
            flash('Your password contain invalid characters.')
            return redirect(url_for('register'))
 
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_function'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home_function'))
        else:
            flash('Incorrect email or password supplied.')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for("home_function"))
# loginError
@app.route('/error', methods=['GET'])
def login_error():
    return render_template('error.html',
                           data=dict(router="Error", title="Error"))

@app.route("/post/<int:post_id>",methods=['GET','POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
  
    comment = Comment.getCommentsByPost(post_id)
    rate = Rating.getCurrentUserRate(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        print("nnora")
        db.session.add(Comment
            (comment=form.comment.data,
       
        post_id=post.id,
        user_id=current_user.id))
        db.session.commit()
        flash("Your comment has been added to the post","success")
        return redirect(f'/post/{post.id}')

    return render_template('post.html',post=post,comments=comment,form=form,rate=rate)


@app.route("/rating")
def rating():
  score = request.args.get('score')
  post_id = request.args.get('post_id')
  Rating.addOrUpdate(post_id,score)
  return redirect('/post/'+post_id)

