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


# @app.route('/display-users')
# def display_users():
#     users = User.get_id(id)
#     return render_template('display-users.html', users=users)


### add Note / start ###

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    form = NoteForm()

    if form.validate_on_submit():
        # Process the submitted note and save it to the database
        submitted_note = form.note.data
        new_note = Note(content=submitted_note)

        try:
            db.session.add(new_note)
            db.session.commit()
            print(f"Note added to database: {submitted_note}")
        except Exception as e:
            print(f"Error adding note to database: {e}")
            db.session.rollback()

        # Redirect to the home page or any other page after adding the note
        return redirect(url_for('add_note'))

    return render_template('add_note.html', form=form)



### add Note / end ###
