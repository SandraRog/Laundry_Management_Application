import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkcalendar import Calendar
import pandas as pd
import matplotlib.pyplot as plt
import io
import os
import csv
from tkinter import messagebox

# Słownik przypisujący cenę do każdego rodzaju rzeczy
prices = {
    "derka zimowa": 40.00,
    "derka zimowa+": 45.00,
    "derka zimowa++": 50.00,
    "derka przejściowa": 35.00,
    "derka polarowa": 25.00,
    "derka plandeka": 30.00,
    "czaprak": 15.00,
    "ochraniacze": 15.00,
    "owijki": 12.00,
    "podkładka": 20.00,
    "legowisko dla psa": 40.00,
    "inne": None  # Użytkownik wpisuje ręcznie
}

payment_list = {
    "Opłacone": "opłacone",
    "Nieopłacone": "nieopłacone"
}

# Funkcja do wczytywania klientów z pliku CSV
def load_clients():
    if not os.path.exists('clients.csv'):
        return []  # Jeśli plik nie istnieje, zwróć pustą listę

    with open('clients.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        return [row[0] for row in reader]  # Wczytaj tylko nazwiska klientów


# Funkcja do zapisywania nowego klienta
def save_client(client):
    if client and client not in combobox_client['values']:  # Dodaj, jeśli klient nie jest już w bazie
        with open('clients.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([client])


# Funkcja do analizy danych z CSV i tworzenia wykresu
def analyze_data():
    if not os.path.exists('laundry.csv'):
        messagebox.showerror("Błąd", "Plik CSV nie istnieje.")
        return

    try:
        # Wczytanie danych z pliku CSV z różnymi kodowaniami
        my_data = pd.read_csv("laundry.csv", header=None, names=['Klient', 'Rzecz', 'Ilość', 'Cena', 'Data', 'Suma PLN', 'Status opłacenia'], encoding='utf-8')
    except UnicodeDecodeError:
        my_data = pd.read_csv("laundry.csv", header=None, names=['Klient', 'Rzecz', 'Ilość', 'Cena', 'Data', 'Suma PLN', 'Status opłacenia'], encoding='windows-1250')

    # Grupowanie danych na podstawie kolumny 'Rzecz' i sumowanie ich ilości
    grouped_data = my_data.groupby('Rzecz')['Ilość'].sum()

    # Grupowanie danych na podstawie kolumny 'Klient', 'Suma PLN'
    grouped_data2 = my_data.groupby('Suma PLN').sum()

    # Tworzenie wykresu kołowego
    plt.figure(figsize=(8, 8))  # Ustawienie rozmiaru wykresu
    plt.pie(grouped_data, labels=grouped_data.index, autopct='%1.1f%%', startangle=90)
    plt.title('Najczęściej oddawane rzeczy do prania')
    plt.axis('equal')  # Ustawienie równych osi, aby wykres był kołem
    plt.show()

    # Obliczanie podsumowań: łączna ilość rzeczy i zarobki
    total_items = my_data['Ilość'].sum()
    total_earnings = my_data['Suma PLN'].sum()

    messagebox.showinfo("Podsumowanie", f"Łączna liczba rzeczy: {total_items}\nŁączne zarobki: {total_earnings} zł")
# Funkcja do analizy danych z CSV i tworzenia wykresu

def analyze_data2():
    if not os.path.exists('laundry.csv'):
        messagebox.showerror("Błąd", "Plik CSV nie istnieje.")
        return

    try:
        # Wczytanie danych z pliku CSV z różnymi kodowaniami
        my_data = pd.read_csv("laundry.csv", header=None, names=['Klient', 'Rzecz', 'Ilość', 'Cena', 'Data', 'Suma PLN', 'Status opłacenia'], encoding='utf-8')
    except UnicodeDecodeError:
        my_data = pd.read_csv("laundry.csv", header=None, names=['Klient', 'Rzecz', 'Ilość', 'Cena', 'Data', 'Suma PLN', 'Status opłacenia'], encoding='windows-1250')

    # Grupowanie danych na podstawie kolumny 'Klient', 'Suma PLN'
    grouped_data2 = my_data.groupby('Klient')['Suma PLN'].sum()

    # Funkcja formatowania do wyświetlania wartości w PLN
    def format_currency(value):
        return f'{value:.2f} PLN'

    # Tworzenie wykresu kołowego
    plt.figure(figsize=(8, 8))  # Ustawienie rozmiaru wykresu
    plt.pie(grouped_data2, labels=grouped_data2.index, autopct=lambda p: format_currency(p * sum(grouped_data2) / 100), startangle=90)
    plt.title('Suma PLN na klienta')
    plt.axis('equal')  # Ustawienie równych osi, aby wykres był kołem
    plt.show()


# Funkcja do automatycznego ustawienia ceny na podstawie wybranego rodzaju rzeczy
def set_price(event):
    selected_thing = combobox_thing.get()
    if selected_thing in prices and prices[selected_thing] is not None:
        entry_price.delete(0, tk.END)  # Wyczyść pole
        entry_price.insert(0, prices[selected_thing])  # Wstaw odpowiednią cenę
    elif selected_thing == "inne":
        entry_price.delete(0, tk.END)  # Użytkownik wpisuje cenę ręcznie


# Funkcja do dodawania prania do pliku CSV
def add_laundry():
    client = combobox_client.get()  # Get selected client from combobox
    thing = combobox_thing.get()  # Get selected thing from combobox
    payment = combobox_payment.get()

    try:
        quantity = int(entry_quantity.get())
        price = float(entry_price.get())
        date = entry_date.get()

        if not client or not thing or not date:
            raise ValueError("Wszystkie pola muszą być wypełnione!")

        # Obliczenie całkowitej kwoty za daną rzecz
        total_price = quantity * price

        # Dodanie danych do pliku CSV z kodowaniem UTF-8
        with io.open('laundry.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([client, thing, quantity, price, date, total_price, payment])

        messagebox.showinfo("Sukces",
                            f"Dane dodane: {client}, {thing}, {quantity} szt., {price} zł/szt, {date}, Razem: {total_price} zł, Płatność {payment}")

        # Zapisz nowego klienta do bazy klientów
        save_client(client)

        # Odśwież listę klientów w Combobox
        combobox_client['values'] = load_clients()

        # Wyświetlenie danych
        show_data()  # Wywołanie funkcji po dodaniu danych

        # Wyczyść pola po dodaniu danych
        combobox_client.set('')  # Reset selected client
        combobox_thing.set('')  # Reset selected thing
        combobox_payment.set('')
        entry_quantity.delete(0, tk.END)
        entry_price.delete(0, tk.END)
        entry_date.delete(0, tk.END)
        set_today_date()

    except ValueError as ve:
        messagebox.showerror("Błąd", str(ve))


# Funkcja do ustawienia dzisiejszej daty
def set_today_date():
    today = datetime.now().strftime("%Y-%m-%d")
    entry_date.delete(0, tk.END)
    entry_date.insert(0, today)


# Funkcja do wyboru daty z kalendarza
def open_calendar():
    def select_date():
        selected_date = cal.selection_get().strftime("%Y-%m-%d")
        entry_date.delete(0, tk.END)
        entry_date.insert(0, selected_date)
        top.destroy()

    top = tk.Toplevel(root)
    cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(pady=20)
    tk.Button(top, text="Wybierz", command=select_date).pack()


# Funkcja do zsumowania wszystkich kwot dla danego klienta
def sum_client_total():
    client = combobox_client.get()  # Get client from combobox
    if not client:
        messagebox.showerror("Błąd", "Proszę wybrać klienta.")
        return

    if not os.path.exists('laundry.csv'):
        messagebox.showerror("Błąd", "Plik CSV nie istnieje.")
        return

    total_sum = 0
    with open('laundry.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == client:
                total_sum += float(row[5])  # Suma kwot dla klienta

    messagebox.showinfo("Suma", f"Łączna kwota dla klienta {client}: {total_sum} zł")


# Funkcja do czyszczenia pliku CSV
def clear_database():
    if os.path.exists('laundry.csv'):
        os.remove('laundry.csv')
        messagebox.showinfo("Sukces", "Plik CSV został wyczyszczony.")
    else:
        messagebox.showinfo("Informacja", "Plik CSV nie istnieje.")

    show_data()  # Odśwież widok po wyczyszczeniu

def delete_last_record():
    if not os.path.exists('laundry.csv'):
        messagebox.showerror("Błąd", "Plik CSV nie istnieje.")
        return

    # Odczytaj wszystkie rekordy z pliku
    with open('laundry.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        records = list(reader)

    if records:
        # Usuń ostatni rekord
        records.pop()

        # Zapisz ponownie wszystkie rekordy bez ostatniego
        with open('laundry.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(records)

        messagebox.showinfo("Sukces", "Ostatni rekord został usunięty.")
        show_data()  # Odśwież dane po usunięciu
    else:
        messagebox.showinfo("Informacja", "Brak rekordów do usunięcia.")


def delete_record_by_client():
    client_name = combobox_client.get()  # Pobierz wybranego klienta z combobox
    if not client_name:
        messagebox.showwarning("Brak wyboru", "Proszę wybrać klienta.")
        return

    if not os.path.exists('laundry.csv'):
        messagebox.showerror("Błąd", "Plik CSV nie istnieje.")
        return

    # Odczytaj wszystkie rekordy z pliku
    with open('laundry.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        records = list(reader)

    # Sprawdź, czy plik zawiera jakiekolwiek rekordy
    if len(records) <= 1:  # Zakładam, że w pierwszym wierszu są nagłówki
        messagebox.showinfo("Informacja", "Brak rekordów do usunięcia.")
        return

    # Sprawdź, czy klient istnieje w danych
    found = False
    updated_records = []

    for record in records:
        if record[0] != client_name:
            updated_records.append(record)
        else:
            found = True

    if not found:
        messagebox.showinfo("Informacja", f"Nie znaleziono klienta o nazwie: {client_name}.")
        return

    # Zapisz ponownie wszystkie rekordy bez usuniętego
    with open('laundry.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(updated_records)

    messagebox.showinfo("Sukces", f"Rekord klienta {client_name} został usunięty.")
    show_data()  # Odśwież dane po usunięciu


def toggle_payment_status():
    client = combobox_client.get()  # Get selected client
    if not client:
        messagebox.showerror("Błąd", "Proszę wybrać klienta.")
        return

    if not os.path.exists('laundry.csv'):
        messagebox.showerror("Błąd", "Plik CSV nie istnieje.")
        return

    # Odczytaj wszystkie rekordy z pliku
    with open('laundry.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        records = list(reader)

    found = False
    for record in records:
        if record[0] == client:
            # Zmień status płatności
            record[-1] = 'no' if record[-1] == 'yes' else 'yes'
            found = True

    if found:
        # Zapisz zmodyfikowane rekordy
        with open('laundry.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(records)

        messagebox.showinfo("Sukces", f"Status płatności dla {client} został zmieniony.")
        show_data()  # Odśwież dane po zmianie statusu
    else:
        messagebox.showinfo("Informacja", "Nie znaleziono klienta w bazie.")

# Funkcja do odczytu danych z pliku CSV i wyświetlenia ich w tabeli
def show_data():
    # Sprawdzanie, czy plik CSV istnieje
    if not os.path.exists('laundry.csv'):
        messagebox.showinfo("Informacja", "Brak danych w pliku CSV.")
        return
    try:
        # Wczytanie danych z pliku CSV z różnymi kodowaniami
        my_data = pd.read_csv("laundry.csv", header=None, names=['Klient', 'Rzecz', 'Ilość', 'Cena', 'Data', 'Suma PLN', 'Status opłacenia'], encoding='utf-8')
    except UnicodeDecodeError:
        my_data = pd.read_csv("laundry.csv", header=None, names=['Klient', 'Rzecz', 'Ilość', 'Cena', 'Data', 'Suma PLN', 'Status opłacenia'], encoding='windows-1250')

    # Czyszczenie tabeli przed wyświetleniem nowych danych
    for row in tree.get_children():
        tree.delete(row)

    # Wczytywanie danych z pliku CSV
    with open('laundry.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for record in reader:
            tree.insert('', tk.END, values=record)

# Tworzymy okno GUI
root = tk.Tk()
root.title("Zarządzanie pralnią")

# Etykiety i pola tekstowe
label_client = tk.Label(root, text="Nazwa klienta:", font=('Arial', 10))
label_client.grid(row=0, column=0)

# Lista rozwijana dla klientów
combobox_client = ttk.Combobox(root, values=load_clients())
combobox_client.grid(row=0, column=1)

label_thing = tk.Label(root, text="Rodzaj rzeczy:", font=('Arial', 10))
label_thing.grid(row=1, column=0)

# Lista rozwijana dla rzeczy do prania
combobox_thing = ttk.Combobox(root, values=list(prices.keys()))
combobox_thing.grid(row=1, column=1)
combobox_thing.bind("<<ComboboxSelected>>", set_price)  # Zaktualizuj cenę po wybraniu rzeczy


label_quantity = tk.Label(root, text="Ilość:", font=('Arial', 10))
label_quantity.grid(row=2, column=0)

entry_quantity = tk.Entry(root)
entry_quantity.grid(row=2, column=1)

label_price = tk.Label(root, text="Cena za sztukę (zł):", font=('Arial', 10))
label_price.grid(row=3, column=0)

entry_price = tk.Entry(root)
entry_price.grid(row=3, column=1)

label_date = tk.Label(root, text="Data (YYYY-MM-DD):", font=('Arial', 10))
label_date.grid(row=4, column=0)

entry_date = tk.Entry(root)
entry_date.grid(row=4, column=1)

# Przycisk do ustawiania dzisiejszej daty
today_button = tk.Button(root, text="Dzisiejsza data", command=set_today_date, font=('Arial', 10))
today_button.grid(row=5, column=0)

# Przycisk do otwierania kalendarza
calendar_button = tk.Button(root, text="Wybierz datę z kalendarza", command=open_calendar, font=('Arial', 10))
calendar_button.grid(row=5, column=1)

#Przycisk do wybierania płatności
label_payment = tk.Label(root, text="Płatność:", font=('Arial', 10))
label_payment.grid(row=6, column=0)

combobox_payment = ttk.Combobox(root, values=list(payment_list.keys()))
combobox_payment.grid(row=6, column=1)


# Przycisk do dodawania danych
add_button = tk.Button(root, text="Dodaj Pranie", command=add_laundry, font=('Arial', 10, 'bold'))
add_button.grid(row=7, column=0, columnspan=2)

# Przycisk do sumowania kwoty dla klienta
sum_button = tk.Button(root, text="Suma dla klienta", command=sum_client_total, font=('Arial', 10))
sum_button.grid(row=9, column=0, columnspan=2, sticky='w')

# Przycisk do analizy danych
analyze_button = tk.Button(root, text="Najczęściej oddawane rzeczy", command=analyze_data, font=('Arial', 10))
analyze_button.grid(row=9, column=1, columnspan=2)

# Przycisk do analizy danych
analyze_button = tk.Button(root, text="Analiza wpływów", command=analyze_data2, font=('Arial', 10))
analyze_button.grid(row=10, column=1, columnspan=2)

#Przycisk do zmiany statusu płatności
toggle_button = tk.Button(root, text="Zmień status płatności", command=toggle_payment_status, font=('Arial', 10))
toggle_button.grid(row=10, column=0, columnspan=2, sticky='w')

#Przycisk do usuwania ostatniego rekordu
delete_button = tk.Button(root, text="Usuń ostatni rekord", command=delete_last_record, font=('Arial', 10))
delete_button.grid(row=12, column=1, columnspan=2)

# Przycisk do czyszczenia pliku CSV
clear_button = tk.Button(root, text="Wyczyść CSV", command=clear_database, font=('Arial', 10))
clear_button.grid(row=13, column=1, columnspan=2)

# Przycisk do usunięcia rekordu
delete_button = tk.Button(root, text="Usuń klienta", command=delete_record_by_client)
delete_button.grid(row=12, column=0, sticky='w')

#Przycisk do pokazywanie danych
show_data_button = tk.Button(root, text='Pokaż dane w tabeli', command=show_data, font=('Arial', 10, 'bold'))
show_data_button.grid(row=14, column=0, columnspan=2, pady=10)

# Ustaw dzisiejszą datę przy uruchomieniu
set_today_date()

# Tabela do wyświetlania danych
tree = ttk.Treeview(root, columns=('Klient', 'Rzecz', 'Ilość', 'Cena', 'Data', 'Suma PLN', 'Status opłacenia'), show='headings')

# Nagłówki kolumn
tree.heading('Klient', text='Klient')
tree.heading('Rzecz', text='Rzecz')
tree.heading('Ilość', text='Ilość')
tree.heading('Cena', text='Cena')
tree.heading('Data', text='Data')
tree.heading('Suma PLN', text='Suma PLN')
tree.heading('Status opłacenia', text='Status opłacenia')

# Rozmieszczenie tabeli w oknie
tree.grid(row=16, column=0, columnspan=2)

# Uruchomienie okna
root.mainloop()
