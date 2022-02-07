

##from multiprocessing.sharedctypes import Value
#from optparse import Values
#from re import S
from re import S
from this import s
from flask import Flask, render_template,url_for, request, flash,redirect,jsonify
from flask_login import logout_user
from markupsafe import re
from sqlalchemy import asc,desc
from werkzeug.security import generate_password_hash
#from flask_sqlalchemy import asc,
from werkzeug.utils import redirect
from flask_app import app, db
from flask_app.models import Rating, User, Post, Comment 
from flask_app.forms import RegistrationForm,LoginForm,CommentForm,SelectOrderForm
from flask_login import login_user, current_user, logout_user, login_required
#import json
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

#    if request.method == 'POST':
#      comment = request.form.get('comment')
#
#      if len(note) < 1:
#          flash('Note is too short!', category='error')
#      else:
#          new_comment = Comment(data=comment, user_id=current_user.id)
#          db.session.add(new_comment)
#          db.session.commit()
#          flash('Note added!', category='success')
#
#  return render_template("home.html", user=current_user)

##delete comment 
#@app.route('/delete-comment', methods=['POST'])
#def delete_comment():
#    comment = json.loads(request.data)
#    userId = comment['userId']
#    comment = Comment.query.get(userId)
#    if comment:
#        if comment.user_id == current_user.id:
#            db.session.delete(comment)
#            db.session.commit()

    #return jsonify({})
    #list_of_posts=Post.query.all()#give a list of all the Post objects
    #for post in list_of_posts:
       #print(post.title)
    #return render_template("home.html", posts=list_of_posts,form=form)
    

@app.route("/register", methods=["GET","POST"])
def register():
    form =RegistrationForm()
    if request.method == 'GET':
        flash("WELCOME")
        return render_template("register.html", form=form)
    else:
        if form.validate_on_submit():
            #hashed_password = bcrypt.generate_password_hash(form_internal.password.data).decode('utf-8')
            
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
        #

#@app.route("/registered_url")
#def registered_function():
    #return render_template("registered.html")

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
#new
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
    # comment = Comment.query.filter(Comment.post_id==post.id)
    comment = Comment.getCommentsByPost(post_id)
    rate = Rating.getCurrentUserRate(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        print("nnora")
        db.session.add(Comment
            (comment=form.comment.data,
        #star=form.rate.data,
        post_id=post.id,
        user_id=current_user.id))
        db.session.commit()
        flash("Your comment has been added to the post","success")
        return redirect(f'/post/{post.id}')

    return render_template('post.html',post=post,comments=comment,form=form,rate=rate)

#@app.route('/post/<int:post_id>/comment',methods=['GET','POST'])
#@login_required
#def post_comment(post_id):
#    print("nora")
#    post=Post.query.get_or_404(post_id)
#    form=CommentForm()
#    if form.validate_on_submit():
#        db.session.add(Comment
#            (comment=form.comment.data,
#        #star=form.rate.data,
#        post_id=post.id,
#        author_id=current_user.id))
#        db.session.commit()
#        flash("Your comment has been added to the post","success")
#        return redirect(f'/post/{post.id}')
#    
#    else:
#        print("ok")
#        flash(
#               'Something wrong with your comment')
#  #comment=Comment.query.filter(Comment.post_id==post.id)
#  #return render_template('post.html',post=post,comment=comment,form=form)
#    comment = {
#        '5' : len(list(filter(lambda x: x.star == 5, post.comment))),
#        '4' : len(list(filter(lambda x: x.star == 4, post.comment))),
#        '3' : len(list(filter(lambda x: x.star == 3, post.comment))),
#        '2' : len(list(filter(lambda x: x.star == 2, post.comment))),
#        '1' : len(list(filter(lambda x: x.star == 1, post.comment)))
#    }
#    print(comment)
#    return render_template('post.html', title=post.title, post=post, form=form, comment=comment)

#new
#@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
#def post(post_id):
#    post=Post.query.get_or_404(post_id)
#    return render_template('post.html',title=post.title,post=post)
#
#@app.route("/post/<int:post_id>", methods=["POST"])
#@login_required
#def comment(post_id):
#    content = request.form["content"]
#    comment_rate = request.form["rate"]
#    db.session.add(
#        Comment(content=content, rate=comment_rate, u_id=current_user.id, p_id=post_id)
#    )
#    db.session.commit()
#    return redirect(url_for("post", post_id=post_id))
#####
#  form = CommentForm()
#  if form.validate_on_submit() and current_user.is_authenticated:
#      comment = Comment(body=form.body.data,
#                        post=post,
#                        author=current_user._get_current_object())
#      db.session.add(comment)
#      db.session.commit()
#      flash('Your comment has been published.')
#      return redirect(url_for('.post', post_id=post.id))
#  page = request.args.get('page', 1, type=int)
#  if page == -1:
#      page = (post.comment.count() - 1) // 5
#  pagination = post.comment.order_by(Comment.timestamp.asc()).paginate(
#      page, per_page=5,
#      error_out=False)
#    comment = pagination.items
    #return render_template('post.html', title=post.title, post=post, form=form,
                         #  comment=comment, pagination=pagination)
 # return render_template('post.html',title=post.title,post=post)

@app.route("/rating")
def rating():
  score = request.args.get('score')
  post_id = request.args.get('post_id')
  Rating.addOrUpdate(post_id,score)
  return redirect('/post/'+post_id)


#@app.route("/DBMaker")
#def dbmake():
   # db.create_all
    
# @app.route("/pers_greet")
# def pers_greet():
#     if current_user.is_authenticated:
#         flash('Hello, <LOGGED-IN first_name_new>!')
#     else:
#         flash('Hello Guest')
#   #return render_template('post.html',title=post.title,post=post)
# #@app.route("/about")   
# #def about():
#     #return render_template('about.html', title='About')
######@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
#def post(post_id):
#    form = CommentForm()
#    if request.method == 'POST':
#        if form.validate_on_submit():
#            comment = Comment(
#                star=form.rate.data,
#                content=form.content.data,
#                post_id=post_id,
 #               user_id=current_user.id)
 #           db.session.add(comment)
 #           db.session.commit()
 #           return redirect(url_for('post', post_id=post_id))
 #       else:
 #           flash(
 #               'Something wrong with your comment, write something before submitting', 'danger')
#
   # post = Post.query.get_or_404(post_id)
  ##  comments = {
  ##      '5' : len(list(filter(lambda x: x.star == 5, post.comments))),
  ###      '4' : len(list(filter(lambda x: x.star == 4, post.comments))),
  ###      '3' : len(list(filter(lambda x: x.star == 3, post.comments))),
  ###      '2' : len(list(filter(lambda x: x.star == 2, post.comments))),
  ###      '1' : len(list(filter(lambda x: x.star == 1, post.comments)))
  ###  }
 #  # print(comments)
    #return render_template('post.html', title=post.title, post=post, form=form, comments=comments)
#