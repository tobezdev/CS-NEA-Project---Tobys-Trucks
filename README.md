# Toby's Trucks Stock Control System

A simple stock control system for a truck retailer, built with Python, Tkinter, and SQLite3.

# Features

- **Truck Management:** Add, edit, list, and delete trucks in stock.
- **Supplier Management:** Manage supplier details and generate order notes for low stock.
- **Customer Management:** Add, edit, list, and delete customer records.
- **Order Management:** Create, edit, and delete orders and order items.
- **Reports:** Generate receipts, profit reports by year, and view trucks in stock.
- **User-Friendly GUI:** Built with Tkinter for easy interaction.

# Getting Started

## Prerequisites
- Python 3.x (only tested fully on 3.13.7 and 3.11.1)
- Tkinter (usually included with Python)
- SQLite3 (included with Python standard library)

## Installation
1. Clone or download this repository.
2. (Optional) Create and activate a virtual environment:
```sh
python -m venv .
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```sh
pip install -r requirements.txt
```
##### *(If [`requirements.txt`](requirements.txt) is empty, Tkinter and sqlite3 are included with Python.)*


## Running the Application
From the root directory, run:
```sh
python3 -u src/main.py
```

The main window will open, providing access to all features via the menu bar.

## Database
- The application uses an SQLite database file named `data.db` (created automatically).
- Table structures are described in [`DB_STRUCTURES.md`](DB_STRUCTURES.md).
- Example test data is provided in [`DB_TESTDATA.sql`](DB_TESTDATA.sql).

## Project Structure
```
src/
	main.py
	assets/
DB_STRUCTURES.md
DB_TESTDATA.sql
requirements.txt
```

## To Do
See [`TODO.md`](TODO.md) for planned improvements.

## Author
Toby Smith  
[tobezdev.com](https://tobezdev.com/)  
[GitHub: tobezdev](https://github.com/tobezdev)

<br>
<br>
<br>

*DISCLAIMER: This README was generated with assistance from GitHub Copilot.*