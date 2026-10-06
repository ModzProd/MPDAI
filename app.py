import os
import sys
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

# Configuração para funcionar tanto em desenvolvimento quanto no executável (.exe)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

app = Flask(__name__, template_folder=resource_path('templates'))

# O banco de dados será criado na mesma pasta do executável/script
DB_NAME = 'catalogo_database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS obras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            tipo TEXT NOT NULL,
            ano_lancamento INTEGER,
            sinopse TEXT,
            status TEXT,
            poster_url TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS obra_generos (
            obra_id INTEGER,
            genero_id INTEGER,
            FOREIGN KEY (obra_id) REFERENCES obras (id),
            FOREIGN KEY (genero_id) REFERENCES generos (id)
        )
    ''')
    
    cursor.execute('SELECT COUNT(*) FROM generos')
    if cursor.fetchone()[0] == 0:
        generos_padrao = ['Ação', 'Comédia', 'Drama', 'Ficção Científica', 'Terror', 'Romance', 'Documentário', 'Animação']
        for gen in generos_padrao:
            cursor.execute('INSERT INTO generos (nome) VALUES (?)', (gen,))
            
    conn.commit()
    conn.close()

@app.route('/')
def index():
    busca = request.args.get('busca', '')
    conn = get_db_connection()
    
    query = '''
        SELECT o.*, GROUP_CONCAT(g.nome, ', ') as generos 
        FROM obras o
        LEFT JOIN obra_generos og ON o.id = og.obra_id
        LEFT JOIN generos g ON og.genero_id = g.id
    '''
    
    if busca:
        query += " WHERE o.titulo LIKE ? GROUP BY o.id ORDER BY o.id DESC"
        obras = conn.execute(query, (f'%{busca}%',)).fetchall()
    else:
        query += " GROUP BY o.id ORDER BY o.id DESC"
        obras = conn.execute(query).fetchall()
        
    generos = conn.execute('SELECT * FROM generos ORDER BY nome').fetchall()
    conn.close()
    
    return render_template('index.html', obras=obras, generos=generos, busca=busca)

@app.route('/adicionar', methods=('POST',))
def adicionar():
    titulo = request.form['titulo']
    tipo = request.form['tipo']
    ano = request.form['ano_lancamento']
    sinopse = request.form['sinopse']
    status = request.form['status']
    poster_url = request.form['poster_url']
    generos_selecionados = request.form.getlist('generos')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO obras (titulo, tipo, ano_lancamento, sinopse, status, poster_url) VALUES (?, ?, ?, ?, ?, ?)",
                   (titulo, tipo, ano, sinopse, status, poster_url))
    obra_id = cursor.lastrowid
    
    for gen_id in generos_selecionados:
        cursor.execute("INSERT INTO obra_generos (obra_id, genero_id) VALUES (?, ?)", (obra_id, gen_id))
        
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=('GET',))
def editar(id):
    conn = get_db_connection()
    obra = conn.execute('SELECT * FROM obras WHERE id = ?', (id,)).fetchone()
    generos = conn.execute('SELECT * FROM generos ORDER BY nome').fetchall()
    
    generos_da_obra = conn.execute('SELECT genero_id FROM obra_generos WHERE obra_id = ?', (id,)).fetchall()
    ids_generos_da_obra = [str(g['genero_id']) for g in generos_da_obra]
    
    conn.close()
    return render_template('editar.html', obra=obra, generos=generos, ids_generos_da_obra=ids_generos_da_obra)

@app.route('/salvar_edicao/<int:id>', methods=('POST',))
def salvar_edicao(id):
    titulo = request.form['titulo']
    tipo = request.form['tipo']
    ano = request.form['ano_lancamento']
    sinopse = request.form['sinopse']
    status = request.form['status']
    poster_url = request.form['poster_url']
    generos_selecionados = request.form.getlist('generos')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""UPDATE obras SET titulo = ?, tipo = ?, ano_lancamento = ?, sinopse = ?, status = ?, poster_url = ? WHERE id = ?""",
                   (titulo, tipo, ano, sinopse, status, poster_url, id))
    
    cursor.execute("DELETE FROM obra_generos WHERE obra_id = ?", (id,))
    for gen_id in generos_selecionados:
        cursor.execute("INSERT INTO obra_generos (obra_id, genero_id) VALUES (?, ?)", (id, gen_id))
        
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>', methods=('POST',))
def deletar(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM obra_generos WHERE obra_id = ?', (id,))
    conn.execute('DELETE FROM obras WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    # Roda na porta 5000 sem abrir o debug para o executável ficar estável
    app.run(debug=False, port=5000)
