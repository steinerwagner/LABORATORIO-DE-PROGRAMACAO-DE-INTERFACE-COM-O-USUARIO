import tkinter
from tkinter import messagebox
import sqlite3

#Conecta ao banco de dados SQLite
conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

#Cria a tabela de usuários se ela não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        email TEXT PRIMARY KEY,
        senha TEXT
    )
''')

#Cria a tabela de usuários se ela não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS itens (
        email TEXT,
        item TEXT,
        FOREIGN KEY (email) REFERENCES usuarios (email)
    )
''')

def cadastrar_usuario():
    email_text = email_usuario.get()
    senha_text = senha_usuario.get()

    if email_text == "" or senha_text == "":
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
    else:
        #Inseri usuário no banco de dados
        cursor.execute('INSERT INTO usuarios VALUES (?, ?)', (email_text, senha_text))
        conn.commit()

        messagebox.showinfo("Cadastro de Usuário", "Usuário cadastrado com sucesso!")
        email_usuario.delete(0, tkinter.END)
        senha_usuario.delete(0, tkinter.END)

def fazer_login():
    email_text = email_usuario.get()
    senha_text = senha_usuario.get()

    #Consulta o banco de dados para verificar o login
    cursor.execute('SELECT * FROM usuarios WHERE email=? AND senha=?', (email_text, senha_text))
    resultado = cursor.fetchone()

    if resultado:
        messagebox.showinfo("Login", "Login realizado com sucesso!")
        janela_login.destroy()
        abrir_janela_cadastro_voos(email_text)  
    #Passando o email do usuário para a função
    else:
        messagebox.showerror("Login", "E-mail ou senha inválidos.")

def abrir_janela_cadastro_voos(email):
    janela_cadastro_voos = tkinter.Toplevel()
    janela_cadastro_voos.geometry("300x500")

    voos = []

    def adicionar_voo():
        novo_voo = voo.get()
        if novo_voo:
            voos.append(novo_voo)
            messagebox.showinfo("Cadastro de Voos", "Voo adicionado com sucesso!")
            atualizar_listbox()
            voo.delete(0, tkinter.END)

            # Inserir item no banco de dados
            cursor.execute('INSERT INTO itens VALUES (?, ?)', (email, novo_voo))
            conn.commit()
        else:
            messagebox.showerror("Erro", "Por favor, insira um Voo.")

    def editar_voo():
        indice_selecionado = listbox.curselection()
        if indice_selecionado:
            novo_voo = voo.get()
            if novo_voo:
                voos[indice_selecionado[0]] = novo_voo
                messagebox.showinfo("Cadastro de Voos", "Voo atualizado com sucesso!")
                atualizar_listbox()
                voo.delete(0, tkinter.END)

                # Atualizar item no banco de dados
                cursor.execute('UPDATE itens SET item=? WHERE email=?', (novo_voo, email))
                conn.commit()
            else:
                messagebox.showerror("Erro", "Por favor, insira um Voo.")
        else:
            messagebox.showerror("Erro", "Nenhum Voo selecionado.")

    def excluir_voo():
        indice_selecionado = listbox.curselection()
        if indice_selecionado:
            resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir o Voo selecionado?")
            if resposta:
                voos.pop(indice_selecionado[0])
                messagebox.showinfo("Cadastro de Voos", "Voo excluído com sucesso!")
                atualizar_listbox()
                voo.delete(0, tkinter.END)

                # Excluir item do banco de dados
                cursor.execute('DELETE FROM itens WHERE email=? AND item=?', (email, listbox.get(indice_selecionado[0])))
                conn.commit()
        else:
            messagebox.showerror("Erro", "Nenhum item Voo selecionado.")

    def atualizar_listbox():
        listbox.delete(0, tkinter.END)
        for voo in voos:
            listbox.insert(tkinter.END, voo)

    texto_cadastro_voos = tkinter.Label(janela_cadastro_voos, text="Cadastro de Voos", font=("Arial", 25))
    texto_cadastro_voos.pack(padx=10, pady=10)

    frame = tkinter.Frame(janela_cadastro_voos)
    frame.pack(padx=10, pady=10)

    label_voo = tkinter.Label(frame, text="Voo:", font=("Arial", 15))
    label_voo.grid(row=0, column=0, padx=5, pady=5)

    voo = tkinter.Entry(frame)
    voo.grid(row=0, column=1, padx=5, pady=5)

    botao_adicionar = tkinter.Button(janela_cadastro_voos, text="Adicionar", command=adicionar_voo)
    botao_adicionar.pack(padx=10, pady=5)

    botao_editar = tkinter.Button(janela_cadastro_voos, text="Editar", command=editar_voo)
    botao_editar.pack(padx=10, pady=5)

    botao_excluir = tkinter.Button(janela_cadastro_voos, text="Excluir", command=excluir_voo)
    botao_excluir.pack(padx=10, pady=5)

    listbox = tkinter.Listbox(janela_cadastro_voos)
    listbox.pack(padx=10, pady=5)

    scrollbar = tkinter.Scrollbar(janela_cadastro_voos)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    # Carregar itens do banco de dados
    cursor.execute('SELECT item FROM itens WHERE email=?', (email,))
    itens_bd = cursor.fetchall()
    for item_bd in itens_bd:
        voos.append(item_bd[0])

    atualizar_listbox()

janela_login = tkinter.Tk()
janela_login.geometry("500x300")

texto_login = tkinter.Label(janela_login, text="Aeroporto Municipal de Maricá", font=("Arial", 25))
texto_login.pack(padx=10, pady=10)

frame_login = tkinter.Frame(janela_login)
frame_login.pack(padx=10, pady=10)

label_email = tkinter.Label(frame_login, text="E-mail:", font=("Arial", 15))
label_email.grid(row=0, column=0, padx=5, pady=5)

email_usuario = tkinter.Entry(frame_login)
email_usuario.grid(row=0, column=1, padx=5, pady=5)

label_senha = tkinter.Label(frame_login, text="Senha:", font=("Arial", 15))
label_senha.grid(row=1, column=0, padx=5, pady=5)

senha_usuario = tkinter.Entry(frame_login, show="*")
senha_usuario.grid(row=1, column=1, padx=5, pady=5)

botao_cadastrar_usuario = tkinter.Button(janela_login, text="Cadastrar Usuário", command=cadastrar_usuario)
botao_cadastrar_usuario.pack(padx=10, pady=5)

botao_login = tkinter.Button(janela_login, text="Login", command=fazer_login)
botao_login.pack(padx=10, pady=5)

janela_login.mainloop()

#Fechar a conexão com o banco de dados quando a janela principal for fechada.
conn.close()


