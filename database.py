import sqlite3
from datetime import date

def conectar():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano INTEGER,
            status TEXT DEFAULT 'Disponível'
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estudantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            matricula TEXT UNIQUE NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_livro INTEGER,
            id_estudante INTEGER,
            data_emprestimo TEXT,
            data_devolucao TEXT,
            FOREIGN KEY (id_livro) REFERENCES livros(id),
            FOREIGN KEY (id_estudante) REFERENCES estudantes(id)
        )
    ''')
    conn.commit()
    return conn

def adicionar_livro(titulo, autor, ano):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO livros (titulo, autor, ano) VALUES (?, ?, ?)", (titulo, autor, ano))
    conn.commit()
    conn.close()

def obter_livros():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros")
    livros = cursor.fetchall()
    conn.close()
    return livros

def ver_livros():
    return obter_livros()

def atualizar_livro(id, titulo, autor, ano, status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE livros SET titulo=?, autor=?, ano=?, status=? WHERE id=?", (titulo, autor, ano, status, id))
    conn.commit()
    conn.close()

def deletar_livro(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM livros WHERE id=?", (id,))
    conn.commit()
    conn.close()

def adicionar_estudante(nome, matricula):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO estudantes (nome, matricula) VALUES (?, ?)", (nome, matricula))
    conn.commit()
    conn.close()

def ver_estudantes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM estudantes")
    estudantes = cursor.fetchall()
    conn.close()
    return estudantes

def emprestar_livro(id_livro, id_estudante):
    conn = conectar()
    cursor = conn.cursor()
    hoje = date.today().strftime('%Y-%m-%d')
    cursor.execute("INSERT INTO emprestimos (id_livro, id_estudante, data_emprestimo) VALUES (?, ?, ?)", (id_livro, id_estudante, hoje))
    cursor.execute("UPDATE livros SET status='Emprestado' WHERE id=?", (id_livro,))
    conn.commit()
    conn.close()

def devolver_livro(id_emprestimo, id_livro):
    conn = conectar()
    cursor = conn.cursor()
    hoje = date.today().strftime('%Y-%m-%d')
    cursor.execute("UPDATE emprestimos SET data_devolucao=? WHERE id=?", (hoje, id_emprestimo))
    cursor.execute("UPDATE livros SET status='Disponível' WHERE id=?", (id_livro,))
    conn.commit()
    conn.close()

def ver_emprestimos_ativos():
    conn = conectar()
    cursor = conn.cursor()
    query = """
        SELECT e.id, l.titulo, s.nome, e.data_emprestimo
        FROM emprestimos e
        JOIN livros l ON e.id_livro = l.id
        JOIN estudantes s ON e.id_estudante = s.id
        WHERE e.data_devolucao IS NULL
    """
    cursor.execute(query)
    emprestimos = cursor.fetchall()
    conn.close()
    return emprestimos