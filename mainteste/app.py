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
    return render_template('gravar.html')

@app.route('/gravar', methods=['POST','GET'])
def gravar():
  sqlQuery = """INSERT INTO tbl_produto (prod_marca, prod_nome, prod_preco, prod_qtd, prod_validade, prod_categoria, prod_ID) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
  marca = request.form['marca']
  nome = request.form['nome']
  preco = request.form['preco']
  quantidade = request.form['quantidade']
  validade = request.form['validade']
  categoria = request.form['categoria']
  prodID = request.form['prodID']
  inputDados = (marca, nome, preco, quantidade, validade, categoria, prodID)
  if marca and nome and preco and quantidade and validade and categoria and prodID:
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sqlQuery, inputDados)
    conn.commit()
  return render_template('cadastrar.html')

@app.route('/alterar', methods=['POST','GET'])
def alterar():
  return render_template('alterarProd.html')

@app.route('/listar', methods=['POST','GET'])
def listar():
  sqlQuery = """SELECT prod_marca, prod_nome, prod_preco, prod_qtd, prod_validade, prod_categoria, prod_ID FROM tbl_produto"""
  conn = mysql.connect()
  cursor = conn.cursor()
  cursor.execute(sqlQuery)
  data = cursor.fetchall()
  conn.commit()
  return render_template('lista.html', datas=data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5008))
    app.run(host='0.0.0.0', port=port)
