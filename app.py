from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cod = db.Column(db.String(50), nullable=False, unique=True)
    descricao = db.Column(db.Text, nullable=True)
    preco = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    products = Produto.query.all()
    return render_template('index.html', products=products)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nome = request.form['nome']
        cod = request.form['cod']
        descricao = request.form['descricao']
        preco = request.form['preco']

        product = Produto(nome=nome, cod=cod, descricao=descricao, preco=preco)
        db.session.add(product)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    product = Produto.query.get(id)

    if request.method == 'POST':
        product.nome = request.form['nome']
        product.cod = request.form['cod']
        product.descricao = request.form['descricao']
        product.preco = request.form['preco']

        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit.html', product=product)

@app.route('/delete/<int:id>')
def delete(id):
    product = Produto.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
