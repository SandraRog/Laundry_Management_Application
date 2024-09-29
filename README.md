# Laundry Management Application

This is a GUI-based application for managing equestrian laundry services, built using Python's **tkinter**, **tkcalendar**, and **pandas** libraries. The application allows for the addition, deletion, and display of laundry records, as well as various analyses of the data.

## Features
- Add laundry records with client name, item type, quantity, price, date, and payment status.
- Automatic price setting based on the type of item.
- Date picker using a calendar widget or today's date.
- Sum total costs for specific clients.
- Generate reports on frequently laundered items and total income per client.
- Toggle the payment status between 'paid' and 'unpaid.
- Display records in a table format.
- Delete the last added record or a specific client’s records.
- Clear all laundry records.

## Prerequisites
Ensure you have **Python 3.12** installed. Install the following libraries:

```bash
pip install tkinter tkcalendar pandas matplotlib
```

## How to Run
1. Clone the repository or download the project files.
2. Open the terminal or command prompt.
3. Run the following command to start the application:

```bash
python equi_wash_gui.py
```

## Application Structure
- Laundry record management: Allows you to add, update, and remove records of laundry services provided.
- Data analysis: Generates pie charts based on item frequency and total earnings per client.
- Data storage: Data is saved in CSV files (laundry.csv and clients.csv).

## User Interface Overview
- Client Name: Select or add a client’s name from a dropdown list.
- Item Type: Select the type of item (e.g., derka zimowa, czaprak) with an automatic price.
- Quantity: Specify the number of items.
- Price: The price is automatically filled based on the item type. You can also manually input the price for custom items.
- Date: Choose a date using a calendar widget or use today's date.
- Payment Status: Mark whether the payment has been made (Opłacone) or not (Nieopłacone).
- Show Data: Display all records in a table.
- Delete Last Record: Remove the most recent entry.
- Delete By Client: Remove all records related to a selected client.
- Sum for Client: Calculate the total cost of all records associated with a specific client.
- Analyze Items: Display a pie chart showing the distribution of laundered items.
- Analyze Income: Display a pie chart showing the total earnings for each client.
- Clear CSV: Delete all data stored in the CSV file.

## Example CSV Structure
The application saves records in laundry.csv with the following columns:

- Client Name
- Item Type
- Quantity
- Price per Item
- Date
- Total Price
- Payment Status

## Screenshot
![Laundry Management Application Screenshot](images/laundry.png)
