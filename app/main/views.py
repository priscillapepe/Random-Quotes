from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import User,quote,Comment
from .. import db,photos
from app.request import get_quotes
from .forms import UpdateProfile,QuoteForm,CommentForm
from flask_login import login_required,current_user
import datetime

# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''

    title = 'Home - Welcome to Random quote'

    quotes = get_quotes()
    

    return render_template('index.html',title = title, quotes = quotes)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    quote_count = quote.count_quote(uname)
    user_joined = user.date_joined.strftime('%b %d, %Y')

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,quote = quote_count,date = user_joined)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form = form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/quote/new', methods = ['GET','POST'])
@login_required
def new_quote():
    quote_form = PitchForm()
    if quote_form.validate_on_submit():
        title = quote_form.title.data
        quote = quote_form.text.data
        category = quote_form.category.data

        # Updated quote instance
        new_quote = Quote(quote_title=title,quote_content=quote,category=category,user=current_user,likes=0,dislikes=0)

        # Save quote method
        new_quote.save_quote()
        return redirect(url_for('.index'))

    title = 'New quote'
    return render_template('new_quote.html',title = title,quote_form=quote_form )

@main.route('/quote/<int:id>', methods = ['GET','POST'])
def quote(id):
    quote = Quote.get_quote(id)
    posted_date = quote.posted.strftime('%b %d, %Y')

    if request.args.get("like"):
        quote.likes = quote.likes + 1

        db.session.add(quote)
        db.session.commit()

        return redirect("/quote/{quote}".format(quote_id=quote.id))

    elif request.args.get("dislike"):
        quote.dislikes = quote.dislikes + 1

        db.session.add(quote)
        db.session.commit()

        return redirect("/quote/{quote_id}".format(quote_id=quote.id))

    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = comment_form.text.data

        new_comment = Comment(comment = comment,user = current_user,quote_id = quote)

        new_comment.save_comment()


    comments = Comment.get_comments(quote)

    return render_template("quote.html", quote = quote, comment_form = comment_form, comments = comments, date = posted_date)

@main.route('/user/<uname>/quote')
def user_quote(uname):
    user = User.query.filter_by(username=uname).first()
    quote = quote.query.filter_by(user_id = user.id).all()
    quote_count = quote.count_quote(uname)
    user_joined = user.date_joined.strftime('%b %d, %Y')

    return render_template("profile/quote.html", user=user,quote=quote,quote_count=quote_count,date = user_joined)
