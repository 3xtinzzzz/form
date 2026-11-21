import tkinter as tk
from tkinter import ttk, messagebox

import psycopg2

from database import authorize_user


class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("App")
        self.root.geometry("1920x1080")
        self.root.minsize(650, 450)
        self.login_entry = None
        self.password_entry = None
        self.configure_style()
        self.show_login()
    def configure_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TButton", padding=8)
        style.configure("TLabel", font=("Arial", 11))
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
    #авторизация
    def show_login(self):
        self.clear_window()
        container = ttk.Frame(self.root, padding=30)
        container.place(relx=0.5, rely=0.5, anchor="center")
        ttk.Label(
            container,
            text="Авторизация",
            font=("Arial", 22, "bold"),
        ).pack(pady=(0, 25))
        ttk.Label(container, text="Логин").pack(anchor="w")
        self.login_entry = ttk.Entry(container, width=32, font=("Arial", 12))
        self.login_entry.pack(pady=(5, 15))

        ttk.Label(container, text="Пароль").pack(anchor="w")
        self.password_entry = ttk.Entry(
            container,
            width=32,
            font=("Arial", 12),
            show="*",
        )
        self.password_entry.pack(pady=(5, 20))
        ttk.Button(
            container,
            text="Войти",
            command=self.login,
        ).pack(fill="x", pady=5)

        ttk.Button(
            container,
            text="Войти как гость",
            command=self.show_guest,
        ).pack(fill="x", pady=5)

        self.login_entry.focus_set()
        self.root.bind("<Return>", self.on_enter)
    def on_enter(self, _event):
        if self.login_entry is not None:
            self.login()
    def login(self):
        username = self.login_entry.get().strip()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showwarning(
                "Пустые поля",
                "Введите логин и пароль.",
            )
            return

        try:
            user = authorize_user(username, password)
        except psycopg2.Error as error:
            messagebox.showerror(
                "Ошибка PostgreSQL",
                f"ошибка\n\n{error}",
            )
            return

        if user is None:
            messagebox.showerror(
                "Ошибка авторизации",
                "Неверный логин или пароль.",
            )
            return
        self.show_user(user)

    def show_user(self, user):
        self.clear_window()
        self.root.unbind("<Return>")

        header = ttk.Frame(self.root, padding=(25, 20))
        header.pack(fill="x")

        ttk.Label(
            header,
            text=f"Добро пожаловать, {user['name']}!",
            font=("Arial", 20, "bold"),
        ).pack(anchor="w")

        ttk.Label(
            header,
            text=f"Ваша роль: {user['role']}",
            font=("Arial", 12),
        ).pack(anchor="w", pady=(8, 0))

        self.create_feed_placeholder()

        ttk.Button(
            self.root,
            text="Выйти",
            command=self.show_login,
        ).pack(anchor="e", padx=25, pady=15)
        
    #гость
    def show_guest(self):
        self.clear_window()
        self.root.unbind("<Return>")
        header = ttk.Frame(self.root, padding=(25, 20))
        header.pack(fill="x")
        ttk.Label(
            header,
            text="Гостевой режим",
            font=("Arial", 20, "bold"),
        ).pack(anchor="w")
        self.create_feed_placeholder()

        ttk.Button(
            self.root,
            text="Назад",
            command=self.show_login,
        ).pack(anchor="e", padx=25, pady=15)

    #товары
    def create_feed_placeholder(self):
        feed = ttk.LabelFrame(
            self.root,
            text="Лента товаров",
            padding=20,
        )
        feed.pack(fill="both", expand=True, padx=25, pady=10)

        ttk.Label(
            feed,
            text="Тут будет лента товаров",
            font=("Arial", 16),
            foreground="gray",
        ).place(relx=0.5, rely=0.5, anchor="center")
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
