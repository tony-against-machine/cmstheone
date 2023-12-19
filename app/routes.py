from flask import render_template, redirect, request, url_for, flash
from werkzeug.security import generate_password_hash
from app import app, db, bcrypt
from app.models import Article, User, RegistrationForm


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article = Article(title=title, intro=intro, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return render_template('create-article.html')
        except:
            print('Ошибка добавления статьи')
    else:
        return render_template('create-article.html')


@app.route('/display-articles')
def display_articles():
    articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template('display-articles.html', articles=articles)


@app.route('/article-more/<int:article_id>/')
def article_more(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('article-more.html', article=article)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Твоя учетная запись создана!', 'success')
        return render_template('index.html')
    return render_template('registration.html', form=form)


@app.route('/display-users')
def display_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('display-users.html', users=users)

