import os
from flask import Flask, render_template, request
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'teste'
app.config['MYSQL_DATABASE_HOST'] = 'db'
mysql.init_app(app)

@app.route('/')
def main():
    return render_template('cadastrar.html')

@app.route('/gravar', methods=['POST','GET'])
def gravar():
  sqlQuery = """INSERT INTO tbl_produto (prod_marca, prod_nome, prod_preco, prod_qtd, prod_validade, prod_categoria) VALUES (%s, %s, %s, %s, %s, %s)"""
  marca = request.form['marca']
  nome = request.form['nome']
  preco = request.form['preco']
  quantidade = request.form['quantidade']
  validade = request.form['validade']
  categoria = request.form['categoria']
  inputDados = (marca, nome, preco, quantidade, validade, categoria)
  if marca and nome and preco and quantidade and validade and categoria:
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sqlQuery, inputDados)
    conn.commit()
  return render_template('cadastrar.html')

@app.route('/alterar', methods=['PUT','GET'])
def alterar():
  ProdID = request.form['prod_id']
  marca = request.form['marca']
  nome = request.form['nome']
  preco = request.form['preco']
  quantidade = request.form['quantidade']
  validade = request.form['validade']
  categoria = request.form['categoria']
  if ProdID and marca and nome and preco and quantidade and validade and categoria:
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('UPDATE tbl_produto SET prod_marca = %S, prod_nome = %S, prod_preco = %S, prod_qtd = %S, prod_validade = %S, prod_categoria = %S WHERE prod_id = %i', (marca, nome, preco, quantidade, validade, categoria, ProdID))
    conn.commit()
  return render_template('alterar.html')

@app.route('/listar', methods=['POST','GET'])
def listar():
  conn = mysql.connect()
  cursor = conn.cursor()
  cursor.execute('select prod_marca, prod_nome, prod_preco, prod_qtd, prod_validade, prod_categoria from tbl_produto')
  data = cursor.fetchall()
  conn.commit()
  return render_template('lista.html', datas=data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5008))
    app.run(host='0.0.0.0', port=port)
