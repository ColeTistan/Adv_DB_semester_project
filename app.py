from flask import (
    Flask,
    render_template,
    request,
    url_for,
    redirect
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import os

base_directory = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_directory, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)

class Quote(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    quote = db.Column(db.String(255), nullable=False)
    character_name = db.Column(db.String(100), nullable=False)
    actor_name = db.Column(db.String(100), nullable=False)
    movie_name = db.Column(db.String(100), nullable=False)

    def __init__(self, quote, character_name, actor_name, movie_name):
        self.quote = quote
        self.character_name = character_name
        self.actor_name = actor_name
        self.movie_name = movie_name

    def __repr__(self):
        return f'"{self.quote}"\n- {self.character_name}\n{self.movie_name}'
    

@app.route('/')
@app.route('/home')
def index():
    quotes = Quote.query.all()
    return render_template('index.html', quotes=quotes)

@app.route('/create', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        quote = request.form['quote']
        character_name = request.form['character']
        actor_name = request.form['actor']
        movie_name = request.form['movie']
        new_quote = Quote(quote=quote, character_name=character_name, actor_name=actor_name, movie_name=movie_name)
        db.session.add(new_quote)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('insert.html')

@app.route('/edit/<int:quote_id>', methods=['GET', 'POST'])
def edit(quote_id):
    edit_quote = Quote.query.get_or_404(quote_id)
    if request.method == 'POST':
        quote = request.form['quote']
        character_name = request.form['character']
        actor_name = request.form['actor']
        movie_name = request.form['movie']

        edit_quote.quote = quote
        edit_quote.character_name = character_name
        edit_quote.actor_name = actor_name
        edit_quote.movie_name = movie_name

        db.session.add(edit_quote)
        db.session.commit()

        return redirect(url_for('index'))
    
    return render_template('edit.html', quote=edit_quote)

@app.route('/delete/<int:quote_id>')
def delete(quote_id):
    quote = Quote.query.get_or_404(quote_id)
    db.session.delete(quote)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)