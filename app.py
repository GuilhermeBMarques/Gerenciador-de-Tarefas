from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3  
app = Flask(__name__)  
app.secret_key = 'chave-secreta'

# Função para inicialização 
def db():
    conn = sqlite3.connect("todo.db") 
    cursor = conn.cursor()  

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            titulo TEXT NOT NULL,  
            descricao TEXT NOT NULL,  
            estado TEXT CHECK(estado IN ('A Fazer', 'Em andamento', 'Concluido')) NOT NULL DEFAULT 'A Fazer'  
        )
    """)
    
    conn.commit()  
    conn.close()  

# Função para criar uma nova conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect("todo.db")  
    conn.row_factory = sqlite3.Row
    return conn  

# Rota principal 
@app.route("/")
def index():
    conn = get_db_connection()  
    tarefas = conn.execute("SELECT * FROM tarefas").fetchall() 
    conn.close()  
    return render_template('index.html', tarefas=tarefas)  

# Rota para adicionar uma nova tarefa
@app.route("/addTarefas", methods=["POST"])
def addTarefas():
    titulo = request.form["titulo"]  
    descricao = request.form["descricao"] 
    
    if not titulo:
        flash("Campo de titulo vazio!")
        return redirect(url_for("index"))  

    conn = get_db_connection()
    conn.execute("INSERT INTO tarefas (titulo, descricao, estado) VALUES (?, ?, ?)", (titulo, descricao, 'A Fazer'))
    conn.commit()  
    conn.close() 
    flash("Tarefa adicionado com sucesso!")
    return redirect(url_for("index"))  

# Rota para alterar o estado de uma tarefa 
@app.route("/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    valorBotao = request.form.get("botao") 
    
    if valorBotao == "andamento":
        valorBotao = "Em andamento"
        flash("Tarefa em andamento com sucesso!")
    elif valorBotao == "concluida":
        valorBotao = "Concluido"
        flash("Tarefa concluida com sucesso!")
            
    conn = get_db_connection()  
    conn.execute("UPDATE tarefas SET estado = ? WHERE id = ?", (valorBotao, task_id,))
    conn.commit()
    conn.close()  
    return redirect(url_for("index"))  

# Rota para deletar uma tarefa
@app.route("/deletTarefas/<int:task_id>", methods=["POST"])
def deletTarefas(task_id):
    conn = get_db_connection()  
    conn.execute("DELETE FROM tarefas WHERE id = ?", (task_id,))
    conn.commit() 
    conn.close()  
    flash("Tarefa deletada com sucesso!")
    return redirect(url_for("index"))  

if __name__ == "__main__":
    db() 
    app.run(debug=True)  
