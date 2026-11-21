import tkinter as tk
from tkinter import ttk, messagebox

import psycopg2

from database import authorize_user


class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Warehouse")
        self.root.geometry("1000x650")
        self.root.minsize(750, 500)

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

        style.configure("Treeview", rowheight=28, font=("Arial", 10))
        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold"),
        )

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # -------------------- Окно входа --------------------

    def show_login(self):
        self.clear_window()

        container = ttk.Frame(self.root, padding=30)
        container.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(
            container,
            text="Вход в систему",
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
            text="Авторизация",
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
        login = self.login_entry.get().strip()
        password = self.password_entry.get()

        if not login or not password:
            messagebox.showwarning(
                "Пустые поля",
                "Введите логин и пароль.",
            )
            return

        try:
            user = authorize_user(login, password)
        except psycopg2.Error as error:
            messagebox.showerror(
                "Ошибка PostgreSQL",
                f"Не удалось выполнить авторизацию.\n\n{error}",
            )
            return

        if user is None:
            messagebox.showerror(
                "Ошибка авторизации",
                "Неверный логин или пароль.",
            )
            return

        self.show_user(user)

    # -------------------- Личный кабинет --------------------

    def show_user(self, user):
        self.clear_window()
        self.root.unbind("<Return>")

        header = ttk.Frame(self.root, padding=(20, 18))
        header.pack(fill="x")

        ttk.Label(
            header,
            text=f"Добро пожаловать, {user['name']}!",
            font=("Arial", 20, "bold"),
        ).pack(side="left")

        ttk.Button(
            header,
            text="Выйти",
            command=self.show_login,
        ).pack(side="right")

        info = ttk.LabelFrame(
            self.root,
            text="Информация о пользователе",
            padding=15,
        )
        info.pack(fill="x", padx=20, pady=(0, 15))

        details = ttk.Frame(info)
        details.pack(fill="x")

        self.add_user_detail(details, "Имя", user["name"], 0)
        self.add_user_detail(details, "Возраст", user["age"], 1)
        self.add_user_detail(details, "Почта", user["email"], 2)

        self.create_products_table()

    def add_user_detail(self, parent, title, value, column):
        item = ttk.Frame(parent)
        item.grid(row=0, column=column, sticky="w", padx=(0, 35))

        ttk.Label(item, text=title, foreground="gray").pack(anchor="w")
        ttk.Label(
            item,
            text=str(value) if value is not None else "Не указано",
            font=("Arial", 11, "bold"),
        ).pack(anchor="w", pady=(3, 0))

    # -------------------- Гостевой режим --------------------

    def show_guest(self):
        self.clear_window()
        self.root.unbind("<Return>")

        header = ttk.Frame(self.root, padding=(20, 18))
        header.pack(fill="x")

        ttk.Label(
            header,
            text="Список товаров",
            font=("Arial", 20, "bold"),
        ).pack(side="left")

        ttk.Button(
            header,
            text="Назад",
            command=self.show_login,
        ).pack(side="right")

        self.create_products_table()

    # -------------------- Таблица товаров --------------------

    def create_products_table(self):
        table_frame = ttk.Frame(self.root, padding=(20, 5, 20, 20))
        table_frame.pack(fill="both", expand=True)

        columns = ("id", "name", "category", "price", "quantity")

        self.products_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
        )

        headings = {
            "id": "ID",
            "name": "Название товара",
            "category": "Категория",
            "price": "Цена",
            "quantity": "Количество",
        }

        widths = {
            "id": 60,
            "name": 280,
            "category": 200,
            "price": 130,
            "quantity": 130,
        }

        for column in columns:
            self.products_table.heading(column, text=headings[column])
            self.products_table.column(
                column,
                width=widths[column],
                anchor="center" if column != "name" else "w",
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.products_table.yview,
        )
        self.products_table.configure(yscrollcommand=scrollbar.set)

        self.products_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
