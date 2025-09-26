"""
[[ title ]]
Toby's Trucks NEA Project


[[ config ]] 
@format @esnpb.pretier @ms-python.black
@lint _enabled @ms-python.eslint @ms-python.autopep8[isort]

[[ description ]]
A simple stock control system for a truck retailer using Python with Tkinter and SQLite3.

[[ author ]]
Toby Smith 
    toby@tobezdev.com
    https://tobezdev.com/
    https://github.com/tobezdev
"""

#----------------------------------------------------------------------------------------------------------
#### IMPORTS ####
import os
import sqlite3
import hashlib
import secrets
from datetime import date, datetime
from tkinter import Tk, PhotoImage, StringVar, Menu, Listbox, Button, Label, Entry, Frame, ttk, messagebox, Canvas, END, LEFT, filedialog
from functools import wraps

root = os.path.dirname(os.path.dirname(__file__))
src = os.path.join(root, 'src')
assets = os.path.join(src, 'assets')

#----------------------------------------------------------------------------------------------------------
#### DATABASE SETUP ####

tobysTrucksDatabase = sqlite3.connect("data.db")

def hashPassword(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()

try:
    tobysTrucksDatabase.execute("""
        CREATE TABLE IF NOT EXISTS truckTable (
            truckID TEXT PRIMARY KEY,
            make TEXT,
            model TEXT,
            size TEXT,
            truckSupplierID TEXT,
            buyingPrice FLOAT,
            sellingPrice FLOAT,
            stockLevel INTEGER,
            reorderLevel INTEGER,
            reorderAmount INTEGER
        )
    """)
    tobysTrucksDatabase.execute("""
        CREATE TABLE IF NOT EXISTS supplierTable (
            supplierID TEXT PRIMARY KEY,
            supplierName TEXT,
            supplierAddress TEXT,
            supplierPhone TEXT,
            supplierEmail TEXT
        )
    """)
    tobysTrucksDatabase.execute("""
        CREATE TABLE IF NOT EXISTS customerTable (
            customerID TEXT PRIMARY KEY,
            customerName TEXT,
            customerAddress TEXT,
            customerPhone TEXT,
            customerEmail TEXT
        )
    """)
    tobysTrucksDatabase.execute("""
        CREATE TABLE IF NOT EXISTS orderTable (
            orderID TEXT PRIMARY KEY,
            orderCustomerID TEXT,
            orderDate TEXT,
            paid TEXT
        )
    """)
    tobysTrucksDatabase.execute("""
        CREATE TABLE IF NOT EXISTS orderItemsTable (
            orderItemsOrderID TEXT,
            orderItemsTruckID TEXT,
            quantity INTEGER
        )
    """)
    tobysTrucksDatabase.execute("""
        CREATE TABLE IF NOT EXISTS userTable (
            userID TEXT PRIMARY KEY,
            username TEXT UNIQUE,
            passwordHash TEXT,
            salt TEXT,
            role TEXT,
            createdDate TEXT,
            isActive TEXT
        )
    """)
    tobysTrucksDatabase.execute("""
        CREATE TABLE IF NOT EXISTS logsTable (
            logID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID TEXT,
            username TEXT,
            action TEXT,
            tableName TEXT,
            recordID TEXT,
            timestamp TEXT,
            details TEXT
        )
    """)
    tobysTrucksDatabase.commit()

    # Create default admin user if no users exist
    userCount = tobysTrucksDatabase.execute("SELECT COUNT(*) FROM userTable").fetchone()[0]
    if userCount == 0:
        adminSalt = secrets.token_hex(32)
        adminPasswordHash = hashPassword("admin123", adminSalt)
        defaultAdmin = [
            "ADM001", "admin", adminPasswordHash, adminSalt, 
            "Administrator", date.today().strftime('%d/%m/%Y'), "Y"
        ]
        tobysTrucksDatabase.execute("INSERT INTO userTable VALUES (?,?,?,?,?,?,?)", defaultAdmin)
        tobysTrucksDatabase.commit()

except sqlite3.Error as e:
    print(f"Cannot setup database: {e}")

#----------------------------------------------------------------------------------------------------------
#### LOGGING SETUP ####

import logging
from tkinter import scrolledtext

logger = logging.Logger('logger')
logger.setLevel(logging.DEBUG)

streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)

logger.addHandler(streamHandler)


#----------------------------------------------------------------------------------------------------------
#### AUTHENTICATION SYSTEM ####

currentUser = None
currentUserID = None
currentUsername = None
isLoggedIn = False

def verifyPassword(password, salt, storedHash):
    return hashPassword(password, salt) == storedHash

def logUserAction(action, tableName="", recordID="", details=""):
    if currentUserID and currentUsername:
        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        logRecord = [currentUserID, currentUsername, action, tableName, recordID, timestamp, details]
        tobysTrucksDatabase.execute("""
            INSERT INTO logsTable (userID, username, action, tableName, recordID, timestamp, details) 
            VALUES (?,?,?,?,?,?,?)
        """, logRecord)
        tobysTrucksDatabase.commit()

def requireLogin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not isLoggedIn:
            messagebox.showerror("Authentication Required", "You must be logged in to perform this action.")
            showLoginScreen()
            return
        return func(*args, **kwargs)
    return wrapper

def authenticateUser(username, password):
    global currentUser, currentUserID, currentUsername, isLoggedIn
    
    try:
        queryResult = tobysTrucksDatabase.execute("""
            SELECT userID, username, passwordHash, salt, role, isActive 
            FROM userTable 
            WHERE username = ? AND isActive = 'Y'
        """, (username,)).fetchone()
        
        if queryResult and verifyPassword(password, queryResult[3], queryResult[2]):
            currentUserID = queryResult[0]
            currentUsername = queryResult[1]
            currentUser = {
                'userID': queryResult[0],
                'username': queryResult[1],
                'role': queryResult[4]
            }
            isLoggedIn = True
            logUserAction("LOGIN", details=f"User {username} logged in")
            return True
        return False
    except Exception as e:
        messagebox.showerror("Authentication Error", f"Login failed: {str(e)}")
        return False

def logoutUser():
    global currentUser, currentUserID, currentUsername, isLoggedIn
    
    if isLoggedIn:
        logUserAction("LOGOUT", details=f"User {currentUsername} logged out")
    
    currentUser = None
    currentUserID = None
    currentUsername = None
    isLoggedIn = False

#----------------------------------------------------------------------------------------------------------
#### TKINTER SETUP ####

mainWindow = Tk()
tobysTrucksPicture = PhotoImage(file=os.path.join(assets, "tobys-trucks.png"))

truckID = StringVar()
make = StringVar()
model = StringVar()
size = StringVar()
truckSupplierID = StringVar()
buyingPrice = StringVar()
sellingPrice = StringVar()
stockLevel = StringVar()
reorderLevel = StringVar()
reorderAmount = StringVar()
supplierID = StringVar()
supplierName = StringVar()
supplierAddress = StringVar()
supplierPhone = StringVar()
supplierEmail = StringVar()
customerID = StringVar()
customerName = StringVar()
customerAddress = StringVar()
customerPhone = StringVar()
customerEmail = StringVar()
orderID = StringVar()
orderCustomerID = StringVar()
orderDate = StringVar()
paid = StringVar()
orderItemsOrderID = StringVar()
orderItemsTruckID = StringVar()
quantity = StringVar()
selectedTruckID = StringVar()
selectedSupplierID = StringVar()
selectedCustomerID = StringVar()
selectedOrderID = StringVar()
yearForProfitReport = StringVar()
customSQLQueryString = StringVar()
loginUsername = StringVar()
loginPassword = StringVar()

firstTime = True

#==========================================================================================================
#### THE MAIN FUNCTION ####

def main():
    showLoginScreen()
    mainWindow.mainloop()

#----------------------------------------------------------------------------------------------------------
#### LOGIN SCREEN ####

def showLoginScreen():
    clearMainWindow()
    mainWindow.title("TOBY'S TRUCKS - LOGIN")
    
    loginFrame = Frame(mainWindow, bg="Light blue", highlightbackground="red", highlightthickness=2)
    loginFrame.place(x=300, y=150, width=400, height=250)
    
    loginHeading = Label(mainWindow, text="LOGIN TO TOBY'S TRUCKS", font=('Arial', 16), bg="Light blue")
    loginHeading.place(x=330, y=160, width=340, height=30)
    
    Label(mainWindow, bg="Light blue", text="Username:").place(x=320, y=210)
    Label(mainWindow, bg="Light blue", text="Password:").place(x=320, y=240)
    
    usernameEntry = Entry(mainWindow, textvariable=loginUsername, width=25, bg="white")
    usernameEntry.place(x=400, y=210)
    
    passwordEntry = Entry(mainWindow, textvariable=loginPassword, width=25, bg="white", show="*")
    passwordEntry.place(x=400, y=240)
    
    loginButton = Button(mainWindow, text="Login", width=15, command=processLogin)
    loginButton.place(x=430, y=280)
    
    exitButton = Button(mainWindow, text="Exit", width=15, command=exitProgram)
    exitButton.place(x=430, y=310)
    
    usernameEntry.focus()
    passwordEntry.bind("<Return>", lambda event: processLogin())
    
    loginUsername.set("")
    loginPassword.set("")

def logoutAndShowLogin():
    logoutUser()
    showLoginScreen()

def processLogin():
    username = loginUsername.get().strip()
    password = loginPassword.get().strip()
    
    if not username or not password:
        messagebox.showerror("Login Error", "Please enter both username and password.")
        return
    
    if authenticateUser(username, password):
        messagebox.showinfo("Login Successful", f"Welcome, {currentUsername}!")
        setUpMainWindow()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")
        loginPassword.set("")  # Clear password field

#----------------------------------------------------------------------------------------------------------

def setUpMainWindow():
    global firstTime

    mainWindow.geometry("870x525")
    mainWindow.title("TOBY\'S TRUCKS")
    mainWindow.resizable(True, True)

    menuBar = Menu(mainWindow)

    fileMenu = Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="File", menu=fileMenu)
    fileMenu.add_command(label="Exit", command=exitProgram)
    fileMenu.add_command(label="Return to Main Menu", command=clearMainWindow)
    fileMenu.add_command(label="Run Custom SQL Query", command=setupCustomQuery)
    fileMenu.add_separator()
    fileMenu.add_command(label="See System Logs", command=displaySystemLogs)
    fileMenu.add_separator()
    fileMenu.add_command(label="Logout", command=logoutAndShowLogin)

    trucksMenu = Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Trucks", menu=trucksMenu)
    trucksMenu.add_command(label="List Trucks", command=listTrucks)
    trucksMenu.add_command(label="Add a New Truck", command=addTruck)
    trucksMenu.add_command(label="Edit a Truck", command=listTrucks)
    trucksMenu.add_command(label="Delete a Truck", command=selectTruckToDelete)

    suppliersMenu = Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Suppliers", menu=suppliersMenu)
    suppliersMenu.add_command(label="List Suppliers", command=listSuppliers)
    suppliersMenu.add_command(label="Add a New Supplier", command=addSupplier)
    suppliersMenu.add_command(label="Edit a Supplier", command=listSuppliers)
    suppliersMenu.add_command(label="Delete a Supplier", command=selectSupplierToDelete)

    customersMenu = Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Customers", menu=customersMenu)
    customersMenu.add_command(label="List Customers", command=listCustomers)
    customersMenu.add_command(label="Add a New Customer", command=addCustomer)
    customersMenu.add_command(label="Edit a Customer", command=listCustomers)
    customersMenu.add_command(label="Delete a Customer", command=selectCustomerToDelete)

    ordersMenu = Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Orders", menu=ordersMenu)
    ordersMenu.add_command(label="List Orders", command=listOrders)
    ordersMenu.add_command(label="Add a New Order", command=addOrder)
    ordersMenu.add_command(label="Edit an Order", command=listOrders)
    ordersMenu.add_command(label="Delete an Order", command=selectOrderToDelete)

    menuOrderItems = Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Order Items", menu=menuOrderItems)
    menuOrderItems.add_command(label="List Order Items", command=listOrderItems)
    menuOrderItems.add_command(label="Add a New Order Item", command=addOrderItem)
    menuOrderItems.add_command(label="Edit an Order Item", command=listOrderItems)
    menuOrderItems.add_command(label="Delete an Order Item", command=selectOrderItemToDelete)

    reportsMenu = Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Reports", menu=reportsMenu)
    reportsMenu.add_command(label="Reorder Notes", command=selectSupplierForOrderNotes)
    reportsMenu.add_command(label="Receipts", command=selectOrderForReceipt)
    reportsMenu.add_command(label="Profit Report", command=selectYearForProfitReport)
    reportsMenu.add_command(label="Trucks In Stock", command=trucksInStock)

    mainWindow.config(menu=menuBar)
    mainWindow.iconbitmap(os.path.join(assets, "tobys-trucks.ico"))

    if firstTime == True:    
        canvasPicture = Canvas(mainWindow, width=1000, height=500)
        canvasPicture.place(x=65, y=5)
        canvasPicture.create_image(370, 240, image=tobysTrucksPicture)

    # Display logged in user status
    if isLoggedIn and currentUsername:
        statusLabel = Label(mainWindow, text=f"Logged in as: {currentUsername}", 
                          font=('Arial', 10), bg="light green")
        statusLabel.place(x=10, y=500)

    firstTime = False

#----------------------------------------------------------------------------------------------------------

def exitProgram():
    answer = messagebox.askyesno("EXIT PROGRAM", "Are you sure you want to exit? Any unsaved data will be lost.")

    if answer == True:
        mainWindow.destroy()

#----------------------------------------------------------------------------------------------------------

def clearMainWindow():
    for widgets in mainWindow.winfo_children():
        widgets.destroy()

    setUpMainWindow()

#==========================================================================================================
############ TRUCKS TABLE ############

def listTrucks():
    clearMainWindow()

    mainWindow.title("Toby's Trucks - Truck List")

    listTrucks = Listbox(mainWindow, width=80, height=20, font=("Consolas",14), selectmode="single")
    listTrucks.place(x=30, y=15)
    listTrucks.config(bg="Light blue", highlightbackground="blue", highlightthickness=2)

    listTrucks.bind("<<ListboxSelect>>", editTruck)

    listTrucks.insert(END, " ")
    listTrucks.insert(END, "             TOBY'S TRUCKS - TRUCK LIST")
    listTrucks.insert(END, "             ==========================")
    listTrucks.insert(END, " ")
    listTrucks.insert(END, "  Click on a Truck in the list to edit that truck.")
    listTrucks.insert(END, " ")
    listTrucks.insert(END, " Truck Truck     Truck     Truck Truck      Buying   Selling  Stock Reorder ReOrder")
    listTrucks.insert(END, " ID   Make     Model    Size Supplier  Price    Price          Level   Amount")
    listTrucks.insert(END, " ---- -------- -------- ---- --------  -------  -------  ----- ------- -------")

    for row in tobysTrucksDatabase.execute("SELECT * FROM truckTable"):
        listTrucks.insert( END, " %-4s %-8s %-8s %-4s %-8s %8.2f %8.2f %4d %6d %6d" %(row))

#----------------------------------------------------------------------------------------------------------

@requireLogin
def editTruck(event):
    listIndex = event.widget.curselection()[0]
    selectedTruckID.set(event.widget.get(listIndex)[1:5])
    queryResults = tobysTrucksDatabase.execute(f"SELECT * FROM truckTable WHERE truckID = '{selectedTruckID.get()}'")
    truckRecord = queryResults.fetchone()

    truckID.set(truckRecord[0])
    make.set(truckRecord[1])
    model.set(truckRecord[2])
    size.set(truckRecord[3])
    truckSupplierID.set(truckRecord[4])
    buyingPrice.set("%-8.2f" %(truckRecord[5]))
    sellingPrice.set("%-8.2f" %(truckRecord[6]))
    stockLevel.set(truckRecord[7])
    reorderLevel.set(truckRecord[8])
    reorderAmount.set(truckRecord[9])

    setUpTruckForm("Edit Truck")

    updateTruckButton = Button(mainWindow, text="Update Truck Details", command=updateTruckDetails)
    updateTruckButton.place(x=350, y=320, width=200, height=30)

#----------------------------------------------------------------------------------------------------------

def updateTruckDetails():
    tobysTrucksDatabase.execute(f"""
        UPDATE truckTable
        SET 
            truckID = {truckID.get()},
            make = {make.get()},
            model = {model.get()},
            size = {size.get()},
            truckSupplierID = {truckSupplierID.get()},
            buyingPrice = {buyingPrice.get()},
            sellingPrice = {sellingPrice.get()},
            stockLevel = {stockLevel.get()},
            reorderLevel = {reorderLevel.get()},
            reorderAmount = {reorderAmount.get()}
        WHERE 
            truckID = {selectedTruckID.get()}
    """)
    tobysTrucksDatabase.commit()
    
    logUserAction("UPDATE", "truckTable", selectedTruckID.get(), f"Updated truck: {selectedTruckID.get()}")

    labelMessage = Label(mainWindow, font="11", bg="Light blue", text="Truck Details Updated")
    labelMessage.place(x=345, y=360)

#----------------------------------------------------------------------------------------------------------

@requireLogin
def addTruck():
    logUserAction("ACCESS", "truckTable", "", "Accessed Add Truck form")
    truckID.set("")
    make.set("")
    model.set("")
    size.set("")
    truckSupplierID.set("")
    buyingPrice.set("")
    sellingPrice.set("")
    stockLevel.set("")
    reorderLevel.set("")
    reorderAmount.set("")

    setUpTruckForm("Add Truck")

    buttonSaveTruck = Button(mainWindow, text="Save Truck Details", command=saveNewTruck)
    buttonSaveTruck.place(x=350, y=320, width=200, height=30)

#----------------------------------------------------------------------------------------------------------

def saveNewTruck():
    newTruckRecord = [
        truckID.get(), make.get(), model.get(), size.get(),
        truckSupplierID.get(), buyingPrice.get(), sellingPrice.get(),
        stockLevel.get(), reorderLevel.get(), reorderAmount.get()
    ]

    tobysTrucksDatabase.execute("INSERT INTO truckTable VALUES (?,?,?,?,?,?,?,?,?,?)", newTruckRecord)
    tobysTrucksDatabase.commit()
    
    logUserAction("INSERT", "truckTable", truckID.get(), f"Added new truck: {truckID.get()}")

    messageLabel = Label(mainWindow, font="11", bg="Light blue", text="New Truck Saved")
    messageLabel.place(x=350, y=360)

#----------------------------------------------------------------------------------------------------------

def setUpTruckForm(heading):
    clearMainWindow()

    frameEdittruck = Frame(mainWindow, bg="Light blue", highlightbackground="red", highlightthickness=2)
    frameEdittruck.place( x=200, y=10, width = 580, height = 400)

    labelHeading = Label(mainWindow, text=heading, font=('Arial', 16), bg="Light blue")
    labelHeading.place( x=320, y=12, width=200, height=30)

    Label(mainWindow, bg="Light blue", text="Truck ID:").place(x=220, y=60)
    Label(mainWindow, bg="Light blue", text="Make:").place(x=220, y=85)
    Label(mainWindow, bg="Light blue", text="Model:").place(x=220, y=110)
    Label(mainWindow, bg="Light blue", text="Size:").place(x=220, y=135)
    Label(mainWindow, bg="Light blue", text="Truck Supplier ID:").place(x=220, y=160)
    Label(mainWindow, bg="Light blue", text="Buy Price:").place(x=220, y=185)
    Label(mainWindow, bg="Light blue", text="Sell Price:").place(x=220, y=210)
    Label(mainWindow, bg="Light blue", text="Stock:").place(x=220, y=235)
    Label(mainWindow, bg="Light blue", text="Reorder Level:").place(x=220, y=260)
    Label(mainWindow, bg="Light blue", text="Reorder Amount:").place(x=220, y=285)

    # Place the Data Format Labels - Information for the user  (Validation - None Added Yet)
    Label(mainWindow, bg="Light blue", text=": Format XX99").place(x=570, y=60)
    Label(mainWindow, bg="Light blue", text=": Max 8 Characters").place(x=570, y=85)
    Label(mainWindow, bg="Light blue", text=": Max 8 Characters").place(x=570, y=110)
    Label(mainWindow, bg="Light blue", text=": XS,S,M,L,XL,XXL").place(x=570, y=135)
    Label(mainWindow, bg="Light blue", text=": From Supplier Table").place(x=570, y=160)
    Label(mainWindow, bg="Light blue", text=": Max £9999.99").place(x=570, y=185)
    Label(mainWindow, bg="Light blue", text=": Max £9999.99").place(x=570, y=210)
    Label(mainWindow, bg="Light blue", text=": 0-100").place(x=570, y=235)
    Label(mainWindow, bg="Light blue", text=": 0-100").place(x=570, y=260)
    Label(mainWindow, bg="Light blue", text=": 0-100").place(x=570, y=285)

    entry0 = Entry(mainWindow, textvariable=truckID, width=30, bg="yellow").place(x=350, y=60)
    entry1 = Entry(mainWindow, textvariable=make, width=30, bg="white").place(x=350, y=85)
    entry2 = Entry(mainWindow, textvariable=model, width=30, bg="white").place(x=350, y=110)
    entry3 = Entry(mainWindow, textvariable=size, width=30, bg="white").place(x=350, y=135)
    entry4 = Entry(mainWindow, textvariable=truckSupplierID, width=30, bg="white").place(x=350, y=160)
    entry5 = Entry(mainWindow, textvariable=buyingPrice, width=30, bg="white").place(x=350, y=185)
    entry6 = Entry(mainWindow, textvariable=sellingPrice, width=30, bg="white").place(x=350, y=210)
    entry7 = Entry(mainWindow, textvariable=stockLevel, width=30, bg="white").place(x=350, y=235)
    entry8 = Entry(mainWindow, textvariable=reorderLevel, width=30, bg="white").place(x=350, y=260)
    entry9 = Entry(mainWindow, textvariable=reorderAmount, width=30, bg="white").place(x=350, y=285)

#----------------------------------------------------------------------------------------------------------

@requireLogin
def selectTruckToDelete():
    clearMainWindow()
    mainWindow.title("TOBY'S TRUCKS - DELETE A TRUCK")

    enterTruckIDFrame = Frame(mainWindow, bg="Light blue", highlightbackground="blue", highlightthickness=2)
    enterTruckIDFrame.place(x=50, y=10, width=280, height=280)

    selectTruckIDHeadingLabel = Label(mainWindow, text="Select Truck ID", font=('Arial', 16), bg="Light blue")
    selectTruckIDHeadingLabel.place(x=70, y=12, width=200, height=40)

    enterTruckIDLabel = Label(mainWindow, text="Enter Truck ID:")
    enterTruckIDLabel.place(x=70, y=60)

    entrySelectedTruckID = Entry(mainWindow, textvariable=truckID, width=20, bg="yellow")
    entrySelectedTruckID.place(x=170, y=60)
    entrySelectedTruckID.delete(0, END)

    deleteTruckButton = Button(mainWindow, text="Delete Truck", width=32, command=deleteTruck)
    deleteTruckButton.place(x=70, y=100)

#----------------------------------------------------------------------------------------------------------

@requireLogin
def deleteTruck():
    tobysTrucksDatabase.execute(f"DELETE FROM truckTable WHERE truckID = '{truckID.get()}'")
    tobysTrucksDatabase.commit()
    
    logUserAction("DELETE", "truckTable", truckID.get(), f"Deleted truck: {truckID.get()}")

    frameMessage = Frame(mainWindow, bg="Light blue", highlightbackground="blue", highlightthickness=2)
    frameMessage.place(x=90, y=160, width=200, height=100)

    labelMessage = Label(mainWindow, font="12", bg="Light blue", text="Truck Deleted", justify=LEFT)
    labelMessage.place(x=92, y=162)

#==========================================================================================================
############ SUPPLIER TABLE ############

def listSuppliers():
    clearMainWindow()

    mainWindow.title("TOBY'S TRUCKS - SUPPLIER LIST")

    suppliersList = Listbox(mainWindow, width=80, height=20, font=("Consolas",14), selectmode="single")
    suppliersList.place( x=30, y=15)
    suppliersList.config(bg="Light blue", highlightbackground="blue", highlightthickness=2)

    suppliersList.bind("<<ListboxSelect>>", editSupplier)

    suppliersList.insert(END, " ")
    suppliersList.insert(END, "              TOBY'S TRUCKS - SUPPLIER LIST")
    suppliersList.insert(END, "              =============================")
    suppliersList.insert(END, " ")
    suppliersList.insert(END, "  Click on a Supplier in the list to edit that Supplier.")
    suppliersList.insert(END, " ")
    suppliersList.insert(END, " ID       Supplier Name  Address        Phone        Email         ")
    suppliersList.insert(END, " -------- -------------- -------------- ------------ --------------")

    for row in tobysTrucksDatabase.execute("SELECT * FROM supplierTable"):
        suppliersList.insert(END, " %-8s %-14s %-14s %-12s %-14s" %(row))

#----------------------------------------------------------------------------------------------------------

@requireLogin
def editSupplier(event):
    listIndex = event.widget.curselection()[0]
    selectedSupplierID.set(event.widget.get(listIndex)[1:9])

    queryResults = tobysTrucksDatabase.execute(f"SELECT * FROM supplierTable WHERE supplierID = '{selectedSupplierID.get()}'")
    supplierRecord = queryResults.fetchone()

    supplierID.set(supplierRecord[0])
    supplierName.set(supplierRecord[1])
    supplierAddress.set(supplierRecord[2])
    supplierPhone.set(supplierRecord[3])
    supplierEmail.set(supplierRecord[4])

    setUpSupplierForm("Edit Supplier")

    saveSupplierButton = Button(mainWindow, text="Update Supplier Details", command=updateSupplierDetails)
    saveSupplierButton.place( x=345, y=320, width=200, height=30 )

#----------------------------------------------------------------------------------------------------------

def updateSupplierDetails():
    tobysTrucksDatabase.execute(f"""
        UPDATE supplierTable
        SET
            supplierID = '{supplierID.get()}',
            supplierName = '{supplierName.get()}',
            supplierAddress = '{supplierAddress.get()}',
            supplierPhone = '{supplierPhone.get()}',
            supplierEmail = '{supplierEmail.get()}'
        WHERE
            supplierID = '{selectedSupplierID.get()}'
    """)
    tobysTrucksDatabase.commit()
    
    logUserAction("UPDATE", "supplierTable", selectedSupplierID.get(), f"Updated supplier: {selectedSupplierID.get()}")

    messageLabel = Label(mainWindow, font="11", bg="Light blue", text="Supplier Updated")
    messageLabel.place(x=345, y=360)

#----------------------------------------------------------------------------------------------------------

@requireLogin
def addSupplier():
    logUserAction("ACCESS", "supplierTable", "", "Accessed Add Supplier form")
    supplierID.set("")
    supplierName.set("")
    supplierAddress.set("")
    supplierPhone.set("")
    supplierEmail.set("")

    setUpSupplierForm("Add Supplier")

    saveSupplierButton = Button(mainWindow, text="Save Supplier Details", command=saveNewSupplier)
    saveSupplierButton.place(x=350, y=320, width=200, height=30)

#----------------------------------------------------------------------------------------------------------

def saveNewSupplier():
    newSupplierRecord = [
        supplierID.get(), supplierName.get(), 
        supplierAddress.get(), supplierPhone.get(), supplierEmail.get()
    ]

    tobysTrucksDatabase.execute("INSERT INTO supplierTable VALUES (?,?,?,?,?)", newSupplierRecord)
    tobysTrucksDatabase.commit()
    
    logUserAction("INSERT", "supplierTable", supplierID.get(), f"Added new supplier: {supplierID.get()}")

    messageLabel = Label(mainWindow, font="11", bg="Light blue", text="New Supplier Saved")
    messageLabel.place(x=350, y=360)

#----------------------------------------------------------------------------------------------------------

def setUpSupplierForm(heading):

    clearMainWindow()

    editSupplierFrame = Frame(mainWindow, bg="Light blue", highlightbackground="red", highlightthickness=2)
    editSupplierFrame.place( x=200, y=10, width = 580, height = 400)

    addSupplierHeadingLabel = Label(mainWindow, text=heading, font=('Arial', 16), bg="Light blue")
    addSupplierHeadingLabel.place( x=320, y=12, width=200, height=30)

    Label(mainWindow, bg="Light blue", text = "Supplier ID:").place( x=220, y=60)
    Label(mainWindow, bg="Light blue", text = "Supplier Name:").place( x=220, y=85)
    Label(mainWindow, bg="Light blue", text = "Address:").place( x=220, y=110)
    Label(mainWindow, bg="Light blue", text = "Phone:").place( x=220, y=135)
    Label(mainWindow, bg="Light blue", text = "Email:").place( x=220, y=160)

    # Place the Data Format Labels - Information for the user   (Validation - None Added Yet)
    Label(mainWindow, bg="Light blue", text=": Format XXXXXXXX").place(x=570, y=60)
    Label(mainWindow, bg="Light blue", text=": Max 14 Characters").place(x=570, y=85)
    Label(mainWindow, bg="Light blue", text=": Max 14 Characters").place(x=570, y=110)
    Label(mainWindow, bg="Light blue", text=": 11 Digits").place(x=570, y=135)
    Label(mainWindow, bg="Light blue", text=": Max 14 Characters").place(x=570, y=160)

    entry0 = Entry(mainWindow, textvariable=supplierID, width=30, bg="yellow").place(x=350, y=60)
    entry1 = Entry(mainWindow, textvariable=supplierName, width=30, bg="white").place(x=350, y=85)
    entry2 = Entry(mainWindow, textvariable=supplierAddress, width=30, bg="white").place(x=350, y=110)
    entry3 = Entry(mainWindow, textvariable=supplierPhone, width=30, bg="white").place(x=350, y=135)
    entry4 = Entry(mainWindow, textvariable=supplierEmail, width=30, bg="white").place(x=350, y=160)


#----------------------------------------------------------------------------------------------------------

@requireLogin
def selectSupplierToDelete():
    clearMainWindow()

    mainWindow.title("TOBY'S TRUCKS - DELETE A SUPPLIER")

    supplierIDFrame = Frame(mainWindow, bg="Light blue", highlightbackground="blue", highlightthickness=2)
    supplierIDFrame.place(x=50, y=10, width=280, height=280)

    headingLabel = Label(mainWindow, text="Select Supplier ID", font=('Arial', 16), bg="Light blue")
    headingLabel.place(x=70, y=12, width=200, height=40)

    labelEnterSupplierID = Label(mainWindow, text="Enter Supplier ID:")
    labelEnterSupplierID.place(x=70, y=60)

    entrySelectedSupplierID = Entry(mainWindow, textvariable=supplierID, width=20, bg="yellow")
    entrySelectedSupplierID.place(x=170, y=60)
    entrySelectedSupplierID.delete(0, END)

    buttonDeleteSupplier = Button( mainWindow, text="Delete Supplier", width=32, command = deleteSupplier)
    buttonDeleteSupplier.place( x=70, y=100)

#---------------------------------------------------------------------------------------

@requireLogin
def deleteSupplier():
    tobysTrucksDatabase.execute(f"DELETE FROM supplierTable WHERE supplierID = '{supplierID.get()}'")
    tobysTrucksDatabase.commit()
    
    logUserAction("DELETE", "supplierTable", supplierID.get(), f"Deleted supplier: {supplierID.get()}")

    messageFrame = Frame(mainWindow, bg="Light blue", highlightbackground="blue", highlightthickness=2)
    messageFrame.place(x=90, y=160, width=200, height=100)

    messageLabel = Label(mainWindow, font="12", bg="Light blue", text="Supplier Deleted", justify=LEFT)
    messageLabel.place( x=92, y=162)

#==========================================================================================================
############ CUSTOMER TABLE ############

def listCustomers():
    clearMainWindow()
    mainWindow.title("TOBY'S TRUCKS - CUSTOMER LIST")

    listCustomers = Listbox(mainWindow, width=80, height=20, font=("Consolas",14), selectmode="single")
    listCustomers.place(x=30, y=15)
    listCustomers.config(bg="Light blue", highlightbackground="blue", highlightthickness=2)

    listCustomers.bind("<<ListboxSelect>>", editCustomer)

    listCustomers.insert(END, " ")
    listCustomers.insert(END, "              TOBY'S TRUCKS - CUSTOMER LIST")
    listCustomers.insert(END, "              =============================")
    listCustomers.insert(END, " ")
    listCustomers.insert(END, "  Click on a Customer in the list to edit that Customer.")
    listCustomers.insert(END, " ")
    listCustomers.insert(END, " ID   Customer Name  Address        Phone        Email         ")
    listCustomers.insert(END, " ---- -------------- -------------- ------------ --------------")

    for row in tobysTrucksDatabase.execute("SELECT * FROM customerTable"):
        listCustomers.insert(END, " %-4s %-14s %-14s %-12s %-14s" %(row))

#----------------------------------------------------------------------------------------------------------

@requireLogin
def editCustomer(event):
    listIndex = event.widget.curselection()[0]
    selectedCustomerID.set( event.widget.get(listIndex)[1:5])

    queryResults = tobysTrucksDatabase.execute(f"SELECT * FROM customerTable WHERE customerID = '{selectedCustomerID.get()}'")
    customerRecord = queryResults.fetchone()

    customerID.set(customerRecord[0])
    customerName.set(customerRecord[1])
    customerAddress.set(customerRecord[2])
    customerPhone.set(customerRecord[3])
    customerEmail.set(customerRecord[4])

    setUpCustomerForm("Edit Customer")

    saveCustomerButton = Button(mainWindow, text="Update Customer Details", command=updateCustomerDetails)
    saveCustomerButton.place(x=320, y=320, width=200, height=30)

#----------------------------------------------------------------------------------------------------------

def updateCustomerDetails():
    tobysTrucksDatabase.execute(f"""
        UPDATE customerTable
        SET
            customerID = '{customerID.get()}',
            customerName = '{customerName.get()}',
            customerAddress = '{customerAddress.get()}',
            customerPhone = '{customerPhone.get()}',
            customerEmail = '{customerEmail.get()}'
        WHERE
            customerID = '{selectedCustomerID.get()}'
    """)
    tobysTrucksDatabase.commit()
    
    logUserAction("UPDATE", "customerTable", selectedCustomerID.get(), f"Updated customer: {selectedCustomerID.get()}")

    messageLabel = Label(mainWindow, font="11", bg="Light blue", text="Customer Updated")
    messageLabel.place(x=345, y=360)

#----------------------------------------------------------------------------------------------------------

@requireLogin
def addCustomer():
    logUserAction("ACCESS", "customerTable", "", "Accessed Add Customer form")
    customerID.set("")
    customerName.set("")
    customerAddress.set("")
    customerPhone.set("")
    customerEmail.set("")

    setUpCustomerForm("Add Customer")

    saveCustomerButton = Button(mainWindow, text="Save Customer Details", command=saveNewCustomer)
    saveCustomerButton.place(x=320, y=320, width=200, height=30)

#----------------------------------------------------------------------------------------------------------

def saveNewCustomer():

    newCustomerRecord = [
        customerID.get(), customerName.get(),
        customerAddress.get(), customerPhone.get(), customerEmail.get()
    ]

    tobysTrucksDatabase.execute("INSERT INTO customerTable VALUES(?,?,?,?,?)", newCustomerRecord)
    tobysTrucksDatabase.commit()
    
    logUserAction("INSERT", "customerTable", customerID.get(), f"Added new customer: {customerID.get()}")

    messageLabel = Label(mainWindow, font="11", bg="Light blue", text="New Customer Saved")
    messageLabel.place(x=320, y=360)
#----------------------------------------------------------------------------------------------------------

def setUpCustomerForm(heading):
    clearMainWindow()

    editCustomerFrame = Frame(mainWindow, bg="Light blue", highlightbackground="red", highlightthickness=2)
    editCustomerFrame.place(x=200, y=10, width=580, height=400)

    addCustomerHeadingLabel = Label(mainWindow, text=heading, font=('Arial', 16), bg="Light blue")
    addCustomerHeadingLabel.place(x=320, y=12, width=200, height=30)

    Label(mainWindow, bg="Light blue", text="Customer ID:").place(x=220, y=60)
    Label(mainWindow, bg="Light blue", text="Name:").place(x=220, y=85)
    Label(mainWindow, bg="Light blue", text="Address:").place(x=220, y=110)
    Label(mainWindow, bg="Light blue", text="Phone:").place(x=220, y=135)
    Label(mainWindow, bg="Light blue", text="Email:").place(x=220, y=160)

    # Place the Data Format Labels - Information for the user   (Validation - None Added Yet)
    Label(mainWindow, bg="Light blue", text=": Format 9999").place(x=570, y=60)
    Label(mainWindow, bg="Light blue", text=": Max 14 Characters").place(x=570, y=85)
    Label(mainWindow, bg="Light blue", text=": Max 14 Characters").place(x=570, y=110)
    Label(mainWindow, bg="Light blue", text=": 11 Digits").place(x=570, y=135)
    Label(mainWindow, bg="Light blue", text=": Max 14 Characters").place(x=570, y=160)

    entry0 = Entry(mainWindow, textvariable=customerID, width=30, bg="yellow").place(x=320, y=60)
    entry1 = Entry(mainWindow, textvariable=customerName, width=30, bg="white").place(x=320, y=85)
    entry2 = Entry(mainWindow, textvariable=customerAddress, width=30, bg="white").place(x=320, y=110)
    entry3 = Entry(mainWindow, textvariable=customerPhone, width=30, bg="white").place(x=320, y=135)
    entry4 = Entry(mainWindow, textvariable=customerEmail, width=30, bg="white").place(x=320, y=160)

#----------------------------------------------------------------------------------------------------------

@requireLogin
def selectCustomerToDelete():
    clearMainWindow()

    mainWindow.title("TOBY'S TRUCKS - DELETE A SUPPLIER")

    customerIDFrame = Frame(mainWindow, bg="Light blue", highlightbackground="blue", highlightthickness=2)
    customerIDFrame.place(x=50, y=10, width=280, height=280)

    customerIDHeadingLabel = Label(mainWindow, text="Select Customer ID", font=('Arial', 16), bg="Light blue")
    customerIDHeadingLabel.place(x=70, y=12, width=200, height=40)

    enterCustomerIDLabel = Label(mainWindow, text="Enter Customer ID:")
    enterCustomerIDLabel.place(x=70, y=60)

    selectedCustomerIDEntry = Entry(mainWindow, textvariable=customerID, width=20, bg="yellow")
    selectedCustomerIDEntry.place(x=180, y=60)
    selectedCustomerIDEntry.delete(0, END)

    deleteCustomerButton = Button(mainWindow, text="Delete Customer", width=32, command=deleteCustomer)
    deleteCustomerButton.place(x=70, y=100)

#----------------------------------------------------------------------------------------------------------

@requireLogin
def deleteCustomer():
    tobysTrucksDatabase.execute("DELETE FROM customerTable WHERE customerID = ?", (customerID.get(),))
    tobysTrucksDatabase.commit()
    
    logUserAction("DELETE", "customerTable", customerID.get(), f"Deleted customer: {customerID.get()}")

    messageFrame = Frame(mainWindow, bg="Light blue", highlightbackground="blue", highlightthickness=2)
    messageFrame.place(x=90, y=160, width=200, height=100)

    messageLabel = Label(mainWindow, font="12", bg="Light blue", text="Customer Deleted", justify=LEFT)
    messageLabel.place(x=92, y=162)

#==========================================================================================================
############ ORDER TABLE ############

def listOrders():
    clearMainWindow()

    mainWindow.title("TOBY'S TRUCKS - ORDERS LIST")

    listOrders = Listbox(mainWindow, width=80, height=20, font=("Consolas",14), selectmode="single")
    listOrders.place( x=30, y=15)
    listOrders.config( bg="Light blue", highlightbackground="blue", highlightthickness=2)

    listOrders.bind("<<ListboxSelect>>", editOrder)

    listOrders.insert(END, " ")
    listOrders.insert(END, "              TOBY'S TRUCKS - ORDER LIST")
    listOrders.insert(END, "              ==========================")
    listOrders.insert(END, " ")
    listOrders.insert(END, "  Click on a Order in the list to edit that Order.")
    listOrders.insert(END, " ")
    listOrders.insert(END, " Order ID Customer ID Order Date Paid")
    listOrders.insert(END, " -------- ----------- ---------- ----")

    for row in tobysTrucksDatabase.execute("SELECT * FROM orderTable"):
        listOrders.insert(END, " %-8s %-11s %-12s %-6s" %(row))

#----------------------------------------------------------------------------------------------------------

@requireLogin
def editOrder(event):

    listIndex = event.widget.curselection()[0]
    selectedOrderID.set( event.widget.get(listIndex)[1:5])

    queryResults = tobysTrucksDatabase.execute("SELECT * FROM orderTable WHERE orderID = ?", (selectedOrderID.get(),))
    orderRecord = queryResults.fetchone()

    orderID.set(orderRecord[0])
    orderCustomerID.set(orderRecord[1])
    orderDate.set(orderRecord[2])
    paid.set(orderRecord[3])

    setUpOrderForm("Edit Order")

    saveOrderButton = Button(mainWindow, text="Update Order Details", command=updateOrderDetails)
    saveOrderButton.place(x=320, y=320, width=200, height=30)

#----------------------------------------------------------------------------------------------------------

def updateOrderDetails():
    tobysTrucksDatabase.execute(f"""
        UPDATE orderTable
        SET 
            orderID = '{orderID.get()}',
            orderCustomerID = '{orderCustomerID.get()}',
            orderDate = '{orderDate.get()}',
            paid = '{paid.get()}'
        WHERE 
            orderID = '{selectedOrderID.get()}'
    """)
    tobysTrucksDatabase.commit()
    
    logUserAction("UPDATE", "orderTable", selectedOrderID.get(), f"Updated order: {selectedOrderID.get()}")

    messageLabel = Label(mainWindow, font="11", bg="Light blue", text="Order Updated")
    messageLabel.place(x=345, y=360)

#----------------------------------------------------------------------------------------------------------

@requireLogin
def addOrder():
    logUserAction("ACCESS", "orderTable", "", "Accessed Add Order form")
    orderID.set("")
    orderCustomerID.set("")
    orderDate.set("")
    paid.set("")

    setUpOrderForm("Add Order")

    saveOrderButton = Button(mainWindow, text="Save Order Details", command=saveNewOrder)
    saveOrderButton.place(x=320, y=320, width=200, height=30)

#----------------------------------------------------------------------------------------------------------

def saveNewOrder():
    newOrderRecord = [orderID.get(), orderCustomerID.get(), orderDate.get(), paid.get()]

    tobysTrucksDatabase.execute("INSERT INTO orderTable VALUES(?,?,?,?)",newOrderRecord)
    tobysTrucksDatabase.commit()
    
    logUserAction("INSERT", "orderTable", orderID.get(), f"Added new order: {orderID.get()}")

    messageLabel = Label(mainWindow, font="11", bg="Light blue", text="New Order Saved")
    messageLabel.place(x=320, y=360)

#----------------------------------------------------------------------------------------------------------

def setUpOrderForm(heading):
    clearMainWindow()

    editOrderFrame = Frame(mainWindow, bg="Light blue", highlightbackground="red", highlightthickness=2)
    editOrderFrame.place(x=200, y=10, width=580, height=400)

    addOrderHeadingLabel = Label(mainWindow, text=heading, font=('Arial', 16), bg="Light blue")
    addOrderHeadingLabel.place(x=320, y=12, width=200, height=30)

    Label(mainWindow, bg="Light blue", text="Order ID:").place(x=220, y=60)
    Label(mainWindow, bg="Light blue", text="CustomerID:").place(x=220, y=85)
    Label(mainWindow, bg="Light blue", text="OrderDate:").place(x=220, y=110)
    Label(mainWindow, bg="Light blue", text="Paid").place(x=220, y=135)

    # Place the Data Format Labels - Information for the user   (Validation - None Added Yet)
    Label(mainWindow, bg="Light blue", text=": Format X999").place(x=570, y=60)
    Label(mainWindow, bg="Light blue", text=": From Customer Table").place(x=570, y=85)
    Label(mainWindow, bg="Light blue", text=": Valid Date dd/mm/yyyy").place(x=570, y=110)
    Label(mainWindow, bg="Light blue", text=": Y or N").place(x=570, y=135)

    entry0 = Entry(mainWindow, textvariable=orderID, width=30, bg="yellow").place(x=320, y=60)
    entry1 = Entry(mainWindow, textvariable=orderCustomerID, width=30, bg="white").place(x=320, y=85)
    entry2 = Entry(mainWindow, textvariable=orderDate, width=30, bg="white").place(x=320, y=110)
    entry4 = Entry(mainWindow, textvariable=paid, width=30, bg="white").place(x=320, y=135)

#----------------------------------------------------------------------------------------------------------

@requireLogin
def selectOrderToDelete():
    clearMainWindow()
    
    mainWindow.title("TOBY'S TRUCKS - DELETE AN ORDER")

    enterOrderIDFrame = Frame(mainWindow, bg="Light blue", highlightbackground="blue", highlightthickness=2)
    enterOrderIDFrame.place(x=50, y=10, width=280, height=280)

    enterOrderIDHeadingLabel = Label(mainWindow, text="Select Order ID", font=('Arial', 16), bg="Light blue")
    enterOrderIDHeadingLabel.place(x=70, y=12, width=200, height=40)

    enterOrderIDLabel = Label(mainWindow, text="Enter Order ID:")
    enterOrderIDLabel.place(x=70, y=60)

    selectedOrderIDEntry = Entry(mainWindow, textvariable=orderID, width=20, bg="yellow")
    selectedOrderIDEntry.place(x=170, y=60)
    selectedOrderIDEntry.delete(0, END)

    deleteOrderButton = Button(mainWindow, text="Delete Order", width=32, command=deleteOrder)
    deleteOrderButton.place(x=70, y=100)

#----------------------------------------------------------------------------------------------------------

@requireLogin
def deleteOrder():
    tobysTrucksDatabase.execute(f"DELETE FROM orderTable WHERE orderID = '{orderID.get()}'")
    tobysTrucksDatabase.commit()
    
    logUserAction("DELETE", "orderTable", orderID.get(), f"Deleted order: {orderID.get()}")

    messageFrame = Frame(mainWindow, bg="Light blue", highlightbackground="blue", highlightthickness=2)
    messageFrame.place(x=90, y=160, width=200, height=100)

    messageLabel = Label(mainWindow, font="12", bg="Light blue", text="Order Deleted", justify=LEFT)
    messageLabel.place(x=92, y=162)


#==========================================================================================================
############ ORDER ITEMS TABLE ############

def listOrderItems():
    clearMainWindow()
    mainWindow.title("TOBY'S TRUCKS - ORDER ITEMS LIST")

    orderItemsList = Listbox(mainWindow, width=80, height=20, font=("Consolas", 14), selectmode="single")
    orderItemsList.place(x=30, y=15)
    orderItemsList.config(bg="Light blue", highlightbackground="blue", highlightthickness=2)

    orderItemsList.bind("<<ListboxSelect>>", editOrderItem)

    orderItemsList.insert(END, " ")
    orderItemsList.insert(END, "              TOBY'S TRUCKS - ORDER ITEMS LIST")
    orderItemsList.insert(END, "              ================================")
    orderItemsList.insert(END, " ")
    orderItemsList.insert(END, "  Click on an Order Item in the list to edit that Order Item.")
    orderItemsList.insert(END, " ")
    orderItemsList.insert(END, " Order ID Truck ID Quantity")
    orderItemsList.insert(END, " -------- ------- --------")

    for row in tobysTrucksDatabase.execute("SELECT * FROM orderItemsTable ORDER BY orderItemsOrderID, orderItemsTruckID"):
        orderItemsList.insert(END, " %-9s %-10s %-5d" %(row))

#----------------------------------------------------------------------------------------------------------

@requireLogin
def editOrderItem(event):
    listIndex = event.widget.curselection()[0]

    selectedOrderID.set( event.widget.get(listIndex)[1:5])
    selectedTruckID.set( event.widget.get(listIndex)[11:15])

    queryResults = tobysTrucksDatabase.execute(f"""
        SELECT * FROM orderItemsTable
        WHERE orderItemsOrderID = '{selectedOrderID.get()}'
        AND orderItemsTruckID = '{selectedTruckID.get()}'
    """)
    orderItemRecord = queryResults.fetchone()

    orderItemsOrderID.set(orderItemRecord[0])
    orderItemsTruckID.set(orderItemRecord[1])
    quantity.set(orderItemRecord[2])

    setUpOrderItemsForm("Edit Order Items")

    saveOrderItemsButton = Button(mainWindow, text="Update Order Item Details", command=updateOrderItemDetails)
    saveOrderItemsButton.place(x=320, y=320, width=200, height=30)

#----------------------------------------------------------------------------------------------------------

def updateOrderItemDetails():
    tobysTrucksDatabase.execute(f"""
        UPDATE orderItemsTable
        SET
            orderItemsOrderID = '{orderItemsOrderID.get()}',
            orderItemsTruckID = '{orderItemsTruckID.get()}',
            quantity = '{quantity.get()}'
        WHERE
            orderItemsOrderID = '{selectedOrderID.get()}'
        AND orderItemsTruckID = '{selectedTruckID.get()}'
    """)
    tobysTrucksDatabase.commit()
    
    logUserAction("UPDATE", "orderItemsTable", f"{selectedOrderID.get()}-{selectedTruckID.get()}", f"Updated order item: Order {selectedOrderID.get()}, Truck {selectedTruckID.get()}")

    messageLabel = Label(mainWindow, font="11", bg="Light blue", text="Order Items Updated")
    messageLabel.place(x=335, y=360)

#----------------------------------------------------------------------------------------------------------

@requireLogin
def addOrderItem():
    logUserAction("ACCESS", "orderItemsTable", "", "Accessed Add Order Item form")
    orderItemsOrderID.set("")
    orderItemsTruckID.set("")
    quantity.set("")

    setUpOrderItemsForm("Add Order Item")

    saveOrderItemButton = Button(mainWindow, text="Save Order Item Details", command=saveNewOrderItem)
    saveOrderItemButton.place(x=320, y=320, width=200, height=30)

#----------------------------------------------------------------------------------------------------------

def saveNewOrderItem():
    newOrderItemsRecord = [orderItemsOrderID.get(), orderItemsTruckID.get(), quantity.get()]

    tobysTrucksDatabase.execute("INSERT INTO orderItemsTable VALUES(?,?,?)", newOrderItemsRecord)
    tobysTrucksDatabase.commit()
    
    logUserAction("INSERT", "orderItemsTable", f"{orderItemsOrderID.get()}-{orderItemsTruckID.get()}", f"Added order item: Order {orderItemsOrderID.get()}, Truck {orderItemsTruckID.get()}")

    messageLabel = Label(mainWindow, font="11", bg="Light blue", text="New Order Item Saved")
    messageLabel.place(x=320, y=360)

#----------------------------------------------------------------------------------------------------------

def setUpOrderItemsForm(heading):
    clearMainWindow()

    frameEditOrderItem = Frame(mainWindow, bg="Light blue", highlightbackground="red", highlightthickness=2)
    frameEditOrderItem.place(x=200, y=10, width=580, height=400)

    labelHeadingAddOrderItem = Label(mainWindow, text=heading, font=('Arial', 16), bg="Light blue")
    labelHeadingAddOrderItem.place(x=320, y=12, width=200, height=30)

    # Place the Labels
    Label(mainWindow, bg="Light blue", text="Order ID:").place(x=220, y=60)
    Label(mainWindow, bg="Light blue", text="Truck ID:").place(x=220, y=85)
    Label(mainWindow, bg="Light blue", text="Quantity:").place(x=220, y=110)

    # Place the Data Format Labels - Information for the user    (Validation - None Added Yet)
    Label(mainWindow, bg="Light blue", text=": From Order Table").place(x=570, y=60)
    Label(mainWindow, bg="Light blue", text=": From Truck Table").place(x=570, y=85)
    Label(mainWindow, bg="Light blue", text=": 1 - 100").place(x=570, y=110)

    entry0 = Entry(mainWindow, textvariable=orderItemsOrderID, width=30, bg="yellow").place(x=320, y=60)
    entry1 = Entry(mainWindow, textvariable=orderItemsTruckID, width=30, bg="yellow").place(x=320, y=85)
    entry2 = Entry(mainWindow, textvariable=quantity, width=30, bg="white").place(x=320, y=110)

#----------------------------------------------------------------------------------------------------------

@requireLogin
def selectOrderItemToDelete():
    clearMainWindow()
    mainWindow.title("TOBY'S TRUCKS - DELETE A ORDER ITEM")

    enterOrderItemFrame = Frame(mainWindow, bg="Light blue", highlightbackground="blue", highlightthickness=2)
    enterOrderItemFrame.place(x=50, y=10, width=380, height=280)

    headingLabel = Label(mainWindow, text="Select Order Item to Delete", font=('Arial', 16), bg="Light blue")
    headingLabel.place( x=70, y=12, width=300, height=40)

    enterOrderItemOrderIDLabel = Label(mainWindow, text="Enter Order Item Order ID:")
    enterOrderItemOrderIDLabel.place( x=70, y=60)
    enterOrderItemTruckIDLabel = Label(mainWindow, text="Enter Order Item Truck ID:")
    enterOrderItemTruckIDLabel.place( x=70, y=85)

    orderItemsOrderID.set("")
    orderItemsTruckID.set("")

    entrySelectedOrderItemOrderID = Entry(mainWindow, textvariable=orderItemsOrderID, width=20, bg="yellow")
    entrySelectedOrderItemOrderID.place(x=280, y=60)
    entrySelectedOrderItemTruckID = Entry(mainWindow, textvariable=orderItemsTruckID, width=20, bg="yellow")
    entrySelectedOrderItemTruckID.place(x=280, y=85)


    buttonDeleteOrderItem = Button(mainWindow, text="Delete Order Item", width=32, command=deleteOrderItem)
    buttonDeleteOrderItem.place(x=100, y=130)

#----------------------------------------------------------------------------------------------------------

@requireLogin
def deleteOrderItem():
    tobysTrucksDatabase.execute(f"DELETE FROM orderItemsTable WHERE orderItemsOrderID = '{orderItemsOrderID.get()}' AND orderItemsTruckID = '{orderItemsTruckID.get()}'")
    tobysTrucksDatabase.commit()
    
    logUserAction("DELETE", "orderItemsTable", f"{orderItemsOrderID.get()}-{orderItemsTruckID.get()}", f"Deleted order item: Order {orderItemsOrderID.get()}, Truck {orderItemsTruckID.get()}")

    messageFrame = Frame(mainWindow, bg="Light blue", highlightbackground="blue", highlightthickness=2)
    messageFrame.place(x=90, y=160, width=200, height=100)

    messageLabel = Label(mainWindow, font="12", bg="Light blue", text="Order Item Deleted", justify=LEFT)
    messageLabel.place(x=92, y=162)
    
#==========================================================================================================
############ SYSTEM LOGS ############

def displaySystemLogs():
    """Display system activity logs"""
    clearMainWindow()
    mainWindow.title("TOBY'S TRUCKS - SYSTEM LOGS")

    logsList = Listbox(mainWindow, width=120, height=25, font=("Consolas", 9), selectmode="single")
    logsList.place(x=30, y=15)
    logsList.config(bg="Light blue", highlightbackground="blue", highlightthickness=2)

    logsList.insert(END, " ")
    logsList.insert(END, "                               TOBY'S TRUCKS - SYSTEM ACTIVITY LOGS")
    logsList.insert(END, "                               ===================================")
    logsList.insert(END, " ")
    logsList.insert(END, " Log ID  User ID   Username     Action      Table       Record ID   Timestamp           Details")
    logsList.insert(END, " ------- --------- ------------ ----------- ----------- ----------- ------------------- ---------------------------------")

    queryResults = tobysTrucksDatabase.execute("""
        SELECT logID, userID, username, action, tableName, recordID, timestamp, details
        FROM logsTable
        ORDER BY logID DESC
    """)

    for row in queryResults:
        logLine = " %-7s %-9s %-12s %-11s %-11s %-11s %-19s %s" % (
            str(row[0]), str(row[1] or ""), str(row[2] or ""), 
            str(row[3] or ""), str(row[4] or ""), str(row[5] or ""), 
            str(row[6] or ""), str(row[7] or "")
        )
        logsList.insert(END, logLine)

#==========================================================================================================
############ REPORTS ############


def selectSupplierForOrderNotes():
    clearMainWindow()
    mainWindow.title("TOBY'S TRUCKS - ORDER TRUCKS FROM SUPPLIER")

    labelSupplierID = Label(mainWindow, text="Select Supplier ID for Order Notes : ", font=('Arial', 10))
    labelSupplierID.place(x=120, y=8, width=220, height=40)
    
    comboBoxValues = []
    for row in tobysTrucksDatabase.execute("SELECT supplierID from supplierTable"):
        comboBoxValues += row

    comboBoxSupplierIDs = ttk.Combobox(state="readonly", textvariable=supplierID, values=comboBoxValues)
    comboBoxSupplierIDs.place(x=360, y=17)

    comboBoxSupplierIDs.bind("<<ComboboxSelected>>", displayOrderNotes)
    
#----------------------------------------------------------------------------------------------------------

def displayOrderNotes(event):
    mainWindow.title("TOBY'S TRUCKS - ORDER NOTES")

    listReport = Listbox(mainWindow, width=71, height=25, font=("Consolas",10), selectmode="single")
    listReport.place(x=100, y=55)
    listReport.config(bg="Light blue", highlightbackground="blue", highlightthickness=2)

    queryResults = tobysTrucksDatabase.execute(f"""
        SELECT 
            supplierID, supplierName, supplierAddress, 
            supplierPhone, supplierEmail
        FROM 
            supplierTable
        WHERE
            supplierID = '{supplierID.get()}'
        ORDER BY supplierID
    """).fetchall()

    for supplierRow in queryResults:
        listReport.insert( END, "  ")
        listReport.insert( END, " =====================================================================")
        listReport.insert( END, "          TOBY'S TRUCKS - FOR ALL YOUR TRUCKING NEEDS                 ")
        listReport.insert( END, " ---------------------------------------------------------------------")
        listReport.insert( END, "    Toby's Trucks, Spokane, South Wales.     Tel 018871 8181181       ")
        listReport.insert( END, "    enquiries@TobysTrucks.com          VAT Reg Number 120987245       ")
        listReport.insert( END, " ---------------------------------------------------------------------")
        listReport.insert( END, "               Order Note for Supplier ID :" + supplierRow[0]          )
        listReport.insert( END, " ---------------------------------------------------------------------")
        listReport.insert( END, "               Supplier Name     : " + supplierRow[1]  )
        listReport.insert( END, "               Supplier Address  : " + supplierRow[2]  )        
        listReport.insert( END, "               Supplier Phone    : " + supplierRow[3]  )
        listReport.insert( END, "               Supplier Email    : " + supplierRow[4]  )
        listReport.insert( END, " ---------------------------------------------------------------------")
        listReport.insert( END, " Please send the following trucks :")
        listReport.insert( END, " ---------------------------------------------------------------------")
        listReport.insert( END, " Truck Truck     Truck     Truck  Truck      ReOrder  Sub")
        listReport.insert( END, " ID   Make     Model    Size  Price     Amount   Total")
        listReport.insert( END, " ---- -------- -------- ----  --------- -------  ---------")  

        queryResults = tobysTrucksDatabase.execute(f"""
            SELECT 
                truckID, make, model, size, truckSupplierID,
                buyingPrice, stockLevel, reorderLevel, reorderAmount
            FROM truckTable
            WHERE 
                truckSupplierID = '{supplierRow[0]}'
            AND stockLevel <= reorderLevel
            ORDER BY truckID
        """)

        grandTotal = float(0)

        for truckRow in queryResults:
            truckLine=( " %-5s"     %(truckRow[0]) + 
                        "%-9s"      %(truckRow[1]) +
                        "%-10s"     %(truckRow[2]) + 
                        "%-5s"      %(truckRow[3]) +
                        "£%8.2f"    %(truckRow[5]) +
                        "%4d"       %(truckRow[8]) +
                        "£%8.2f"    %(truckRow[5]  * truckRow[8])
                    )
            listReport.insert(END, truckLine)
            grandTotal += (truckRow[5]) * (truckRow[8])

        if grandTotal > 0:
            listReport.insert( END, " =====================================================================")
            listReport.insert( END, " "*30 + "      Grand Total  £" + "%8.2f" %(grandTotal)                 )              
            listReport.insert( END, " =====================================================================")
        else:            
            listReport.insert( END, " =====================================================================")
            listReport.insert( END, "               ***  NO TRUCKS TO ORDER CURRENTLY  ***                 ")            
            listReport.insert( END, " =====================================================================")

#----------------------------------------------------------------------------------------------------------
########  RECEIPT  ####### 

def selectOrderForReceipt():
    clearMainWindow()
    mainWindow.title("TOBY'S TRUCKS - ORDER RECEIPT")
    
    enterOrderIDLabel = Label(mainWindow, text="Select Order ID for Receipt : ", font=('Arial', 10))
    enterOrderIDLabel.place(x=110, y=8, width=200, height=40)

    comboBoxValues = []
    
    for row in tobysTrucksDatabase.execute("SELECT orderID from orderTable"):
        comboBoxValues += row

    comboBoxOrderIDs = ttk.Combobox(state="readonly", textvariable=orderID, values=comboBoxValues)
    comboBoxOrderIDs.place(x=300, y=17)
    comboBoxOrderIDs.bind("<<ComboboxSelected>>", displayReceipt)

#----------------------------------------------------------------------------------------------------------

def displayReceipt(event):
    mainWindow.title("TOBY'S TRUCKS - RECEIPT")

    listReport = Listbox(mainWindow, width=71, height=24, font=("Consolas",10))
    listReport.place(x=100, y=55)
    listReport.config(bg="Light blue", highlightbackground="blue", highlightthickness=2)

    queryResults = tobysTrucksDatabase.execute(f"""
        SELECT 
            orderID, orderCustomerID, orderDate, paid,
            customerID, customerName, customerAddress, 
            customerPhone, customerEmail
        FROM 
            orderTable, customerTable
        WHERE
            orderID = '{orderID.get()}'
        AND orderCustomerID = customerID
    """).fetchall()

    currentDate = date.today().strftime('%d-%m-%Y')

    for row in queryResults:
        listReport.insert( END, " ")
        listReport.insert( END, " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        listReport.insert( END, "          TOBY'S TRUCKS - RECEIPT - THANK YOU FOR YOUR ORDER          ")
        listReport.insert( END, " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        listReport.insert( END, " Toby's Trucks, Truck Island, Scotland.        Tel 018871 8181181     ")
        listReport.insert( END, " E-Mail  enquiries@TobysTrucks.com          VAT Reg Number 120987245  ")
        listReport.insert( END, " ---------------------------------------------------------------------")
        listReport.insert( END, "   Receipt for Order ID : " + row[0] + "        Date : " + currentDate )
        listReport.insert( END, " ---------------------------------------------------------------------")
        listReport.insert( END, " ORDER ID    : " + "%-14s"  %(row[0]) + " CUSTOMER ID : "     + row[4] )
        listReport.insert( END, " Order Date  : " + "%-14s"  %(row[2]) + " Name        : "     + row[5] )        
        listReport.insert( END, " Paid        : " + "%-14s"  %(row[3]) + " Address     : "     + row[6] )
        listReport.insert( END, " "*29                                 + " Phone       : "     + row[7] )
        listReport.insert( END, " "*29                                 + " Email       : "     + row[8] )
        listReport.insert( END, " ---------------------------------------------------------------------")
        listReport.insert( END, " Truck Truck     Truck     Truck  Truck      Truck     Sub")
        listReport.insert( END, " ID   Make     Model    Size  Price     Quantity Total")
        listReport.insert( END, " ---- -------- -------- ----  --------- -------  ---------")  

    queryResults = tobysTrucksDatabase.execute(f"""
        SELECT 
            orderItemsOrderID, orderItemstruckID, quantity,
            truckID, make, model, size, sellingPrice
        FROM   
            orderItemsTable, truckTable 
        WHERE
            orderItemsOrderID = '{orderID.get()}'
        AND orderItemstruckID = truckID
    """).fetchall()

    grandTotal = float(0)

    for truckRow in queryResults:
        truckLine=( " %-5s"     %(truckRow[3]) +
                    "%-9s"      %(truckRow[4]) +
                    "%-10s"     %(truckRow[5]) +
                    "%-5s"      %(truckRow[6]) +
                    "£%8.2f"    %(truckRow[7]) +
                    "%4d"       %(truckRow[2]) +
                    "£%8.2f"    %(truckRow[7] * truckRow[2])
                )
        listReport.insert(END, truckLine)
        grandTotal += (truckRow[7]) * (truckRow[2])

    if grandTotal > 0:
        listReport.insert(END, " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        listReport.insert(END, " "*30 + "      Grand Total  £" + "%8.2f" %(grandTotal))
        listReport.insert(END, " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    else:
        listReport.insert(END, "=====================================================================")
        listReport.insert(END, "                    ***  NO TRUCKS ON THE ORDER   ***                ")
        listReport.insert(END, "=====================================================================")


#----------------------------------------------------------------------------------------------------------
########  PROFIT REPORT  #######

def selectYearForProfitReport():
    clearMainWindow()
    mainWindow.title("TOBY'S TRUCKS - PROFIT REPORT")

    labelEnterOrderID = Label(mainWindow, text="Select Year for Profit Report : ", font=('Arial', 10))
    labelEnterOrderID.place( x=110, y=8, width=200, height=40)
    
    currentYear = int(date.today().strftime('%Y'))
    comboBoxValues = []

    for i in range(currentYear - 5, currentYear + 6):
        comboBoxValues.append(i)

    comboBoxYears = ttk.Combobox(state="readonly", textvariable=yearForProfitReport, values=comboBoxValues)
    comboBoxYears.place(x=300, y=17)
    comboBoxYears.bind("<<ComboboxSelected>>", profitReport)

#----------------------------------------------------------------------------------------------------------
    
def profitReport(event):
    mainWindow.title("TOBY'S TRUCKS - PROFIT REPORT")

    listReport = Listbox(mainWindow, width=71, height=26, font=("Consolas", 10))
    listReport.place(x=100, y=55)
    listReport.config(bg="Light blue", highlightbackground="blue", highlightthickness=2)

    currentDate = date.today().strftime('%d-%m-%Y')

    listReport.insert(END, " ")
    listReport.insert(END, " =====================================================================")
    listReport.insert(END, "         TOBY'S TRUCKS - PROFIT REPORT FOR " + yearForProfitReport.get())
    listReport.insert(END, " =====================================================================")
    listReport.insert(END, "         Created on  : " + currentDate )
    listReport.insert(END, " ---------------------------------------------------------------------")

    currentDate = date.today().strftime('%d-%m-%Y')

    queryResults = tobysTrucksDatabase.execute(f"""
        SELECT 
            orderID, orderDate, paid,
            orderItemsOrderID, orderItemstruckID, quantity,
            truckID, buyingPrice, sellingPrice,
            ((sellingPrice - buyingPrice) * quantity)
        FROM   
            orderTable, orderItemsTable, truckTable
        WHERE  
            orderID = orderItemsOrderID
        AND truckID = orderItemstruckID
        AND SUBSTR(orderDate,7,10) = '{yearForProfitReport.get()}'
    """)
    allQueryResults = queryResults.fetchall()

    totalTrucksSold = int(0)
    totalOutGoings = float(0)
    totalIncome = float(0)
    unPaidIncome = float(0)
    unPaidProfit = float(0)
    totalProfit = float(0)

    listReport.insert( END, " Order Order      Paid Quantity Truck  Buying     Selling    Order Item ")
    listReport.insert( END, " ID    Date                     ID    Price      Price      Profit     ")
    listReport.insert( END, " ----- ---------- ---- -------- ----  ---------- ---------- ---------- ")
    
    for row in allQueryResults:
        orderItemLine=( "%-6s"    %(row[0])  + 
                        "%-12s"   %(row[1])  + 
                        "%-8s"    %(row[2])  + 
                        "%-5s"    %(row[5])  + 
                        "%-5s"    %(row[6])  +
                        "£%8.2f"  %(row[7])  +
                        "£%8.2f"  %(row[8])  +
                        "£%8.2f"  %(row[9])  
                    )
        listReport.insert(END, orderItemLine)
        totalOutGoings += (row[7] * row[5])
        totalTrucksSold += int(row[5])

        if row[2] == "Y":
            totalProfit += row[9]
            totalIncome += (row[8] * row[5])
        else:
            unPaidProfit += row[9]
            unPaidIncome += (row[8] * row[5])
            
    listReport.insert( END, " =====================================================================")             
    listReport.insert( END, " Total Trucks Sold        " + "  %8d"  %(totalTrucksSold))
    listReport.insert( END, " Total Out Goings        " + "£%9.2f" %(totalOutGoings))    
    listReport.insert( END, " Total Actual Income     " + "£%9.2f" %(totalIncome))
    listReport.insert( END, " ---------------------------------------------------------------------")
    listReport.insert( END, " TOTAL ACTUAL PROFIT     " + "£%9.2f" %(totalProfit))
    listReport.insert( END, " ---------------------------------------------------------------------")
    listReport.insert( END, " Missing Unpaid Income   " + "£%9.2f" %(unPaidIncome))
    listReport.insert( END, " Missing Unpaid Profit   " + "£%9.2f" %(unPaidProfit))
    listReport.insert( END, " =====================================================================")

#----------------------------------------------------------------------------------------------------------
########  TRUCKS IN STOCK REPORT  #######

def trucksInStock():
    clearMainWindow()
    mainWindow.title("TOBY'S TRUCKS - TRUCKS IN STOCK")
    
    listReport = Listbox(mainWindow, width=71, height=26, font=("Consolas",10))
    listReport.place( x=100, y=15)
    listReport.config( bg="Light blue", highlightbackground="blue", highlightthickness=2)

    currentDate = date.today().strftime('%d-%m-%Y')

    listReport.insert( END, " ")
    listReport.insert( END, " =====================================================================")
    listReport.insert( END, "    TOBY'S TRUCKS - STOCK REPORT WITH TOTAL                           ")
    listReport.insert( END, " =====================================================================")
    listReport.insert( END, "         Created on  : " + currentDate )
    listReport.insert( END, " ---------------------------------------------------------------------")
    listReport.insert( END, " Truck Truck     Truck     Truck   Stock ")
    listReport.insert( END, " ID   Make     Model    Size   Level")
    listReport.insert( END, " ---- -------- -------- ----   --------")
    
    queryResults = tobysTrucksDatabase.execute("SELECT truckID, make, model, size, stockLevel FROM truckTable ORDER BY truckID")
    allQueryResults = queryResults.fetchall()
    
    for row in allQueryResults:
        listReport.insert( END, " %-4s %-8s %-8s  %-4s %4d" %(row))

    listReport.insert( END, " ---------------------------------------------------------------------")
    queryResults = tobysTrucksDatabase.execute("SELECT SUM(stockLevel) FROM truckTable")
    totalStock = queryResults.fetchone()[0]

    listReport.insert( END, " =====================================================================")
    listReport.insert( END, " Total Trucks in stock :         " + str(totalStock) )
    listReport.insert( END, " =====================================================================")

# =======================================================================================================
#### CUSTOM SQL QUERY ####

def setupCustomQuery():
    clearMainWindow()
    mainWindow.title("TOBY'S TRUCKS - CUSTOM SQL QUERY")

    labelEnterSQL = Label(mainWindow, text="Enter SQL Query : ", font=('Arial', 10))
    labelEnterSQL.place(x=100, y=8, width=120, height=40)

    entrySQLQuery = Entry(mainWindow, textvariable=customSQLQueryString, width=75, bg="light blue")
    entrySQLQuery.place(x=220, y=17)
    entrySQLQuery.delete(0, END)

    buttonRunSQL = Button(mainWindow, text="Run SQL Query", width=20, bg="light green", command=runCustomQuery)
    buttonRunSQL.place(x=700, y=15)


def runCustomQuery():
    mainWindow.title("TOBY'S TRUCKS - CUSTOM SQL QUERY RESULTS")

    listReport = Listbox(mainWindow, width=100, height=25, font=("Consolas",10))
    listReport.place(x=30, y=55)
    listReport.config(bg="Light blue", highlightbackground="blue", highlightthickness=2)

    try:
        queryResults = tobysTrucksDatabase.execute(customSQLQueryString.get())
        allQueryResults = queryResults.fetchall()

        if len(allQueryResults) >= 1:

            listReport.destroy()
            resultText = scrolledtext.ScrolledText(mainWindow, width=100, height=25, font=("Consolas", 10), wrap="word")
            resultText.place(x=30, y=55)
            resultText.config(bg="Light blue", highlightbackground="blue", highlightthickness=2)

            resultText.insert(END, str(allQueryResults))
            resultText.config(state="disabled")

            def copy_data():
                mainWindow.clipboard_clear()
                mainWindow.clipboard_append(resultText.get("0.0", "end").strip())

            def save_data_to_file():
                file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[
                    ("Text files", "*.txt"), 
                    ("Javascript Object Notation (JSON)", "*.json"), 
                    ("Binary Archive", "*.bin"),
                    ("All files", "*.*")
                ])
                if file_path:
                    with open(file_path, 'w') as file:
                        file.write(resultText.get("0.0", "end").strip())
                    messagebox.showinfo("Save Successful", f"Data saved to {file_path}.")
                else:
                    messagebox.showwarning("Save Cancelled", "The filepath you selected did not exist or could not be created. Please try again later.")

            copyButton = Button(mainWindow, text="Copy Data to Clipboard", command=copy_data, bg="light green")
            copyButton.place(x=720, y=415, width=130, height=30)

            saveButton = Button(mainWindow, text="Save Data to File", command=save_data_to_file, bg="light green")
            saveButton.place(x=720, y=455, width=130, height=30)

        else:
            listReport.insert(END, " No Records Found ")

    except Exception as e:
        messageLabel = Label(mainWindow, font="11", bg="red", text="Error in SQL Query: " + str(e))
        messageLabel.place(x=320, y=360)


#=========================================================================================================
#### CALL THE MAIN FUNCTION ####


if __name__ == "__main__":
    main()


#=========================================================================================================