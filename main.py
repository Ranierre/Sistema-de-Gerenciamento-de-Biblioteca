import tkinter as tk
from tkinter import messagebox, ttk
import database as db
import sqlite3

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gerenciamento de Biblioteca")
        self.geometry("800x600")

        db.conectar()

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=10, fill="both", expand=True)

        self.frame_livros = ttk.Frame(self.notebook, width=780, height=580)
        self.frame_estudantes = ttk.Frame(self.notebook, width=780, height=580)
        self.frame_emprestimos = ttk.Frame(self.notebook, width=780, height=580)

        self.notebook.add(self.frame_livros, text="Livros")
        self.notebook.add(self.frame_estudantes, text="Estudantes")
        self.notebook.add(self.frame_emprestimos, text="Empréstimos")

        self.criar_aba_livros()
        self.criar_aba_estudantes()
        self.criar_aba_emprestimos()

    def criar_aba_livros(self):
        from_frame = ttk.LabelFrame(self.frame_livros, text="Adicionar/Editar Livros")
        from_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(from_frame, text="Título").grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.entry_titulo = ttk.Entry(from_frame, width=40)
        self.entry_titulo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(from_frame, text="Autor").grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.entry_autor = ttk.Entry(from_frame, width=40)
        self.entry_autor.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(from_frame, text="Ano").grid(row=2, column=0, padx=5, pady=5, sticky="W")
        self.entry_ano = ttk.Entry(from_frame, width=40)
        self.entry_ano.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(from_frame, text="Status").grid(row=3, column=0, padx=5, pady=5, sticky="W")
        self.entry_status = ttk.Entry(from_frame, width=40)
        self.entry_status.grid(row=3, column=1, padx=5, pady=5)

        btn_frame = ttk.Frame(from_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Adicionar Livro", command=self.adicionar_livros).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Atualizar Livro", command=self.atualizar_livro).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Deletar Livro", command=self.deletar_livro).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Limpar Campos", command=self.limpar_campos_livro).pack(side="left", padx=5)

        list_frame = ttk.LabelFrame(self.frame_livros, text="Lista de Livros")
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree_livros = ttk.Treeview(list_frame, columns=("ID", "Título", "Autor", "Ano", "Status"), show="headings")
        self.tree_livros.heading("ID", text="ID")
        self.tree_livros.heading("Título", text="Título")
        self.tree_livros.heading("Autor", text="Autor")
        self.tree_livros.heading("Ano", text="Ano")
        self.tree_livros.heading("Status", text="Status")

        self.tree_livros.column("ID", width=50)
        self.tree_livros.column("Título", width=200)
        self.tree_livros.column("Autor", width=150)
        self.tree_livros.column("Ano", width=100)
        self.tree_livros.column("Status", width=100)

        self.tree_livros.pack(fill="both", expand=True)
        self.tree_livros.bind("<<TreeviewSelect>>", self.selecionar_livro)
        self.atualizar_treeview_livros()

    def adicionar_livros(self):
        titulo = self.entry_titulo.get()
        autor = self.entry_autor.get()
        ano = self.entry_ano.get()

        if titulo and autor and ano:
            db.adicionar_livro(titulo, autor, ano)
            messagebox.showinfo("Sucesso", "Livro adicionado com sucesso!")
            self.limpar_campos_livro()
            self.atualizar_treeview_livros()
        else:
            messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")

    def atualizar_livro(self):
        item_selecionado = self.tree_livros.selection()
        if not item_selecionado:
            messagebox.showwarning("Erro", "Por favor, selecione um livro para atualizar.")
            return
        livro_id = self.tree_livros.item(item_selecionado)["values"][0]
        titulo = self.entry_titulo.get()
        autor = self.entry_autor.get()
        ano = self.entry_ano.get()
        status = self.entry_status.get()
        if titulo and autor and ano:
            db.atualizar_livro(livro_id, titulo, autor, ano, status)
            messagebox.showinfo("Sucesso", "Livro atualizado com sucesso!")
            self.limpar_campos_livro()
            self.atualizar_treeview_livros()
        else:
            messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")

    def deletar_livro(self):
        item_selecionado = self.tree_livros.selection()
        if not item_selecionado:
            messagebox.showwarning("Erro", "Por favor, selecione um livro para deletar.")
            return
        livro_id = self.tree_livros.item(item_selecionado)["values"][0]
        db.deletar_livro(livro_id)
        messagebox.showinfo("Sucesso", "Livro deletado com sucesso!")
        self.limpar_campos_livro()
        self.atualizar_treeview_livros()

    def selecionar_livro(self, event):
        item_selecionado = self.tree_livros.selection()
        if item_selecionado:
            livro = self.tree_livros.item(item_selecionado)["values"]
            self.entry_titulo.delete(0, tk.END)
            self.entry_titulo.insert(0, livro[1])
            self.entry_autor.delete(0, tk.END)
            self.entry_autor.insert(0, livro[2])
            self.entry_ano.delete(0, tk.END)
            self.entry_ano.insert(0, livro[3])
            self.entry_status.delete(0, tk.END)
            self.entry_status.insert(0, livro[4])

    def limpar_campos_livro(self):
        self.entry_titulo.delete(0, tk.END)
        self.entry_autor.delete(0, tk.END)
        self.entry_ano.delete(0, tk.END)
        self.entry_status.delete(0, tk.END)

    def atualizar_treeview_livros(self):
        for item in self.tree_livros.get_children():
            self.tree_livros.delete(item)
        livros = db.obter_livros()
        for livro in livros:
            self.tree_livros.insert("", tk.END, values=livro)

    def criar_aba_estudantes(self):
        form_frame = ttk.LabelFrame(self.frame_estudantes, text="Adicionar/Editar Estudantes")
        form_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(form_frame, text="Nome").grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.entry_nome_estudante = ttk.Entry(form_frame, width=40)
        self.entry_nome_estudante.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Matrícula").grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.entry_matricula_estudante = ttk.Entry(form_frame, width=40)
        self.entry_matricula_estudante.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(form_frame, text="Adicionar Estudante", command=self.adicionar_estudante).grid(row=2, column=0, columnspan=2, pady=10)

        list_frame = ttk.LabelFrame(self.frame_estudantes, text="Lista de Estudantes")
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree_estudantes = ttk.Treeview(list_frame, columns=("ID", "Nome", "Matrícula"), show="headings")
        self.tree_estudantes.heading("ID", text="ID")
        self.tree_estudantes.heading("Nome", text="Nome")
        self.tree_estudantes.heading("Matrícula", text="Matrícula")
        self.tree_estudantes.pack(fill="both", expand=True)
        self.atualizar_treeview_estudantes()

    def adicionar_estudante(self):
        nome = self.entry_nome_estudante.get()
        matricula = self.entry_matricula_estudante.get()
        if nome and matricula:
            try:
                db.adicionar_estudante(nome, matricula)
                messagebox.showinfo("Sucesso", "Estudante adicionado com sucesso!")
                self.entry_nome_estudante.delete(0, tk.END)
                self.entry_matricula_estudante.delete(0, tk.END)
                self.atualizar_treeview_estudantes()
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "Matrícula já existe. Por favor, use uma matrícula diferente.")
        else:
            messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")

    def atualizar_treeview_estudantes(self):
        for i in self.tree_estudantes.get_children():
            self.tree_estudantes.delete(i)
        for estudante in db.ver_estudantes():
            self.tree_estudantes.insert("", "end", values=estudante)

    def criar_aba_emprestimos(self):
        emprestimo_frame = ttk.LabelFrame(self.frame_emprestimos, text="Registrar Empréstimos/Devoluções")
        emprestimo_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(emprestimo_frame, text="Livro (Disponível):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.combo_livros = ttk.Combobox(emprestimo_frame, width=40)
        self.combo_livros.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(emprestimo_frame, text="Estudante:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.combo_estudantes = ttk.Combobox(emprestimo_frame, width=40)
        self.combo_estudantes.grid(row=1, column=1, padx=5, pady=5)

        self.notebook.bind("<<NotebookTabChanged>>", self.tab_changed)
        ttk.Button(emprestimo_frame, text="Emprestar", command=self.realizar_emprestimo).grid(row=2, column=0, columnspan=2, pady=10)

        devolucao_frame = ttk.LabelFrame(self.frame_emprestimos, text="Empréstimos Ativos")
        devolucao_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree_emprestimos = ttk.Treeview(devolucao_frame, columns=("ID", "Livro", "Estudante", "Data Empréstimo"), show="headings")
        self.tree_emprestimos.heading("ID", text="ID")
        self.tree_emprestimos.heading("Livro", text="Livro")
        self.tree_emprestimos.heading("Estudante", text="Estudante")
        self.tree_emprestimos.heading("Data Empréstimo", text="Data Empréstimo")
        self.tree_emprestimos.pack(side="left", fill="both", expand=True)
        ttk.Button(devolucao_frame, text="Devolver Livro", command=self.realizar_devolucao).pack(side="right", padx=10, pady=10)
        self.atualizar_treeview_emprestimos()

    def tab_changed(self, event):
        selected_tab = self.notebook.index(self.notebook.select())
        if selected_tab == 2:
            self.atualizar_combos_emprestimos()

    def atualizar_combos_emprestimos(self):
        livros_disponiveis = [f"{livro[0]} - {livro[1]}" for livro in db.ver_livros() if livro[4] == 'Disponível']
        self.combo_livros['values'] = livros_disponiveis
        estudantes = [f"{estudante[0]} - {estudante[1]}" for estudante in db.ver_estudantes()]
        self.combo_estudantes['values'] = estudantes

        for i in self.tree_emprestimos.get_children():
            self.tree_emprestimos.delete(i)
        for emprestimo in db.ver_emprestimos_ativos():
            self.tree_emprestimos.insert("", "end", values=emprestimo)

    def realizar_emprestimo(self):
        livro_selecionado = self.combo_livros.get()
        estudante_selecionado = self.combo_estudantes.get()
        if not livro_selecionado or not estudante_selecionado:
            messagebox.showwarning("Aviso", "Selecione um livro e um estudante")
            return
        id_livro = int(livro_selecionado.split(" - ")[0])
        id_estudante = int(estudante_selecionado.split(" - ")[0])

        try:
            db.emprestar_livro(id_livro, id_estudante)
            messagebox.showinfo("Sucesso", "Empréstimo realizado com sucesso!")
            self.atualizar_combos_emprestimos()
            self.atualizar_treeview_livros()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível realizar o empréstimo: {e}")

    def realizar_devolucao(self):
        item_selecionado = self.tree_emprestimos.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um empréstimo para devolução")
            return

        id_emprestimo = self.tree_emprestimos.item(item_selecionado, "values")[0]
        emprestimos = {str(e[0]): e for e in db.ver_emprestimos_ativos()}
        titulo_livro = emprestimos[str(id_emprestimo)][1]

        id_livro = None
        for livro in db.ver_livros():
            if livro[1] == titulo_livro:
                id_livro = livro[0]
                break
        if id_livro:
            db.devolver_livro(id_emprestimo, id_livro)
            messagebox.showinfo("Sucesso", "Devolução registrada com sucesso!")
            self.atualizar_combos_emprestimos()
            self.atualizar_treeview_livros()
        else:
            messagebox.showerror("Erro", "Não foi possível encontrar o livro associado.")

    def atualizar_treeview_emprestimos(self):
        for i in self.tree_emprestimos.get_children():
            self.tree_emprestimos.delete(i)
        for emprestimo in db.ver_emprestimos_ativos():
            self.tree_emprestimos.insert("", "end", values=emprestimo)

if __name__ == "__main__":
    app = App()
    app.mainloop()