from atexit import register
from cgitb import text
from email.mime import application
from operator import length_hint
from tkinter import messagebox
import customtkinter as ctk
import sqlite3
import random
from tkinter import *
#from PIL import Image, ImageTk
from PIL import Image
#from tkinter import BitmapImage
import Database
import re 

janela = ctk.CTk()

def validate_email(email):
    return '@' in email

def validate_password(password):
    return len(password) >= 6 and any(c.isupper() for c in password) and any(c.islower() for c in password) and any(c.isdigit() for c in password)

def validate_username(username):
    return len(username) >= 6

def validate_confirm_password(password, confirm_password):
    return password == confirm_password

class Application():
    def __init__(self):
        self.janela = janela
        self.username_entry = None
        self.password_entry = None
        self.tema()
        self.tela()
        self.tela_login()
        janela.mainloop()

    def tema(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

    def tela(self):
        janela.geometry("1200x600")
        janela.title("Sistema de login")
        janela.resizable(False, False)

    def tela_login(self):
        # Adicionando uma imagem
        try:
            self.img = ctk.CTkImage(Image.open("tech_house-removebg-preview.png"), size=(800, 800))  # Substitua "sua_imagem.png" pelo nome do arquivo da sua imagem
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar a imagem: {e}")
            return

        # Adicionando a imagem no frame
        img_label = ctk.CTkLabel(master=janela, image=self.img, text="")  # text="" remove qualquer texto padrão
        img_label.place(x=0, y=-100)  # Posicione a imagem conforme necessário

        login_frame = ctk.CTkFrame(master=janela, width=350, height=396)
        login_frame.pack(side=ctk.RIGHT, padx=20)

        label = ctk.CTkLabel(master=login_frame, text="Sistema de Login", font=("Roboto", 20))
        label.place(x=25, y=5)
        
        self.username_entry = ctk.CTkEntry(master=login_frame, placeholder_text="*Nome de usuário", width=300, font=("Roboto", 14))
        self.username_entry.place(x=25, y=105)

        self.password_entry = ctk.CTkEntry(master=login_frame, placeholder_text="*Senha de usuário", width=300, font=("Roboto", 14), show="*")
        self.password_entry.place(x=25, y=145)

        def login():
            username = self.username_entry.get()
            password = self.password_entry.get()

            if not username or not password:
                messagebox.showerror(title="Login", message="Os campos obrigatórios devem ser preenchidos.")
            else:
                # Conectar ao banco de dados
                try:
                    conn = sqlite3.connect("Dados.db")
                    cursor = conn.cursor()

                    # Verificar se o usuário e senha existem na tabela
                    cursor.execute("SELECT * FROM users WHERE Username=? AND Password=?", (username, password))
                    row = cursor.fetchone()

                    if row:
                        messagebox.showinfo(title="Login", message="Login feito com sucesso.")
                        self.open_home_page()  # Chama a função para abrir a página principal após o login

                    else:
                        messagebox.showerror(title="Login", message="Usuário ou senha incorreto.")

                except sqlite3.Error as e:
                    messagebox.showerror(title="Erro de Banco de Dados", message=f"Erro ao tentar conectar com o banco de dados: {e}")

                finally:
                    if conn:
                        conn.close()

        login_button = ctk.CTkButton(master=login_frame, text="LOGIN", width=300, command=login)
        login_button.place(x=25 , y=185)

        def tela_register():
            login_frame.pack_forget()

            rg_frame = ctk.CTkFrame(master=janela, width=350, height=396)
            rg_frame.pack(side=ctk.RIGHT)

            label = ctk.CTkLabel(master=rg_frame, text="Cadastre-se", font=("Roboto", 20))
            label.place(x=25, y=5)

            span = ctk.CTkLabel(master=rg_frame, text="Favor preencher corretamente todos os campos abaixo.", font=("Roboto", 12), text_color="white")
            span.place(x=25, y=35)

            username_entry_rg = ctk.CTkEntry(master=rg_frame, placeholder_text="*Nome de usuário", width=300, font=("Roboto", 14))
            username_entry_rg.place(x=25, y=75)
            username_info_label = ctk.CTkLabel(master=rg_frame, text="Deve ter pelo menos 6 caracteres.", font=("Roboto", 10), text_color="gray")
            username_info_label.place(x=25, y=105)

            email_entry = ctk.CTkEntry(master=rg_frame, placeholder_text="*E-mail de usuário", width=300, font=("Roboto", 14))
            email_entry.place(x=25, y=125)
            email_info_label = ctk.CTkLabel(master=rg_frame, text="Deve ser um e-mail válido.", font=("Roboto", 10), text_color="gray")
            email_info_label.place(x=25, y=155)

            password_entry_rg = ctk.CTkEntry(master=rg_frame, placeholder_text="*Senha de usuário", width=300, font=("Roboto", 14), show="*")
            password_entry_rg.place(x=25, y=175)
            password_info_label = ctk.CTkLabel(master=rg_frame, text="Deve conter ao menos uma letra maiúscula, uma minúscula, \num número e ter pelo menos 6 caracteres.", font=("Roboto", 10), text_color="gray")
            password_info_label.place(x=25, y=205)

            cPassword_entry = ctk.CTkEntry(master=rg_frame, placeholder_text="*Confirmar senha", width=300, font=("Roboto", 14), show="*")
            cPassword_entry.place(x=25, y=235)

            def back():
                rg_frame.destroy()
                login_frame.pack(side=ctk.RIGHT)

            def RegisterToDataBase():
                Username = username_entry_rg.get()
                Email = email_entry.get()
                Password = password_entry_rg.get()
                C_password = cPassword_entry.get()

                valid_username = validate_username(Username)
                valid_email = validate_email(Email)
                valid_password = validate_password(Password)
                valid_confirm_password = validate_confirm_password(Password, C_password)

                # Validando Nome de Usuário
                if not valid_username:
                    username_entry_rg.configure(border_color="red")
                    username_info_label.configure(text_color="red")
                    messagebox.showerror(title="Erro no cadastro", message="O nome de usuário deve ter pelo menos 6 caracteres.")
                    return
                else:
                    username_entry_rg.configure(border_color="green")
                    username_info_label.configure(text_color="green")

                # Validando E-mail
                if not valid_email:
                    email_entry.configure(border_color="red")
                    email_info_label.configure(text_color="red")
                    messagebox.showerror(title="Erro no cadastro", message="E-mail inválido. Deve conter '@'.")
                    return
                else:
                    email_entry.configure(border_color="green")
                    email_info_label.configure(text_color="green")

                # Validando Senha
                if not valid_password:
                    password_entry_rg.configure(border_color="red")
                    password_info_label.configure(text_color="red")
                    messagebox.showerror(title="Erro no cadastro", message="Senha inválida. Deve conter ao menos uma letra maiúscula, uma minúscula, um número e ter pelo menos 6 caracteres.")
                    return
                else:
                    password_entry_rg.configure(border_color="green")
                    password_info_label.configure(text_color="green")

                # Validando Confirmar Senha
                if not valid_confirm_password:
                    cPassword_entry.configure(border_color="red")
                    messagebox.showerror(title="Erro no cadastro", message="As senhas não correspondem.")
                    return
                else:
                    cPassword_entry.configure(border_color="green")

                # Se todas as validações passarem, proceder com o registro no banco de dados
                try:
                    conn = sqlite3.connect("Dados.db")
                    cursor = conn.cursor()

                    cursor.execute("""
                        INSERT INTO users(Username, Email, Password, ConfPassword)
                        VALUES(?, ?, ?, ?)
                        """, (Username, Email, Password, C_password))

                    conn.commit()
                    messagebox.showinfo(title="Registro", message="Conta criada com sucesso")

                    rg_frame.destroy()
                    login_frame.pack(side=ctk.RIGHT)

                except sqlite3.Error as e:
                    messagebox.showerror(title="Erro de Banco de Dados", message=f"Erro ao tentar registrar no banco de dados: {e}")

                finally:
                    if conn:
                        conn.close()

            back_button = ctk.CTkButton(master=rg_frame, text="Voltar", width=145, fg_color="gray", hover_color="#202020", command=back)
            back_button.place(x=25 , y=300)

            save_button = ctk.CTkButton(master=rg_frame, text="Registrar", width=145, fg_color="green", hover_color="#014B05", command=RegisterToDataBase)
            save_button.place(x=180 , y=300)

        register_ad = ctk.CTkLabel(master=login_frame, text="Não possui uma conta?").place(x=25 , y=225)
        register_button = ctk.CTkButton(master=login_frame, text="Cadastre-se",fg_color="green", hover_color="#014B05", width=300, command=tela_register).place(x=25 , y=250)

    def open_home_page(self):
        # Limpar todos os widgets do login_frame para ocultar a tela de login
        for widget in self.janela.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.destroy()

        self.janela.geometry("900x900")
        self.janela.title("Controle de Ambientes")
        self.janela.resizable(False, False)

        labelTitulo = ctk.CTkLabel(master=self.janela, text="Controle de Ambientes", text_color="white", font=("Roboto", 23))
        labelTitulo.place(x=300 , y=10)

        # Botão de logout
        logout_button = ctk.CTkButton(master=self.janela, text="Logout", width=100, fg_color="red", hover_color="#FF0000", command=self.logout)
        logout_button.place(x=750, y=15)

        # Rótulo para exibir status das ações
        self.status_label = ctk.CTkLabel(master=self.janela, text="", font=("Roboto", 12), text_color="gray")
        self.status_label.place(x=200, y=60)  # Ajuste a posição conforme necessário

        # Ambiente 1 - Sala de estar
        self.create_environment_frame("Sala de estar", x=450, y=100, commands=[
            ("Ar Condicionado", self.toggle_air_conditioner, random.randint(0, 1)),
            ("Lâmpada", self.toggle_lamp, random.randint(0, 1)),
            ("TV", self.toggle_tv, random.randint(0, 1)),
            ("Som", self.toggle_sound, random.randint(0, 1)),
            ("Portas/Janelas", self.close_doors_windows, random.randint(0, 1))
        ])

        # Ambiente 2 - Cozinha
        self.create_environment_frame("Cozinha", x=250, y=425, commands=[
            ("Lâmpada", self.toggle_lamp, random.randint(0, 1)),
            ("Portas/Janelas", self.close_doors_windows, random.randint(0, 1)),
            ("TV", self.toggle_tv, random.randint(0, 1))
        ])

        # Ambiente 3 - Varanda
        self.create_environment_frame("Varanda", x=50, y=425, commands=[
            ("Lâmpada", self.toggle_lamp, random.randint(0, 1)),
            ("Portas/Janelas", self.close_doors_windows, random.randint(0, 1)),
            ("Som", self.toggle_sound, random.randint(0, 1))
        ])

        # Ambiente 4 - Quarto 1
        self.create_environment_frame("Quarto 1", x=50, y=100, commands=[
            ("Ar Condicionado", self.toggle_air_conditioner, random.randint(0, 1)),
            ("Lâmpada", self.toggle_lamp, random.randint(0, 1)),
            ("TV", self.toggle_tv, random.randint(0, 1)),
            ("Som", self.toggle_sound, random.randint(0, 1)),
            ("Portas/Janelas", self.close_doors_windows, random.randint(0, 1))
        ])

        # Ambiente 5 - Quarto 2
        self.create_environment_frame("Quarto 2", x=250, y=100, commands=[
            ("Ar Condicionado", self.toggle_air_conditioner, random.randint(0, 1)),
            ("Lâmpada", self.toggle_lamp, random.randint(0, 1)),
            ("TV", self.toggle_tv, random.randint(0, 1)),
            ("Som", self.toggle_sound, random.randint(0, 1)),
            ("Portas/Janelas", self.close_doors_windows, random.randint(0, 1))
        ])

        # Ambiente 6 - Segurança
        self.create_environment_frame("Segurança", x=450, y=425, commands=[
            ("Portas/Janelas", self.close_doors_windows, random.randint(0, 1)),
            ("Cerca de Segurança", self.toggle_security_fence, random.randint(0, 1)),
            ("Ligar p/ Polícia", self.call_police, random.randint(0, 1))
        ])

        # Ambiente 7 - Banheiro
        self.create_environment_frame("Banheiro", x=650, y=100, commands=[
            ("Banheira", self.toggle_bathtub, random.randint(0, 1)),
            ("Lâmpada", self.toggle_lamp, random.randint(0, 1)),
            ("Hidromassagem", self.toggle_whirlpool, random.randint(0, 1)),
            ("Som", self.toggle_sound, random.randint(0, 1)),
            ("Portas/Janelas", self.close_doors_windows, random.randint(0, 1))
        ])

        # Ambiente 8 - Garagem
        self.create_environment_frame("Garagem", x=650, y=425, commands=[
            ("Luzes", self.toggle_garage_lights, random.randint(0, 1)),
            ("Portão", self.toggle_garage_gate, random.randint(0, 1))
        ])

        # Cenas - Novo label com cenas específicas
        self.create_scenes_frame("Cenas", x=50, y=580)

    def create_environment_frame(self, title, x, y, commands):
        frame = ctk.CTkFrame(master=self.janela, width=400, height=250)
        frame.place(x=x, y=y)

        label = ctk.CTkLabel(master=frame, text=title, font=("Roboto", 20))
        label.pack(pady=12)

        for idx, (btn_text, command, state) in enumerate(commands, start=1):
            button_color = "#4F4F4F" if state == 1 else "#4F4F4F"
            button = ctk.CTkButton(master=frame, text=btn_text, width=120, fg_color=button_color, command=lambda text=f"Comando ligar/desligar ou abrir/fechar para {btn_text.lower()} para o cômodo {title}": self.update_status(text))
            button.pack(pady=12)

    def create_scenes_frame(self, title, x, y):
        frame = ctk.CTkFrame(master=self.janela, width=800, height=250)
        frame.place(x=x, y=y)

        label = ctk.CTkLabel(master=frame, text=title, font=("Roboto", 20))
        label.pack(pady=12)

        # Definição das cenas divididas em duas colunas
        scenes = [
            ("Chegar em casa", "Portão da garagem aberto e lâmpadas acesas.", self.scene_arrive_home),
            ("Sair de casa", "Gás fechado, portas/janelas fechadas e apagar as luzes.", self.scene_leave_home),
            ("Dormir", "Portas/janelas fechadas e apagar as luzes.", self.scene_sleep),
            ("Dia quente", "Ar condicionado ligado nos quartos e abrir as janelas do restante da casa.", self.scene_hot_day),
            ("Dia frio", "Aquecedor ligado e janelas fechadas.", self.scene_cold_day),
            ("Banho", "Luz do banheiro acesa e banheira ligada.", self.scene_bath)
        ]

        # Dividindo as cenas em duas colunas
        column1 = ctk.CTkFrame(master=frame, width=400, height=250)
        column1.pack(side=ctk.LEFT, padx=10)

        column2 = ctk.CTkFrame(master=frame, width=400, height=250)
        column2.pack(side=ctk.LEFT, padx=10)

        for i, (scene_title, scene_description, scene_function) in enumerate(scenes):
            if i < len(scenes) // 2:
                button = ctk.CTkButton(master=column1, text=scene_title, width=340, command=lambda text=scene_description: self.update_status(text))
            else:
                button = ctk.CTkButton(master=column2, text=scene_title, width=340, command=lambda text=scene_description: self.update_status(text))
            button.pack(pady=6)

    def scene_arrive_home(self):
        self.update_status("Portão da garagem aberto e lâmpadas acesas.")

    def scene_leave_home(self):
        self.update_status("Gás fechado, portas/janelas fechadas e apagar as luzes.")

    def scene_sleep(self):
        self.update_status("Portas/janelas fechadas e apagar as luzes.")

    def scene_hot_day(self):
        self.update_status("Ar condicionado ligado nos quartos e abrir as janelas do restante da casa.")

    def scene_cold_day(self):
        self.update_status("Aquecedor ligado e janelas fechadas.")

    def scene_bath(self):
        self.update_status("Luz do banheiro acesa e banheira ligada.")

    def update_status(self, text):
        self.status_label.configure(text=text)

    def toggle_air_conditioner(self):
        # Implementar lógica para ativar/desativar o ar condicionado
        pass

    def toggle_lamp(self):
        # Implementar lógica para ligar/desligar a lâmpada
        pass

    def toggle_tv(self):
        # Implementar lógica para ligar/desligar a TV
        pass

    def toggle_sound(self):
        # Implementar lógica para ligar/desligar o som
        pass

    def close_doors_windows(self):
        # Implementar lógica para fechar portas e janelas
        pass

    def toggle_security_fence(self):
        # Implementar lógica para ativar/desativar a cerca de segurança
        pass

    def call_police(self):
        # Implementar lógica para ligar para a polícia
        pass

    def toggle_bathtub(self):
        # Implementar lógica para ligar/desligar a banheira
        self.update_status("Comando para ligar/desligar a banheira")

    def toggle_whirlpool(self):
        # Implementar lógica para ligar/desligar a hidromassagem
        self.update_status("Comando para ligar/desligar a hidromassagem")

    def toggle_garage_lights(self):
        # Implementar lógica para ligar/desligar as luzes da garagem
        self.update_status("Comando para ligar/desligar as luzes da garagem")

    def toggle_garage_gate(self):
        # Implementar lógica para abrir/fechar o portão da garagem
        self.update_status("Comando para abrir/fechar o portão da garagem")

    def logout(self):
        # Limpar todos os widgets da HomePage para voltar à tela de login
        for widget in self.janela.winfo_children():
            widget.destroy()

        self.username_entry = None
        self.password_entry = None
        self.tema()
        self.tela()
        self.tela_login()

if __name__ == "__main__":
    Application()