import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import json

# Функция для показа стартового экрана
def show_start_screen():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Библиотечная система", font=("Helvetica", 16, "bold")).pack(pady=10)
    tk.Button(root, text="Выдать книгу", command=issue_book, width=20).pack(pady=5)
    tk.Button(root, text="Вернуть книгу", command=return_book, width=20).pack(pady=5)
    tk.Button(root, text="Список выданных книг", command=show_issued_books, width=20).pack(pady=5)

# Функция для выдачи книги
def issue_book():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Выдача книги", font=("Helvetica", 14, "bold")).pack(pady=10)

    # Выбор книги
    tk.Label(root, text="Выберите книгу для выдачи:").pack()
    try:
        with open('book.json', 'r', encoding='utf-8') as f:
            books = json.load(f)
    except FileNotFoundError:
        tk.Label(root, text="Файл с книгами не найден или пуст").pack()
        return

    book_var = tk.StringVar(root)
    book_var.set("Выберите книгу")
    book_dropdown = ttk.Combobox(root, textvariable=book_var, values=[f"{book['Код книги']} - {book['Название']} - {book['Залоговая стоимость']} - {book['Стоимость проката']}" for book in books])
    book_dropdown.pack(pady=5)

    # Выбор читателя
    tk.Label(root, text="Выберите читателя:").pack()
    try:
        with open('readers.json', 'r', encoding='utf-8') as f:
            readers = json.load(f)
    except FileNotFoundError:
        tk.Label(root, text="Файл с читателями не найден или пуст").pack()
        return

    reader_var = tk.StringVar(root)
    reader_var.set("Выберите читателя")
    reader_dropdown = ttk.Combobox(root, textvariable=reader_var, values=[f"{reader['Код читателя']} - {reader['Фамилия']} {reader['Имя']} {reader['Отчество']}" for reader in readers])
    reader_dropdown.pack(pady=5)

    # Поле для выбора даты выдачи
    tk.Label(root, text="Выберите дату выдачи:").pack()
    issue_date_calendar = Calendar(root, selectmode='day', date_pattern='dd.mm.yyyy')
    issue_date_calendar.pack(pady=5)

    # Поле для выбора даты возврата
    tk.Label(root, text="Выберите ожидаемую дату возврата:").pack()
    return_date_calendar = Calendar(root, selectmode='day', date_pattern='dd.mm.yyyy')
    return_date_calendar.pack(pady=5)

    def confirm_issue():
        selected_book = book_var.get().split(" - ")[0]
        selected_reader = reader_var.get().split(" - ")[0]
        issue_date = issue_date_calendar.get_date()
        return_date = return_date_calendar.get_date()

        # Удаление книги из списка книг
        updated_books = [book for book in books if book['Код книги'] != selected_book]
        with open('book.json', 'w', encoding='utf-8') as f:
            json.dump(updated_books, f, ensure_ascii=False, indent=4)

        # Запись информации о выдаче книги
        try:
            with open('issued_books.json', 'r', encoding='utf-8') as f:
                issued_books = json.load(f)
        except FileNotFoundError:
            issued_books = []

        issued_books.append({
            'Код книги': selected_book,
            'Код читателя': selected_reader,
            'Дата выдачи': issue_date,
            'Ожидаемая дата возврата': return_date
        })

        with open('issued_books.json', 'w', encoding='utf-8') as f:
            json.dump(issued_books, f, ensure_ascii=False, indent=4)

        show_start_screen()

    tk.Button(root, text="Подтвердить выдачу", command=confirm_issue, width=20).pack(pady=5)
    tk.Button(root, text="Отмена", command=show_start_screen, width=20).pack(pady=5)

# Функция для возврата книги
def return_book():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Возврат книги", font=("Helvetica", 14, "bold")).pack(pady=10)
    tk.Label(root, text="Выберите книгу для возврата:").pack()

    try:
        with open('issued_books.json', 'r', encoding='utf-8') as f:
            issued_books = json.load(f)
        if not issued_books:
            tk.Label(root, text="Список выданных книг пуст").pack()
            tk.Button(root, text="Возврат в предыдущее меню", command=show_start_screen, width=20).pack(pady=5)
            return
    except FileNotFoundError:
        tk.Label(root, text="Файл с выданными книгами не найден или пуст").pack()
        tk.Button(root, text="Возврат в предыдущее меню", command=show_start_screen, width=20).pack(pady=5)
        return

    book_var = tk.StringVar(root)
    book_var.set("Выберите книгу")
    book_dropdown = ttk.Combobox(root, textvariable=book_var, values=[f"{book['Код книги']} - {book['Код читателя']} - {book['Дата выдачи']} - {book['Ожидаемая дата возврата']}" for book in issued_books])
    book_dropdown.pack(pady=5)

    def confirm_return():
        selected_book_code = book_var.get().split(" - ")[0]

        # Найти книгу в списке выданных книг
        returned_book = next((book for book in issued_books if book['Код книги'] == selected_book_code), None)
        if returned_book:
            issued_books.remove(returned_book)

            # Сохранить обновленный список выданных книг
            with open('issued_books.json', 'w', encoding='utf-8') as f:
                json.dump(issued_books, f, ensure_ascii=False, indent=4)

            # Вернуть книгу в список всех книг
            try:
                with open('book.json', 'r', encoding='utf-8') as f:
                    books = json.load(f)
            except FileNotFoundError:
                books = []

            books.append({
                'Код книги': returned_book['Код книги'],
                'Название': 'Название книги',  # Здесь нужно указать название книги
                'Залоговая стоимость': 'Залоговая стоимость',  # Здесь нужно указать залоговую стоимость
                'Стоимость проката': 'Стоимость проката'  # Здесь нужно указать стоимость проката
            })

            with open('book.json', 'w', encoding='utf-8') as f:
                json.dump(books, f, ensure_ascii=False, indent=4)

        show_start_screen()

    tk.Button(root, text="Подтвердить возврат", command=confirm_return, width=20).pack(pady=5)
    tk.Button(root, text="Отмена", command=show_start_screen, width=20).pack(pady=5)

# Функция для вывода списка выданных книг
def show_issued_books():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Список выданных книг", font=("Helvetica", 14, "bold")).pack(pady=10)

    try:
        with open('issued_books.json', 'r', encoding='utf-8') as f:
            issued_books = json.load(f)
        if not issued_books:
            tk.Label(root, text="Список выданных книг пуст").pack()
        else:
            for issued_book in issued_books:
                tk.Label(root, text=f"Код книги: {issued_book['Код книги']}, Код читателя: {issued_book['Код читателя']}, Дата выдачи: {issued_book['Дата выдачи']}, Ожидаемая дата возврата: {issued_book['Ожидаемая дата возврата']}").pack()
    except FileNotFoundError:
        tk.Label(root, text="Файл с выданными книгами не найден или пуст").pack()

    tk.Button(root, text="Возврат в предыдущее меню", command=show_start_screen, width=20).pack(pady=5)

# Создание основного окна приложения
root = tk.Tk()
root.title("Библиотечная система")
root.geometry('400x500')

show_start_screen()

root.mainloop()
