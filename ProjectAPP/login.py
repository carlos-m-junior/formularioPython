import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk, ImageDraw, ImageOps
from tkinter import messagebox
from Banco import Banco
from Main import MainMenu as Mainform

def criar_imagem_arredondada(caminho_imagem, tamanho):
    # Carregar imagem
    imagem = Image.open(caminho_imagem)

    # Redimensionar imagem
    imagem = imagem.resize(tamanho, Image.Resampling.LANCZOS)

    # Criar máscara circular
    mascara = Image.new('L', tamanho, 0)
    draw = ImageDraw.Draw(mascara)
    draw.ellipse((0, 0, tamanho[0], tamanho[1]), fill=255)

    # Aplicar máscara
    imagem = ImageOps.fit(imagem, tamanho, centering=(0.5, 0.5))
    imagem.putalpha(mascara)

    return imagem

class Login:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Login")

        # Configuração da imagem arredondada
        try:
            imagem_arredondada = criar_imagem_arredondada("imagem/711769.png", (250, 250))  # Aumentei o tamanho da imagem
            imagem_tk = ImageTk.PhotoImage(imagem_arredondada)

            self.label_imagem = Label(master, image=imagem_tk)
            self.label_imagem.image = imagem_tk  # Mantém uma referência à imagem
            self.label_imagem.pack(pady=20)  # Aumentei o padding para um espaçamento maior
        except IOError:
            print("Imagem 'imagem/711769.png' não encontrada.")
            self.label_imagem = Label(master, text="Imagem não encontrada")
            self.label_imagem.pack(pady=20)

        # Frame para usuário
        self.janela40 = Frame(master)
        self.janela40.pack(pady=10)

        self.usuario_label = Label(self.janela40, text="Usuário:", font=("Arial", 14))
        self.usuario_label.pack(side="left")
        self.usuario = Entry(self.janela40, width=30, font=("Arial", 14))  # Aumentei a largura e o tamanho da fonte
        self.usuario.pack(side="left")

        # Frame para senha
        self.janela41 = Frame(master)
        self.janela41.pack(pady=10)

        self.senha_label = Label(self.janela41, text="Senha:", font=("Arial", 14))
        self.senha_label.pack(side="left")
        self.senha = Entry(self.janela41, width=30, font=("Arial", 14), show="*")  # Aumentei a largura e o tamanho da fonte
        self.senha.pack(side="left")

        # Frame para o botão de login
        self.janela42 = Frame(master)
        self.janela42.pack(pady=20)

        self.botao10 = Button(self.janela42, width=15, text="Login", font=("Arial", 14), command=self.entrar)  # Aumentei a largura e o tamanho da fonte
        self.botao10.pack()

    def entrar(self):
        usuario = self.usuario.get()
        senha = self.senha.get()

        banco = Banco()
        cursor = banco.conexao.cursor()

        cursor.execute("SELECT * FROM tbl_usuarios WHERE usuario=? AND senha=?", (usuario, senha))
        engual = cursor.fetchone()

        if engual:
            messagebox.showinfo("Login", "Login realizado com sucesso!")
            self.abrir()
            self.master.destroy()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")
        cursor.close()

    def abrir(self):
        self.master.withdraw()  # Esconde a janela de login
        self.new_window = tk.Toplevel(self.master)
        self.app = Mainform(self.new_window)

if __name__ == "__main__":
    root = Tk()
    root.geometry("600x400")  # Ajustei o tamanho da janela principal para melhor adaptação
    root.resizable(False, False)  # Impede o redimensionamento da janela
    root.eval('tk::PlaceWindow . center')  # Centraliza a janela
    app = Login(master=root)
    root.mainloop()
