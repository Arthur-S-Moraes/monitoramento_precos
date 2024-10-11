import sqlite3

def criar_sql():
    conexao = sqlite3.connect('urls.db')
    cursor = conexao.cursor()
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS Urls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    URL TEXT NOT NULL,
                    PRODUTO TEXT
                    );
                    ''')
    conexao.commit()
    return conexao

def adicionar_dados(conexao, url, produto):
    cursor = conexao.cursor()
    cursor.execute(f'INSERT INTO urls (Url, produto) VALUES ("{url}", "{produto}")')
    conexao.commit()

def visualizar(conexao):
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM urls')
    tarefas = cursor.fetchall()
    for tarefa in tarefas:
        print(tarefa)
        print('')


def pegar_url(conexao):
    urls= []
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM urls')
    tarefas = cursor.fetchall()
    for tarefa in tarefas:
        urls.append(tarefa[1])
        
    return urls

def excluir(conexao,id):
    cursor = conexao.cursor()
    cursor.execute('DELETE from urls WHERE id =?',(id,))
    conexao.commit()

def editar(conexao, editado, id):
    cursor = conexao.cursor()
    cursor.execute('UPDATE urls SET URL = ? WHERE id = ?',(editado, id))
    conexao.commit()

