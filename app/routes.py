from datetime import datetime
from flask import render_template, redirect, request, url_for, flash
from werkzeug.security import generate_password_hash
from app import app, db, bcrypt
from app.models import Article, User, RegistrationForm, NoteForm, Note


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create_article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article = Article(title=title, intro=intro, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return render_template('create_article.html')
        except Exception as e:
            print(f'Ошибка добавления статьи: {e}')
    else:
        return render_template('create_article.html')


@app.route('/display_articles')
def display_articles():
    articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template('display_articles.html', articles=articles)


@app.route('/article_more/<int:article_id>/')
def article_more(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('article_more.html', article=article)


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



@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    form = NoteForm()
    if form.validate_on_submit():
        submitted_title = form.title.data
        submitted_note = form.note.data
        new_note = Note(title=submitted_title, content=submitted_note, timestamp=datetime.utcnow())
        try:
            db.session.add(new_note)
            db.session.commit()
        except Exception as e:
            print(f'Error adding note to database: {e}')
            db.session.rollback()
        return redirect(url_for('add_note'))
    return render_template('add_note.html', form=form)

@app.route('/display_note')
def display_note():
    notes = Note.query.order_by(Note.timestamp.desc()).all()
    return render_template('display_note.html', notes=notes)

