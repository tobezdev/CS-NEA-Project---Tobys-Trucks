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

#### IMPORTS ####
import sqlite3                      # SQL Commands
from os.path import isfile          # We need this to check if the database exists
from datetime import date           # We need this for todays date and finding the year
from tkinter import *               # Tkinter
from tkinter import messagebox      # Tkinter Message Box
from tkinter import ttk             # We need this for the Tkinter Combo Box (Drop Down List Box)

#----------------------------------------------------------------------------------------------------------

#### DATABASE SETUP ####

# DATABASE - If the database exists in the same folder as the program it will be opened.
#            If it does not exist it will be created with an tables.

databaseExists = isfile("BOSTON BIKES DATABASE.db")   # databaseExist - Boolean Variable - True or False  

# OPEN OR CREATE THE DATABASE - AS A GLOBAL    
bostonBikesDatabase = sqlite3.connect("BOSTON BIKES DATABASE.db")

# IF THIS IS A NEW DATABASE - CREATE THE TABLES        
if not databaseExists:

    print("The database 'BOSTON BIKES DATABASE.db' did not exist. It has been created.")

    sqlCommand = ( "CREATE TABLE bikeTable("      # FILED FORMAT / VALIDATION #
                   "bikeID TEXT PRIMARY KEY,"     # XX99 Unique
                   "make TEXT,"                   # Max 8 Characters
                   "model TEXT,"                  # Max 8 Characters
                   "size TEXT,"                   # XS,S,M,L,XL,XXL
                   "bikeSupplierID TEXT,"         # Supplier ID from Supplier table
                   "buyingPrice FLOAT,"           # Max £9999.99
                   "sellingPrice FLOAT,"          # Max £9999.99
                   "stockLevel INTEGER,"          # 0-100
                   "reorderLevel INTEGER,"        # 0-100
                   "reorderAmount INTEGER)" )     # 0-100

    bostonBikesDatabase.execute(sqlCommand)
    bostonBikesDatabase.commit()

    sqlCommand = ( "CREATE TABLE supplierTable("  
                   "supplierID TEXT PRIMARY KEY," # XXXXXXXX (8 Characters) Unique
                   "supplierName TEXT,"           # Max 14 Characters
                   "supplierAddress TEXT,"        # Max 14 Characters
                   "supplierPhone TEXT,"          # 11 Digits
                   "supplierEmail TEXT)" )        # Max 14 Characters
   
    bostonBikesDatabase.execute(sqlCommand)
    bostonBikesDatabase.commit()  

    sqlCommand = ( "CREATE TABLE customerTable("
                   "customerID TEXT PRIMARY KEY," # 4 Digits
                   "customerName TEXT,"           # Max 14 Characters
                   "customerAddress TEXT,"        # Max 14 Characters
                   "customerPhone TEXT,"          # 11 Digits
                   "customerEmail TEXT)" )        # Max 14 Characters

    bostonBikesDatabase.execute(sqlCommand)
    bostonBikesDatabase.commit()

    sqlCommand = ( "CREATE TABLE orderTable("
                   "orderID TEXT PRIMARY KEY,"    # Format - X999
                   "orderCustomerID TEXT,"        # Customer ID from Customer Table
                   "orderDate TEXT,"              # Valid Date dd/mm/yyyy
                   "paid TEXT)" )                 # Y or N  
   
    bostonBikesDatabase.execute(sqlCommand)
    bostonBikesDatabase.commit()  

    sqlCommand = ( "CREATE TABLE orderItemsTable("
                   "orderItemsOrderID TEXT,"      # Order ID from Order Table ## COMBINED ##
                   "orderItemsBikeID TEXT,"       # Bike ID from Bike Table   ##   KEY    ##
                   "Quantity INTEGER)" )          # 1 - 100  Integer
   
    bostonBikesDatabase.execute(sqlCommand)
    bostonBikesDatabase.commit()

#----------------------------------------------------------------------------------------------------------

#### TKINTER SETUP ####

windowMain = Tk()

bostonBikesPicture = PhotoImage(file = "BOSTON Bikes Picture.png")

bikeID = StringVar()    # Tkinter Stringvar()s for Bike details
make = StringVar()
model = StringVar()
size = StringVar()
bikeSupplierID = StringVar()
buyingPrice = StringVar()
sellingPrice = StringVar()
stockLevel = StringVar()
reorderLevel = StringVar()
reorderAmount = StringVar()

supplierID = StringVar()    # Tkinter Stringvar()s for Supplier details
supplierName = StringVar()
supplierAddress = StringVar()
supplierPhone = StringVar()
supplierEmail = StringVar()

customerID = StringVar()        # Tkinter Stringvar()s for Customer details
customerName = StringVar()
customerAddress = StringVar()
customerPhone = StringVar()
customerEmail = StringVar()

orderID = StringVar()           # Tkinter Stringvar()s for Order details
orderCustomerID = StringVar()
orderDate = StringVar()
paid = StringVar()

orderItemsOrderID = StringVar()  # Tkinter Stringvar()s for Order Items details
orderItemsBikeID = StringVar()
quantity = StringVar()

selectedBikeID = StringVar()     # Tkinter StringVar()s for Changing Key Fields
selectedSupplierID = StringVar() 
selectedCustomerID = StringVar()
selectedOrderID = StringVar()

yearForProfitReport = StringVar()

firstTime = True












#==========================================================================================================

#### THE MAIN FUNCTION ####

def main():
   
    setUpWindowMain()

    windowMain.mainloop()

#----------------------------------------------------------------------------------------------------------

def setUpWindowMain():

    global firstTime
 
    # Main Window - windowMain  
    windowMain.geometry("870x525")
    windowMain.title("BOSTON BIKES")
    windowMain.resizable (True, True)

    # Add a Menu Bar to windowMain - menuBar
    menuBar = Menu(windowMain)

    # File Menu - menuFile
    menuFile = Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="File", menu = menuFile)
    menuFile.add_command(label="Exit", command = exitProgram)

    # Bike Menu - menuBikes
    menuBikes = Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Bikes", menu = menuBikes)
    menuBikes.add_command(label="List Bikes", command = listBikes)
    menuBikes.add_command(label="Add a New Bike", command = addBike)
    menuBikes.add_command(label="Edit a Bike", command = listBikes)
    menuBikes.add_command(label="Delete a Bike", command = selectBikeToDelete)
       
    # Supplier Menu - menuSuppliers
    menuSuppliers = Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Suppliers", menu = menuSuppliers)
    menuSuppliers.add_command(label="List Suppliers", command = listSuppliers)
    menuSuppliers.add_command(label="Add a New Supplier", command = addSupplier)
    menuSuppliers.add_command(label="Edit a Supplier", command = listSuppliers)
    menuSuppliers.add_command(label="Delete a Supplier", command = selectSupplierToDelete)

    # Customer Menu - menuCustomers
    menuCustomers = Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Customers", menu = menuCustomers)
    menuCustomers.add_command(label="List Customers", command = listCustomers)
    menuCustomers.add_command(label="Add a New Customer", command = addCustomer)
    menuCustomers.add_command(label="Edit a Customer", command = listCustomers)
    menuCustomers.add_command(label="Delete a Customer", command = selectCustomerToDelete)

    # Order Menu - menuOrders
    menuOrders = Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Orders", menu = menuOrders)
    menuOrders.add_command(label="List Orders", command = listOrders)
    menuOrders.add_command(label="Add a New Order", command = addOrder)
    menuOrders.add_command(label="Edit an Order", command = listOrders)
    menuOrders.add_command(label="Delete an Order", command = selectOrderToDelete)

    # Order Items Menu - menuOrderitems
    menuOrderItems = Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Order Items", menu = menuOrderItems)
    menuOrderItems.add_command(label="List Order Items", command = listOrderItems)
    menuOrderItems.add_command(label="Add a New Order Item", command = addOrderItem)
    menuOrderItems.add_command(label="Edit an Order Item", command = listOrderItems)
    menuOrderItems.add_command(label="Delete an Order Item", command = selectOrderItemToDelete)

   # Reports Menu - menuReports
    menuReports = Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Reports", menu = menuReports)
    menuReports.add_command(label="Reorder Notes", command = selectSupplierForOrderNotes)
    menuReports.add_command(label="Receipts", command = selectOrderForReceipt)
    menuReports.add_command(label="Profit Report", command = selectYearForProfitReport)
    menuReports.add_command(label="Bikes In Stock", command = bikesInStock)
   
    # Configure the Window with the Menu Bar
    windowMain.config(menu=menuBar)
   
    # Add the Window Icon - Popcorn Icon File
    windowMain.iconbitmap("Boston Bikes Icon.ico")
   
    # Create canvas for the Picture and Add Picture first time window opens
    if firstTime == True:    
        canvasPicture = Canvas( windowMain, width=1000, height=500)
        canvasPicture.place( x=65, y=5)
        canvasPicture.create_image(370, 240, image = bostonBikesPicture)

    firstTime = False
   
#----------------------------------------------------------------------------------------------------------

def exitProgram():

    answer = messagebox.askyesno("EXIT PROGRAM", "Are You Sure?")

    if answer == True:
        windowMain.destroy()
       
#----------------------------------------------------------------------------------------------------------

def clearWindowMain():
     
    for widgets in windowMain.winfo_children():
        widgets.destroy()

    setUpWindowMain()



#==========================================================================================================

############ BIKE TABLE ############
   
#==========================================================================================================

def listBikes():

    clearWindowMain()
   
    # Set Title
    windowMain.title("BOSTON Bikes - Bike List")

    # Place the Listbox to contain the Bike List
    listBikes = Listbox(windowMain, width=80, height=20, font=("Consolas",14), selectmode="single")
    listBikes.place( x=30, y=15)
    listBikes.config( bg="Light blue", highlightbackground="blue", highlightthickness=2)

    ## This line calls the function - editBike - when a bike is clicked in listBikes
    listBikes.bind("<<ListboxSelect>>", editBike)

    # Add Column Headings to List Box
    listBikes.insert(END, " ")
    listBikes.insert(END, "              BOSTON BIKES - BIKE LIST")
    listBikes.insert(END, "              ========================")
    listBikes.insert(END, " ")
    listBikes.insert(END, "  Click on a Bike in the list to edit that bike.")
    listBikes.insert(END, " ")
    listBikes.insert(END, " Bike Bike     Bike     Bike Bike      Buying   Selling  Stock Reorder ReOrder")
    listBikes.insert(END, " ID   Make     Model    Size Supplier  Price    Price          Level   Amount")
    listBikes.insert(END, " ---- -------- -------- ---- --------  -------  -------  ----- ------- -------")
   
    sqlCommand = "SELECT * FROM bikeTable"

    for row in bostonBikesDatabase.execute(sqlCommand):
           
        listBikes.insert( END, " %-4s %-8s %-8s %-4s %-8s %8.2f %8.2f %4d %6d %6d" %(row))

#----------------------------------------------------------------------------------------------------------

# EDIT A BIKE - SET UP THE EDIT WINDOW AND LOAD BIKE DETAILS IN

def editBike(event):
   
    listIndex = event.widget.curselection()[0] # Find index number of the item clicked in the list      

    selectedBikeID.set( event.widget.get(listIndex)[1:5] ) # Find the clicked bikeID

    sqlCommand = "SELECT * from bikeTable WHERE bikeID = " + "'" + selectedBikeID.get() + "'"
   
    queryResults = bostonBikesDatabase.execute(sqlCommand)
   
    # Fetch one record from Query Results (should be only one result here anyway)    
    bikeRecord = queryResults.fetchone()
     
    # Put Bike Data into the Tkinter String Vars
    bikeID.set(bikeRecord[0])
    make.set(bikeRecord[1])
    model.set(bikeRecord[2])
    size.set(bikeRecord[3])
    bikeSupplierID.set(bikeRecord[4])
    buyingPrice.set("%-8.2f" %(bikeRecord[5]))
    sellingPrice.set("%-8.2f" %(bikeRecord[6]))
    stockLevel.set(bikeRecord[7])
    reorderLevel.set(bikeRecord[8])
    reorderAmount.set(bikeRecord[9])

    setUpBikeForm("Edit Bike")

    # Place the Update button
    buttonUpdateBike = Button( windowMain, text="Update Bike Details", command = updateBikeDetails)
    buttonUpdateBike.place( x=350, y=320, width=200, height=30 )


#----------------------------------------------------------------------------------------------------------

def updateBikeDetails():

    sqlCommand = ( "UPDATE bikeTable "
                   "SET bikeID = '"     + bikeID.get()         + "', "
                   "make = '"           + make.get()           + "', "
                   "model = '"          + model.get()          + "', "
                   "size = '"           + size.get()           + "', "
                   "bikeSupplierID = '" + bikeSupplierID.get() + "', "
                   "buyingPrice = '"    + buyingPrice.get()    + "', "
                   "sellingPrice = '"   + sellingPrice.get()   + "', "
                   "stockLevel = '"     + stockLevel.get()     + "', "
                   "reorderLevel = '"   + reorderLevel.get()   + "', "
                   "reorderAmount = '"  + reorderAmount.get()  + "'  "    
                   "WHERE bikeID = '"   + selectedBikeID.get() + "'  " )

    bostonBikesDatabase.execute(sqlCommand)
    bostonBikesDatabase.commit()

    labelMessage = Label( windowMain, font="11", bg="Light blue", text = "Bike Details Updated")
    labelMessage.place( x=345, y=360)

#----------------------------------------------------------------------------------------------------------

def addBike():

    # Empty the Tkinter String Variables
    bikeID.set("")
    make.set("")
    model.set("")
    size.set("")
    bikeSupplierID.set("")
    buyingPrice.set("")
    sellingPrice.set("")
    stockLevel.set("")
    reorderLevel.set("")
    reorderAmount.set("")

    setUpBikeForm("Add Bike")

    # Place the Save button
    buttonSaveBike = Button( windowMain, text="Save Bike Details", command = saveNewBike)
    buttonSaveBike.place( x=350, y=320, width=200, height=30 )

#----------------------------------------------------------------------------------------------------------

def saveNewBike():

    newBikeRecord = [bikeID.get(), make.get(), model.get(), size.get(),\
                     bikeSupplierID.get(), buyingPrice.get(), sellingPrice.get(),\
                     stockLevel.get(), reorderLevel.get(), reorderAmount.get()]

    bostonBikesDatabase.execute("INSERT INTO bikeTable VALUES(?,?,?,?,?,?,?,?,?,?)",newBikeRecord)
    bostonBikesDatabase.commit()
   
    labelMessage = Label( windowMain, font="11", bg="Light blue", text = "New Bike Saved")
    labelMessage.place( x=350, y=360)
   
#----------------------------------------------------------------------------------------------------------

def setUpBikeForm(heading):
   
    clearWindowMain()
   
    # Place a frame to surround heading,labels and user entries    
    frameEditbike = Frame(windowMain, bg="Light blue", highlightbackground="red", highlightthickness=2)
    frameEditbike.place( x=200, y=10, width = 580, height = 400)

    # Place the heading  
    labelHeading = Label(windowMain, text=heading, font=('Arial', 16), bg="Light blue")
    labelHeading.place( x=320, y=12, width=200, height=30)
   
    # Place the Labels
    Label( windowMain, bg="Light blue", text = "Bike ID:"          ).place( x=220, y=60)
    Label( windowMain, bg="Light blue", text = "Make:"             ).place( x=220, y=85)
    Label( windowMain, bg="Light blue", text = "Model:"            ).place( x=220, y=110)
    Label( windowMain, bg="Light blue", text = "Size:"             ).place( x=220, y=135)
    Label( windowMain, bg="Light blue", text = "Bike Supplier ID:" ).place( x=220, y=160)
    Label( windowMain, bg="Light blue", text = "Buy Price:"        ).place( x=220, y=185)
    Label( windowMain, bg="Light blue", text = "Sell Price:"       ).place( x=220, y=210)
    Label( windowMain, bg="Light blue", text = "Stock:"            ).place( x=220, y=235)
    Label( windowMain, bg="Light blue", text = "Reorder Level:"    ).place( x=220, y=260)
    Label( windowMain, bg="Light blue", text = "Reorder Amount:"   ).place( x=220, y=285)

    # Place the Data Format Labels - Information for the user  (Validation - None Added Yet)
    Label( windowMain, bg="Light blue", text = ": Format XX99"         ).place( x=570, y=60)
    Label( windowMain, bg="Light blue", text = ": Max 8 Characters"    ).place( x=570, y=85)
    Label( windowMain, bg="Light blue", text = ": Max 8 Characters"    ).place( x=570, y=110)
    Label( windowMain, bg="Light blue", text = ": XS,S,M,L,XL,XXL"     ).place( x=570, y=135)
    Label( windowMain, bg="Light blue", text = ": From Supplier Table" ).place( x=570, y=160)
    Label( windowMain, bg="Light blue", text = ": Max £9999.99"        ).place( x=570, y=185)
    Label( windowMain, bg="Light blue", text = ": Max £9999.99"        ).place( x=570, y=210)
    Label( windowMain, bg="Light blue", text = ": 0-100"               ).place( x=570, y=235)
    Label( windowMain, bg="Light blue", text = ": 0-100"               ).place( x=570, y=260)
    Label( windowMain, bg="Light blue", text = ": 0-100"               ).place( x=570, y=285)
 
    # Place the Entry boxes
    entry0 = Entry( windowMain, textvariable = bikeID,         width=30, bg="yellow").place( x=350, y=60)
    entry1 = Entry( windowMain, textvariable = make,           width=30, bg="white") .place( x=350, y=85)
    entry2 = Entry( windowMain, textvariable = model,          width=30, bg="white") .place( x=350, y=110)
    entry3 = Entry( windowMain, textvariable = size,           width=30, bg="white") .place( x=350, y=135)
    entry4 = Entry( windowMain, textvariable = bikeSupplierID, width=30, bg="white") .place( x=350, y=160)
    entry5 = Entry( windowMain, textvariable = buyingPrice,    width=30, bg="white") .place( x=350, y=185)
    entry6 = Entry( windowMain, textvariable = sellingPrice,   width=30, bg="white") .place( x=350, y=210)
    entry7 = Entry( windowMain, textvariable = stockLevel,     width=30, bg="white") .place( x=350, y=235)
    entry8 = Entry( windowMain, textvariable = reorderLevel,   width=30, bg="white") .place( x=350, y=260)
    entry9 = Entry( windowMain, textvariable = reorderAmount,  width=30, bg="white") .place( x=350, y=285)
 
#----------------------------------------------------------------------------------------------------------

def selectBikeToDelete():

    clearWindowMain()

    # Set Up the Edit bike Window - windowEditbike
    windowMain.title("BOSTON BIKES - DELETE A BIKE")
   
    # Place a Frame to surround heading,labels and user entries    
    frameEnterbikeID = Frame(windowMain, bg="Light blue", highlightbackground="blue", highlightthickness=2)
    frameEnterbikeID.place( x=50, y=10, width = 280, height = 280)
   
    # Place the Heading
    labelHeadingEnterbikeID = Label(windowMain, text="Select Bike ID", font=('Arial', 16), bg="Light blue")
    labelHeadingEnterbikeID.place( x=70, y=12, width=200, height=40)

    # Place the Label
    labelEnterbikeID = Label( windowMain, text = "Enter Bike ID:").place( x=70, y=60)

    # Place the Entry Box
    entrySelectedbikeID = Entry( windowMain, textvariable = bikeID, width=20, bg="yellow")
    entrySelectedbikeID.place( x=170, y=60)
    entrySelectedbikeID.delete(0, END)

    # Place the Button Delete Bike
    buttonDeleteBike = Button( windowMain, text = "Delete Bike", width=32, command = deleteBike)
    buttonDeleteBike.place( x=70, y=100)
   
#----------------------------------------------------------------------------------------------------------

def deleteBike():

    sqlCommand = "DELETE FROM bikeTable WHERE bikeID = '" + bikeID.get() + "'"

    bostonBikesDatabase.execute(sqlCommand)
    bostonBikesDatabase.commit()

    # Place a frame to surround the message    
    frameMessage = Frame(windowMain, bg="Light blue", highlightbackground="blue", highlightthickness=2)
    frameMessage.place( x=90, y=160, width = 200, height = 100)
   
    # Place the Message
    labelMessage = Label( windowMain, font="12", bg="Light blue", text = "Bike Deleted", justify = LEFT)
    labelMessage.place( x=92, y=162)

#==========================================================================================================

############ SUPPLIER TABLE ############
       
#==========================================================================================================

def listSuppliers():

    clearWindowMain()
   
    # Set Title
    windowMain.title("BOSTON BIKES - SUPPLIER LIST")

    # Place the Listbox to contain the Supplier List
    listSuppliers = Listbox(windowMain, width=80, height=20, font=("Consolas",14), selectmode="single")
    listSuppliers.place( x=30, y=15)
    listSuppliers.config( bg="Light blue", highlightbackground="blue", highlightthickness=2)

    ## This line calls the function - supplierClickedInList - when a supplier is clicked in the list
    listSuppliers.bind("<<ListboxSelect>>", editSupplier)

    # Add Column Headings to List Box
    listSuppliers.insert(END, " ")
    listSuppliers.insert(END, "              BOSTON BIKES - SUPPLIER LIST")
    listSuppliers.insert(END, "              ============================")
    listSuppliers.insert(END, " ")
    listSuppliers.insert(END, "  Click on a Supplier in the list to edit that Supplier.")
    listSuppliers.insert(END, " ")
    listSuppliers.insert(END, " ID       Supplier Name  Address        Phone        Email         ")
    listSuppliers.insert(END, " -------- -------------- -------------- ------------ --------------")
   
    sqlCommand = "SELECT * FROM supplierTable"

    for row in bostonBikesDatabase.execute(sqlCommand):
           
        listSuppliers.insert(END, " %-8s %-14s %-14s %-12s %-14s" %(row))

#----------------------------------------------------------------------------------------------------------

def editSupplier(event):
     
    listIndex = event.widget.curselection()[0] # Find index number of the item clicked in the list

    selectedSupplierID.set( event.widget.get(listIndex)[1:9] ) # Find clicked supplierID

    sqlCommand = "SELECT * from supplierTable WHERE supplierID = " + "'" + selectedSupplierID.get() + "'"
   
    queryResults = bostonBikesDatabase.execute(sqlCommand)
   
    # Fetch one record from Query Results (should be only one result here anyway)    
    supplierRecord = queryResults.fetchone()
     
    # Put Supplier Data into the Tkinter String Vars
    supplierID.set(supplierRecord[0])
    supplierName.set(supplierRecord[1])
    supplierAddress.set(supplierRecord[2])
    supplierPhone.set(supplierRecord[3])
    supplierEmail.set(supplierRecord[4])

    setUpSupplierForm("Edit Supplier")
   
    # Place the Update button
    buttonSaveSupplier = Button( windowMain, text="Update Supplier Details", command = updateSupplierDetails)
    buttonSaveSupplier.place( x=345, y=320, width=200, height=30 )

#----------------------------------------------------------------------------------------------------------

def updateSupplierDetails():

    sqlCommand = ( "UPDATE supplierTable "
                   "SET supplierID = '"   + supplierID.get() + "', "
                   "supplierName = '"     + supplierName.get()    + "', "
                   "supplierAddress = '"  + supplierAddress.get()    + "', "
                   "supplierPhone = '"    + supplierPhone.get()      + "', "
                   "supplierEmail = '"    + supplierEmail.get()      + "'  "
                   "WHERE supplierID = '" + selectedSupplierID.get() + "'  " )

    bostonBikesDatabase.execute(sqlCommand)
    bostonBikesDatabase.commit()

    labelMessage = Label( windowMain, font="11", bg="Light blue", text = "Supplier Updated")
    labelMessage.place( x=345, y=360)

#----------------------------------------------------------------------------------------------------------

def addSupplier():

    # EMPTY THE ENTRY BOXES
    supplierID.set("")
    supplierName.set("")
    supplierAddress.set("")
    supplierPhone.set("")
    supplierEmail.set("")

    setUpSupplierForm("Add Supplier")

    # Place the Save button
    buttonSaveSupplier = Button( windowMain, text="Save Supplier Details", command = saveNewSupplier)
    buttonSaveSupplier.place( x=350, y=320, width=200, height=30 )

#----------------------------------------------------------------------------------------------------------

def saveNewSupplier():

    newSupplierRecord = [supplierID.get(), supplierName.get(), supplierAddress.get(),\
                         supplierPhone.get(), supplierEmail.get()]

    bostonBikesDatabase.execute("INSERT INTO supplierTable VALUES(?,?,?,?,?)",newSupplierRecord)
    bostonBikesDatabase.commit()
   
    # Place the Message
    labelMessage = Label( windowMain, font="11", bg="Light blue", text = "New Supplier Saved")
    labelMessage.place( x=350, y=360)
   
#----------------------------------------------------------------------------------------------------------

def setUpSupplierForm(heading):

    clearWindowMain()
   
    # Place a frame to surround heading,labels and user entries    
    frameEditSupplier = Frame(windowMain, bg="Light blue", highlightbackground="red", highlightthickness=2)
    frameEditSupplier.place( x=200, y=10, width = 580, height = 400)

    # Place the heading  
    labelHeadingAddSupplier = Label(windowMain, text=heading, font=('Arial', 16), bg="Light blue")
    labelHeadingAddSupplier.place( x=320, y=12, width=200, height=30)

    # Place the Labels
    Label( windowMain, bg="Light blue", text = "Supplier ID:"   ).place( x=220, y=60)
    Label( windowMain, bg="Light blue", text = "Supplier Name:" ).place( x=220, y=85)
    Label( windowMain, bg="Light blue", text = "Address:"       ).place( x=220, y=110)
    Label( windowMain, bg="Light blue", text = "Phone:"         ).place( x=220, y=135)
    Label( windowMain, bg="Light blue", text = "Email"          ).place( x=220, y=160)

    # Place the Data Format Labels - Information for the user   (Validation - None Added Yet)
    Label( windowMain, bg="Light blue", text = ": Format XXXXXXXX"   ).place( x=570, y=60)
    Label( windowMain, bg="Light blue", text = ": Max 14 Characters" ).place( x=570, y=85)
    Label( windowMain, bg="Light blue", text = ": Max 14 Characters" ).place( x=570, y=110)
    Label( windowMain, bg="Light blue", text = ": 11 Digits"         ).place( x=570, y=135)
    Label( windowMain, bg="Light blue", text = ": Max 14 Characters" ).place( x=570, y=160)
 
    # Place the Entry boxes
    entry0 = Entry( windowMain, textvariable = supplierID,      width=30, bg="yellow").place( x=350, y=60)
    entry1 = Entry( windowMain, textvariable = supplierName,    width=30, bg="white") .place( x=350, y=85)
    entry2 = Entry( windowMain, textvariable = supplierAddress, width=30, bg="white") .place( x=350, y=110)
    entry3 = Entry( windowMain, textvariable = supplierPhone,   width=30, bg="white") .place( x=350, y=135)
    entry4 = Entry( windowMain, textvariable = supplierEmail,   width=30, bg="white") .place( x=350, y=160)


#----------------------------------------------------------------------------------------------------------

def selectSupplierToDelete():

    clearWindowMain()

    # Set Up the Edit supplier Window - windowEditsupplier
    windowMain.title("BOSTON BIKES - DELETE A SUPPLIER")
   
    # Place a Frame to surround heading,labels and user entries    
    frameSupplierID = Frame(windowMain, bg="Light blue", highlightbackground="blue", highlightthickness=2)
    frameSupplierID.place( x=50, y=10, width = 280, height = 280)
   
    # Place the Heading
    labelHeading = Label(windowMain, text="Select Supplier ID", font=('Arial', 16), bg="Light blue")
    labelHeading.place( x=70, y=12, width=200, height=40)

    # Place the Label
    labelEnterSupplierID = Label( windowMain, text = "Enter Supplier ID:").place( x=70, y=60)

    # Place the Entry Box
    entrySelectedSupplierID = Entry( windowMain, textvariable = supplierID, width=20, bg="yellow")
    entrySelectedSupplierID.place( x=170, y=60)
    entrySelectedSupplierID.delete(0, END)

    # Place the Button Delete Supplier
    buttonDeleteSupplier = Button( windowMain, text="Delete Supplier", width=32, command = deleteSupplier)
    buttonDeleteSupplier.place( x=70, y=100)
   
#---------------------------------------------------------------------------------------
 
def deleteSupplier():

    sqlCommand = "DELETE FROM supplierTable WHERE supplierID = '" + supplierID.get() + "'"

    bostonBikesDatabase.execute(sqlCommand)
    bostonBikesDatabase.commit()

    # Place a frame to surround the message    
    frameMessage = Frame(windowMain, bg="Light blue", highlightbackground="blue", highlightthickness=2)
    frameMessage.place( x=90, y=160, width = 200, height = 100)
   
    # Place the Message
    labelMessage = Label( windowMain, font="12", bg="Light blue", text = "Supplier Deleted", justify = LEFT)
    labelMessage.place( x=92, y=162)

#----------------------------------------------------------------------------------------------------------

#==========================================================================================================

############ CUSTOMER TABLE ############
       
#==========================================================================================================

def listCustomers():

    clearWindowMain()
   
    # Set Title
    windowMain.title("BOSTON BIKES - CUSTOMER LIST")

    # Place the Listbox to contain the Customer List
    listCustomers = Listbox(windowMain, width=80, height=20, font=("Consolas",14), selectmode="single")
    listCustomers.place( x=30, y=15)
    listCustomers.config( bg="Light blue", highlightbackground="blue", highlightthickness=2)

    ## This line calls the function - customerClickedInList - when a customer is clicked in the list
    listCustomers.bind("<<ListboxSelect>>", editCustomer)

    # Add Column Headings to List Box
    listCustomers.insert(END, " ")
    listCustomers.insert(END, "              BOSTON BIKES - CUSTOMER LIST")
    listCustomers.insert(END, "              ============================")
    listCustomers.insert(END, " ")
    listCustomers.insert(END, "  Click on a Customer in the list to edit that Customer.")
    listCustomers.insert(END, " ")
    listCustomers.insert(END, " ID   Customer Name  Address        Phone        Email         ")
    listCustomers.insert(END, " ---- -------------- -------------- ------------ --------------")
   
    sqlCommand = "SELECT * FROM customerTable"

    for row in bostonBikesDatabase.execute(sqlCommand):
           
        listCustomers.insert(END, " %-4s %-14s %-14s %-12s %-14s" %(row))

#----------------------------------------------------------------------------------------------------------

def editCustomer(event):
     
    listIndex = event.widget.curselection()[0] # Find index number of the item clicked in the list

    selectedCustomerID.set( event.widget.get(listIndex)[1:5] ) # Find clicked customerID

    sqlCommand = "SELECT * from customerTable WHERE customerID = " + "'" + selectedCustomerID.get() + "'"
   
    queryResults = bostonBikesDatabase.execute(sqlCommand)
   
    # Fetch one record from Query Results (should be only one result here anyway)    
    customerRecord = queryResults.fetchone()
     
    # Put Customer Data into the Tkinter String Vars
    customerID.set(customerRecord[0])
    customerName.set(customerRecord[1])
    customerAddress.set(customerRecord[2])
    customerPhone.set(customerRecord[3])
    customerEmail.set(customerRecord[4])

    setUpCustomerForm("Edit Customer")
   
    # Place the Update button
    buttonSaveCustomer = Button( windowMain, text="Update Customer Details", command = updateCustomerDetails)
    buttonSaveCustomer.place( x=320, y=320, width=200, height=30 )

#----------------------------------------------------------------------------------------------------------

def updateCustomerDetails():

    sqlCommand = ( "UPDATE customerTable "
                   "SET customerID = '"   + customerID.get()      + "', "
                   "customerName = '"     + customerName.get()    + "', "
                   "customerAddress = '"  + customerAddress.get() + "', "
                   "customerPhone = '"    + customerPhone.get()   + "', "
                   "customerEmail = '"    + customerEmail.get()   + "'  "
                   "WHERE customerID = '" + selectedCustomerID.get()      + "'  " )

    bostonBikesDatabase.execute(sqlCommand)
    bostonBikesDatabase.commit()

    labelMessage = Label( windowMain, font="11", bg="Light blue", text = "Customer Updated")
    labelMessage.place( x=345, y=360)

#----------------------------------------------------------------------------------------------------------

def addCustomer():

    # EMPTY THE ENTRY BOXES
    customerID.set("")
    customerName.set("")
    customerAddress.set("")
    customerPhone.set("")
    customerEmail.set("")

    setUpCustomerForm("Add Customer")

    # Place the Save button
    buttonSaveCustomer = Button( windowMain, text="Save Customer Details", command = saveNewCustomer)
    buttonSaveCustomer.place( x=320, y=320, width=200, height=30 )

#----------------------------------------------------------------------------------------------------------

def saveNewCustomer():

    newCustomerRecord = [customerID.get(), customerName.get(), customerAddress.get(),\
                         customerPhone.get(), customerEmail.get()]

    bostonBikesDatabase.execute("INSERT INTO customerTable VALUES(?,?,?,?,?)",newCustomerRecord)
    bostonBikesDatabase.commit()
   
    # Place the Message
    labelMessage = Label( windowMain, font="11", bg="Light blue", text = "New Customer Saved")
    labelMessage.place( x=320, y=360)
   
#----------------------------------------------------------------------------------------------------------

def setUpCustomerForm(heading):

    clearWindowMain()
   
    # Place a frame to surround heading,labels and user entries    
    frameEditCustomer = Frame(windowMain, bg="Light blue", highlightbackground="red", highlightthickness=2)
    frameEditCustomer.place( x=200, y=10, width = 580, height = 400)

    # Place the heading  
    labelHeadingAddCustomer = Label(windowMain, text=heading, font=('Arial', 16), bg="Light blue")
    labelHeadingAddCustomer.place( x=320, y=12, width=200, height=30)

    # Place the Labels
    Label( windowMain, bg="Light blue", text = "Customer ID:" ).place( x=220, y=60)
    Label( windowMain, bg="Light blue", text = "Name:"        ).place( x=220, y=85)
    Label( windowMain, bg="Light blue", text = "Address:"     ).place( x=220, y=110)
    Label( windowMain, bg="Light blue", text = "Phone:"       ).place( x=220, y=135)
    Label( windowMain, bg="Light blue", text = "Email"        ).place( x=220, y=160)

    # Place the Data Format Labels - Information for the user   (Validation - None Added Yet)
    Label( windowMain, bg="Light blue", text = ": Format 9999"       ).place( x=570, y=60)
    Label( windowMain, bg="Light blue", text = ": Max 14 Characters" ).place( x=570, y=85)
    Label( windowMain, bg="Light blue", text = ": Max 14 Characters" ).place( x=570, y=110)
    Label( windowMain, bg="Light blue", text = ": 11 Digits"         ).place( x=570, y=135)
    Label( windowMain, bg="Light blue", text = ": Max 14 Characters" ).place( x=570, y=160)

    # Place the Entry boxes
    entry0 = Entry( windowMain, textvariable = customerID,      width=30, bg="yellow").place( x=320, y=60)
    entry1 = Entry( windowMain, textvariable = customerName,    width=30, bg="white") .place( x=320, y=85)
    entry2 = Entry( windowMain, textvariable = customerAddress, width=30, bg="white") .place( x=320, y=110)
    entry3 = Entry( windowMain, textvariable = customerPhone,   width=30, bg="white") .place( x=320, y=135)
    entry4 = Entry( windowMain, textvariable = customerEmail,   width=30, bg="white") .place( x=320, y=160)

#----------------------------------------------------------------------------------------------------------

def selectCustomerToDelete():

    clearWindowMain()

    # Set Up the Edit customer Window - windowEditcustomer
    windowMain.title("BOSTON BIKES - DELETE A SUPPLIER")
   
    # Place a Frame to surround heading,labels and user entries    
    frameCustomerID = Frame(windowMain, bg="Light blue", highlightbackground="blue", highlightthickness=2)
    frameCustomerID.place( x=50, y=10, width = 280, height = 280)
   
    # Place the Heading
    labelHeadingCustomerID = Label(windowMain, text="Select Customer ID", font=('Arial', 16), bg="Light blue")
    labelHeadingCustomerID.place( x=70, y=12, width=200, height=40)

    # Place the Label
    labelEnterCustomerID = Label( windowMain, text = "Enter Customer ID:").place( x=70, y=60)

    # Place the Entry Box
    entrySelectedCustomerID = Entry( windowMain, textvariable = customerID, width=20, bg="yellow")
    entrySelectedCustomerID.place( x=180, y=60)
    entrySelectedCustomerID.delete(0, END)

    # Place the Button Delete Customer
    buttonDeleteCustomer = Button( windowMain, text="Delete Customer", width=32, command = deleteCustomer)
    buttonDeleteCustomer.place( x=70, y=100)
   
#----------------------------------------------------------------------------------------------------------

def deleteCustomer():

    sqlCommand = "DELETE FROM customerTable WHERE customerID = '" + customerID.get() + "'"

    bostonBikesDatabase.execute(sqlCommand)
    bostonBikesDatabase.commit()

    # Place a frame to surround the message    
    frameMessage = Frame(windowMain, bg="Light blue", highlightbackground="blue", highlightthickness=2)
    frameMessage.place( x=90, y=160, width = 200, height = 100)
   
    # Place the Message
    labelMessage = Label( windowMain, font="12", bg="Light blue", text = "Customer Deleted", justify = LEFT)
    labelMessage.place( x=92, y=162)

#==========================================================================================================

############ ORDER TABLE ############
       
#==========================================================================================================

def listOrders():

    clearWindowMain()
   
    # Set Title
    windowMain.title("BOSTON BIKES - ORDERS LIST")

    # Place the Listbox to contain the Order List
    listOrders = Listbox(windowMain, width=80, height=20, font=("Consolas",14), selectmode="single")
    listOrders.place( x=30, y=15)
    listOrders.config( bg="Light blue", highlightbackground="blue", highlightthickness=2)

    ## This line calls the function - orderClickedInList - when a order is clicked in the list
    listOrders.bind("<<ListboxSelect>>", editOrder)

    # Add Column Headings to List Box
    listOrders.insert(END, " ")
    listOrders.insert(END, "              BOSTON BIKES - ORDER LIST")
    listOrders.insert(END, "              =========================")
    listOrders.insert(END, " ")
    listOrders.insert(END, "  Click on a Order in the list to edit that Order.")
    listOrders.insert(END, " ")
    listOrders.insert(END, " Order ID Customer ID Order Date Paid")
    listOrders.insert(END, " -------- ----------- ---------- ----")
   
    sqlCommand = "SELECT * FROM orderTable"

    for row in bostonBikesDatabase.execute(sqlCommand):
           
        listOrders.insert(END, " %-8s %-11s %-12s %-6s" %(row))

#----------------------------------------------------------------------------------------------------------

def editOrder(event):
     
    listIndex = event.widget.curselection()[0] # Find index number of the item clicked in the list

    selectedOrderID.set( event.widget.get(listIndex)[1:5] ) # Find clicked orderID

    sqlCommand = "SELECT * from orderTable WHERE orderID = " + "'" + selectedOrderID.get() + "'"
   
    queryResults = bostonBikesDatabase.execute(sqlCommand)
   
    # Fetch one record from Query Results (should be only one result here anyway)    
    orderRecord = queryResults.fetchone()
     
    # Put Order Data into the Tkinter String Vars
    orderID.set(orderRecord[0])
    orderCustomerID.set(orderRecord[1])
    orderDate.set(orderRecord[2])
    paid.set(orderRecord[3])

    setUpOrderForm("Edit Order")
   
    # Place the Update button
    buttonSaveOrder = Button( windowMain, text="Update Order Details", command = updateOrderDetails)
    buttonSaveOrder.place( x=320, y=320, width=200, height=30 )

#----------------------------------------------------------------------------------------------------------

def updateOrderDetails():

    sqlCommand = ( "UPDATE orderTable "
                   "SET orderID = '"     + orderID.get()         + "', "
                   "orderCustomerID = '" + orderCustomerID.get() + "', "
                   "orderDate = '"       + orderDate.get()       + "', "
                   "paid = '"            + paid.get()            + "'  "
                   "WHERE orderID = '"   + selectedOrderID.get() + "'  " )

    bostonBikesDatabase.execute(sqlCommand)
    bostonBikesDatabase.commit()

    labelMessage = Label( windowMain, font="11", bg="Light blue", text = "Order Updated")
    labelMessage.place( x=345, y=360)

#----------------------------------------------------------------------------------------------------------

def addOrder():

    # EMPTY THE ENTRY BOXES
    orderID.set("")
    orderCustomerID.set("")
    orderDate.set("")
    paid.set("")

    setUpOrderForm("Add Order")

    # Place the Save button
    buttonSaveOrder = Button( windowMain, text="Save Order Details", command = saveNewOrder)
    buttonSaveOrder.place( x=320, y=320, width=200, height=30 )

#----------------------------------------------------------------------------------------------------------

def saveNewOrder():

    newOrderRecord = [orderID.get(), orderCustomerID.get(), orderDate.get(), paid.get()]

    bostonBikesDatabase.execute("INSERT INTO orderTable VALUES(?,?,?,?)",newOrderRecord)
    bostonBikesDatabase.commit()
   
    # Place the Message
    labelMessage = Label( windowMain, font="11", bg="Light blue", text = "New Order Saved")
    labelMessage.place( x=320, y=360)
   
#----------------------------------------------------------------------------------------------------------

def setUpOrderForm(heading):

    clearWindowMain()
   
    # Place a frame to surround heading,labels and user entries    
    frameEditOrder = Frame(windowMain, bg="Light blue", highlightbackground="red", highlightthickness=2)
    frameEditOrder.place( x=200, y=10, width = 580, height = 400)

    # Place the heading  
    labelHeadingAddOrder = Label(windowMain, text=heading, font=('Arial', 16), bg="Light blue")
    labelHeadingAddOrder.place( x=320, y=12, width=200, height=30)

    # Place the Labels
    Label( windowMain, bg="Light blue", text = "Order ID:"   ).place( x=220, y=60)
    Label( windowMain, bg="Light blue", text = "CustomerID:" ).place( x=220, y=85)
    Label( windowMain, bg="Light blue", text = "OrderDate:"  ).place( x=220, y=110)
    Label( windowMain, bg="Light blue", text = "Paid"        ).place( x=220, y=135)

    # Place the Data Format Labels - Information for the user
    Label( windowMain, bg="Light blue", text = ": Format X999"           ).place( x=570, y=60)
    Label( windowMain, bg="Light blue", text = ": From Customer Table"   ).place( x=570, y=85)
    Label( windowMain, bg="Light blue", text = ": Valid Date dd/mm/yyyy" ).place( x=570, y=110)
    Label( windowMain, bg="Light blue", text = ": Y or N"                ).place( x=570, y=135)
 
    # Place the Entry boxes
    entry0 = Entry( windowMain, textvariable = orderID,         width=30, bg="yellow").place( x=320, y=60)
    entry1 = Entry( windowMain, textvariable = orderCustomerID, width=30, bg="white") .place( x=320, y=85)
    entry2 = Entry( windowMain, textvariable = orderDate,       width=30, bg="white") .place( x=320, y=110)
    entry4 = Entry( windowMain, textvariable = paid,            width=30, bg="white") .place( x=320, y=135)

#----------------------------------------------------------------------------------------------------------

def selectOrderToDelete():

    clearWindowMain()

    # Set Up the Edit order Window - windowEditorder
    windowMain.title("BOSTON BIKES - DELETE A SUPPLIER")
   
    # Place a Frame to surround heading,labels and user entries    
    frameEnterOrderID = Frame(windowMain, bg="Light blue", highlightbackground="blue", highlightthickness=2)
    frameEnterOrderID.place( x=50, y=10, width = 280, height = 280)
   
    # Place the Heading
    labelHeadingEnterOrderID = Label(windowMain, text="Select Order ID", font=('Arial', 16), bg="Light blue")
    labelHeadingEnterOrderID.place( x=70, y=12, width=200, height=40)

    # Place the Label
    labelEnterOrderID = Label( windowMain, text = "Enter Order ID:").place( x=70, y=60)

    # Place the Entry Box
    entrySelectedOrderID = Entry( windowMain, textvariable = orderID, width=20, bg="yellow")
    entrySelectedOrderID.place( x=170, y=60)
    entrySelectedOrderID.delete(0, END)

    # Place the Button Delete Order
    buttonDeleteOrder = Button( windowMain, text="Delete Order", width=32, command = deleteOrder)
    buttonDeleteOrder.place( x=70, y=100)
   
#----------------------------------------------------------------------------------------------------------

def deleteOrder():

    sqlCommand = "DELETE FROM orderTable WHERE orderID = '" + orderID.get() + "'"

    bostonBikesDatabase.execute(sqlCommand)
    bostonBikesDatabase.commit()

    # Place a frame to surround the message    
    frameMessage = Frame(windowMain, bg="Light blue", highlightbackground="blue", highlightthickness=2)
    frameMessage.place( x=90, y=160, width = 200, height = 100)
   
    # Place the Message
    labelMessage = Label( windowMain, font="12", bg="Light blue", text = "Order Deleted", justify = LEFT)
    labelMessage.place( x=92, y=162)


#==========================================================================================================

############ ORDER ITEMS TABLE ############
       
#==========================================================================================================

def listOrderItems():

    clearWindowMain()
   
    # Set Title
    windowMain.title("BOSTON BIKES - ORDER ITEMS LIST")

    # Place the Listbox to contain the Order Items List
    listOrderItems = Listbox(windowMain, width=80, height=20, font=("Consolas",14), selectmode="single")
    listOrderItems.place( x=30, y=15)
    listOrderItems.config( bg="Light blue", highlightbackground="blue", highlightthickness=2)

    ## This line calls the function - editOrderItem - when a order item is clicked in the list
    listOrderItems.bind("<<ListboxSelect>>", editOrderItem)

    # Add Column Headings to List Box
    listOrderItems.insert(END, " ")
    listOrderItems.insert(END, "              BOSTON BIKES - ORDER ITEMS LIST")
    listOrderItems.insert(END, "              ===============================")
    listOrderItems.insert(END, " ")
    listOrderItems.insert(END, "  Click on an Order Item in the list to edit that Order Item.")
    listOrderItems.insert(END, " ")
    listOrderItems.insert(END, " Order ID Bike ID Quantity")
    listOrderItems.insert(END, " -------- ------- --------")
   
    sqlCommand = "SELECT * FROM orderItemsTable ORDER BY orderItemsOrderID, orderItemsBikeID"

    for row in bostonBikesDatabase.execute(sqlCommand):
           
        listOrderItems.insert(END, " %-9s %-10s %-5d" %(row))

#----------------------------------------------------------------------------------------------------------

def editOrderItem(event):
     
    listIndex = event.widget.curselection()[0] # Find index number of the item clicked in the list

    selectedOrderID.set( event.widget.get(listIndex)[1:5] ) # Find clicked orderItemsOrderID
    selectedBikeID.set( event.widget.get(listIndex)[11:15]) # Find clicked orderItemsBikeID

    sqlCommand = ( "SELECT * from orderItemsTable "
                   "WHERE orderItemsOrderID = " + "'" + selectedOrderID.get() + "' "
                   "AND orderItemsBikeID = " + "'" + selectedBikeID.get() + "'" )
    
    queryResults = bostonBikesDatabase.execute(sqlCommand)
   
    # Fetch one record from Query Results (should be only one result here anyway)    
    orderItemRecord = queryResults.fetchone()
     
    # Put Order Items Data into the Tkinter String Vars
    orderItemsOrderID.set(orderItemRecord[0])
    orderItemsBikeID.set(orderItemRecord[1])
    quantity.set(orderItemRecord[2])

    setUpOrderItemsForm("Edit Order Items")
   
    # Place the Update button
    buttonSaveOrderItems = Button( windowMain, text="Update Order Item Details", command = updateOrderItemDetails)
    buttonSaveOrderItems.place( x=320, y=320, width=200, height=30 )

#----------------------------------------------------------------------------------------------------------

def updateOrderItemDetails():

    sqlCommand = ( "UPDATE  orderItemsTable "
                   "SET     orderItemsOrderID = '" + orderItemsOrderID.get() + "', "
                   "        orderItemsBikeID  = '" + orderItemsBikeID.get()  + "', "
                   "        quantity          = '" + quantity.get()          + "'  "
                   "WHERE   orderItemsOrderID = '" + selectedOrderID.get() + "'  "
                   "AND     orderItemsBikeID  = '" + selectedBikeID.get()  + "'" )

    bostonBikesDatabase.execute(sqlCommand)
    bostonBikesDatabase.commit()

    labelMessage = Label( windowMain, font="11", bg="Light blue", text = "Order Items Updated")
    labelMessage.place( x=335, y=360)

#----------------------------------------------------------------------------------------------------------

def addOrderItem():

    # EMPTY THE ENTRY BOXES
    orderItemsOrderID.set("")
    orderItemsBikeID.set("")
    quantity.set("")

    setUpOrderItemsForm("Add Order Item")

    # Place the Save button
    buttonSaveOrderItem = Button( windowMain, text="Save Order Item Details", command = saveNewOrderItem)
    buttonSaveOrderItem.place( x=320, y=320, width=200, height=30 )

#----------------------------------------------------------------------------------------------------------

def saveNewOrderItem():

    newOrderItemsRecord = [orderItemsOrderID.get(), orderItemsBikeID.get(), quantity.get()]

    bostonBikesDatabase.execute("INSERT INTO orderItemsTable VALUES(?,?,?)", newOrderItemsRecord)
    bostonBikesDatabase.commit()
   
    # Place the Message
    labelMessage = Label( windowMain, font="11", bg="Light blue", text = "New Order Item Saved")
    labelMessage.place( x=320, y=360)
   
#----------------------------------------------------------------------------------------------------------

def setUpOrderItemsForm(heading):

    clearWindowMain()
   
    # Place a frame to surround heading,labels and user entries    
    frameEditOrderItem = Frame(windowMain, bg="Light blue", highlightbackground="red", highlightthickness=2)
    frameEditOrderItem.place( x=200, y=10, width = 580, height = 400)

    # Place the heading  
    labelHeadingAddOrderItem = Label(windowMain, text=heading, font=('Arial', 16), bg="Light blue")
    labelHeadingAddOrderItem.place( x=320, y=12, width=200, height=30)

    # Place the Labels
    Label( windowMain, bg="Light blue", text = "Order ID:" ).place( x=220, y=60)
    Label( windowMain, bg="Light blue", text = "Bike ID:"  ).place( x=220, y=85)
    Label( windowMain, bg="Light blue", text = "Quantity:" ).place( x=220, y=110)

    # Place the Data Format Labels - Information for the user    (Validation - None Added Yet)
    Label( windowMain, bg="Light blue", text = ": From Order Table" ).place( x=570, y=60)
    Label( windowMain, bg="Light blue", text = ": From Bike Table"  ).place( x=570, y=85)
    Label( windowMain, bg="Light blue", text = ": 1 - 100"          ).place( x=570, y=110)
   
    # Place the Entry boxes
    entry0 = Entry( windowMain, textvariable = orderItemsOrderID, width=30, bg="yellow") .place( x=320, y=60)
    entry1 = Entry( windowMain, textvariable = orderItemsBikeID,  width=30, bg="yellow") .place( x=320, y=85)
    entry2 = Entry( windowMain, textvariable = quantity,          width=30, bg="white")  .place( x=320, y=110)

#----------------------------------------------------------------------------------------------------------

def selectOrderItemToDelete():

    clearWindowMain()

    # Set Up the Edit order item Window - windowEditorder item
    windowMain.title("BOSTON BIKES - DELETE A ORDER ITEM")
   
    # Place a Frame to surround heading,labels and user entries    
    frameEnterOrderitem = Frame(windowMain, bg="Light blue", highlightbackground="blue", highlightthickness=2)
    frameEnterOrderitem.place( x=50, y=10, width = 380, height = 280)
   
    # Place the Heading
    labelHeading = Label(windowMain, text="Select Order Item to Delete", font=('Arial', 16), bg="Light blue")
    labelHeading.place( x=70, y=12, width=300, height=40)

    # Place the Labels
    labelEnterOrderItemOrderID = Label( windowMain, text = "Enter Order Item Order ID:").place( x=70, y=60)
    labelEnterOrderItemBikeID = Label( windowMain, text = "Enter Order Item Bike ID :").place( x=70, y=85)
   
    # Place the Entry Box
    orderItemsOrderID.set("")
    orderItemsBikeID.set("")
    entrySelectedOrderItemOrderID = Entry( windowMain, textvariable = orderItemsOrderID, width=20, bg="yellow")
    entrySelectedOrderItemOrderID.place( x=280, y=60)
    entrySelectedOrderItemBikeID = Entry( windowMain, textvariable = orderItemsBikeID, width=20, bg="yellow")
    entrySelectedOrderItemBikeID.place( x=280, y=85)

    # Place the Button Delete Order Items
    buttonDeleteOrderItem = Button( windowMain, text="Delete Order Item", width=32, command = deleteOrderItem)
    buttonDeleteOrderItem.place( x=100, y=130)
   
#----------------------------------------------------------------------------------------------------------

def deleteOrderItem():

    sqlCommand = ( "DELETE FROM orderItemsTable "
                   "WHERE orderItemsOrderID = '" + orderItemsOrderID.get() + "'"
                   "AND   orderItemsBikeID  = '" + orderItemsBikeID.get()  + "'" )

    bostonBikesDatabase.execute(sqlCommand)
    bostonBikesDatabase.commit()

    # Place a frame to surround the message    
    frameMessage = Frame(windowMain, bg="Light blue", highlightbackground="blue", highlightthickness=2)
    frameMessage.place( x=90, y=160, width = 200, height = 100)
   
    # Place the Message
    labelMessage = Label(windowMain,font="12",bg="Light blue",text = "Order Item Deleted",justify = LEFT)
    labelMessage.place( x=92, y=162)
    
#==========================================================================================================

############ REPORTS ############
       
#==========================================================================================================

#----------------------------------------------------------------------------------------------------------
########  REORDER NOTES  #######
# This report lets the user select one Supplier from the combo box (drop down list).  Then it goes through
# 
#----------------------------------------------------------------------------------------------------------

def selectSupplierForOrderNotes():     # SELECTION HERE USING COMBO BOX WITH ORDER NUMBERS
   
    clearWindowMain()
    
    windowMain.title("BOSTON BIKES - ORDER BIKES FROM SUPPLIER")

    labelSupplierID = Label(windowMain, text="Select Supplier ID for Order Notes : ", font=('Arial', 10))
    labelSupplierID.place( x=120, y=8, width=220, height=40)

    sqlCommand = "SELECT supplierID from supplierTable"

    comboBoxValues = []
    
    for row in bostonBikesDatabase.execute(sqlCommand):
        comboBoxValues += row
     
    comboBoxSupplierIDs = ttk.Combobox(state = "readonly",textvariable=supplierID,values = comboBoxValues )
    comboBoxSupplierIDs.place(x=360, y=17)

    comboBoxSupplierIDs.bind("<<ComboboxSelected>>", displayOrderNotes)
    
#----------------------------------------------------------------------------------------------------------

def displayOrderNotes(event):
   
    # Set Up the Edit Car Window - windowEditCar
    windowMain.title("BOSTON Bikes - ORDER NOTES")

    # Place the Listbox to contain the Sales List
    listReport = Listbox(windowMain, width=71, height=25, font=("Consolas",10), selectmode="single")
    listReport.place( x=100, y=55)
    listReport.config( bg="Light blue", highlightbackground="blue", highlightthickness=2)
 
    sqlCommandSuppliers = ( "SELECT supplierID, supplierName, supplierAddress, supplierPhone, supplierEmail "
                            "FROM supplierTable "
                            "WHERE supplierID = '" + supplierID.get() + "' "
                            "ORDER BY supplierID")

    for supplierRow in bostonBikesDatabase.execute(sqlCommandSuppliers):
        
        listReport.insert( END, "  ")
        listReport.insert( END, " =====================================================================")
        listReport.insert( END, "             BOSTON BIKES - FOR ALL YOUR CYCLE NEEDS                 ")
        listReport.insert( END, " ---------------------------------------------------------------------")
        listReport.insert( END, "    Boston Bikes, Spokane, South Wales.     Tel 018871 8181181       ")
        listReport.insert( END, "    enquiries@BostonBikes.com         VAT Reg Number 120987245       ")
        listReport.insert( END, " ---------------------------------------------------------------------")
        listReport.insert( END, "               Order Note for Supplier ID :" + supplierRow[0]   )
        listReport.insert( END, " ---------------------------------------------------------------------")
        listReport.insert( END, "               Supplier Name     : " + supplierRow[1]  )
        listReport.insert( END, "               Supplier Address  : " + supplierRow[2]  )        
        listReport.insert( END, "               Supplier Phone    : " + supplierRow[3]  )
        listReport.insert( END, "               Supplier Email    : " + supplierRow[4]  )
        listReport.insert( END, " ---------------------------------------------------------------------")
        listReport.insert( END, " Please send the following bikes :")
        listReport.insert( END, " ---------------------------------------------------------------------")
        listReport.insert( END, " Bike Bike     Bike     Bike  Bike      ReOrder  Sub")
        listReport.insert( END, " ID   Make     Model    Size  Price     Amount   Total")
        listReport.insert( END, " ---- -------- -------- ----  --------- -------  ---------")  

        sqlCommandBikes = ( "SELECT bikeID, make, model, size, bikeSupplierID, buyingPrice, "
                            "stockLevel, reorderLevel, reorderAmount "
                            "FROM bikeTable "
                            "WHERE bikeSupplierID = '" + supplierRow[0] + "' AND stockLevel <= reorderLevel "
                            "ORDER BY bikeID" )

        grandTotal = float(0)

        for bikeRow in bostonBikesDatabase.execute(sqlCommandBikes):

            bikeLine = ( " %-5s"     %(bikeRow[0]) +               # Bike ID
                         "%-9s"      %(bikeRow[1]) +               # Make
                         "%-10s"     %(bikeRow[2]) +               # Model
                         "%-5s"      %(bikeRow[3]) +               # Size
                         "£%8.2f"    %(bikeRow[5]) +               # Buying Price
                         "%4d      " %(bikeRow[8]) +               # Reorder Amount
                         "£%8.2f"    %(bikeRow[5] * bikeRow[8]) )  # Sub Total

            listReport.insert( END, bikeLine)

            grandTotal += (bikeRow[5]) * (bikeRow[8])

        if grandTotal > 0:

            listReport.insert( END, " ---------------------------------------------------------------------")
            listReport.insert( END, " "*30 + "      Grand Total  £" + "%8.2f" %(grandTotal))              
            listReport.insert( END, " =====================================================================")

        else:

            listReport.insert( END, "    ***  NO BIKES TO ORDER CURRENTLY  ***                            ")            
            listReport.insert( END, " =====================================================================")

#----------------------------------------------------------------------------------------------------------
########  RECEIPT  ####### 
#----------------------------------------------------------------------------------------------------------

def selectOrderForReceipt():     # SELECTION HERE USING COMBO BOX WITH ORDER NUMBERS
   
    clearWindowMain()
    
    windowMain.title("BOSTON BIKES - ORDER RECEIPT")

    labelEnterOrderID = Label(windowMain, text="Select Order ID for Receipt : ", font=('Arial', 10))
    labelEnterOrderID.place( x=110, y=8, width=200, height=40)

    sqlCommand = "SELECT orderID from orderTable"

    comboBoxValues = []
    
    for row in bostonBikesDatabase.execute(sqlCommand):
        comboBoxValues += row
     
    comboBoxOrderIDs = ttk.Combobox( state = "readonly", textvariable = orderID, values = comboBoxValues )
    comboBoxOrderIDs.place(x=300, y=17)

    comboBoxOrderIDs.bind("<<ComboboxSelected>>", displayReceipt)

#----------------------------------------------------------------------------------------------------------
 
def displayReceipt(event):

    windowMain.title("BOSTON BIKES - RECEIPT")

    # Place the Listbox to contain the Receipt
    listReport = Listbox(windowMain, width=71, height=24, font=("Consolas",10))
    listReport.place( x=100, y=55)
    listReport.config( bg="Light blue", highlightbackground="blue", highlightthickness=2)

    sqlCommand = ( "SELECT orderID, orderCustomerID, orderDate, paid, "
                   "       customerID, customerName, customerAddress, customerPhone, customerEmail "              
                   "FROM   orderTable, customerTable "
                   "WHERE  orderID = '" + orderID.get() + "' "
                   "AND    orderCustomerID = customerID "
                   "ORDER  BY orderID" )

    currentDate = date.today().strftime('%d-%m-%Y')

    for row in bostonBikesDatabase.execute(sqlCommand):

        listReport.insert( END, " ")
        listReport.insert( END, " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        listReport.insert( END, "          BOSTON BIKES - RECEIPT - THANK YOU FOR YOUR ORDER           ")
        listReport.insert( END, " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        listReport.insert( END, " Boston Bikes, BOSTON Island, South Wales.    Tel 018871 8181181      ")
        listReport.insert( END, " E-Mail  enquiries@BostonBikes.com         VAT Reg Number 120987245   ")
        listReport.insert( END, " ---------------------------------------------------------------------")
        listReport.insert( END, "   Receipt for Order ID : " + row[0] + "        Date : " + currentDate )
        listReport.insert( END, " ---------------------------------------------------------------------")
        listReport.insert( END, " ORDER ID    : " + "%-14s"  %(row[0]) + " CUSTOMER ID : "     + row[4] )
        listReport.insert( END, " Order Date  : " + "%-14s"  %(row[2]) + " Name        : "     + row[5] )        
        listReport.insert( END, " Paid        : " + "%-14s"  %(row[3]) + " Address     : "     + row[6] )
        listReport.insert( END, " "*29                                 + " Phone       : "     + row[7] )
        listReport.insert( END, " "*29                                 + " Email       : "     + row[8] )
        listReport.insert( END, " ---------------------------------------------------------------------")
        listReport.insert( END, " Bike Bike     Bike     Bike  Bike      Bike     Sub")
        listReport.insert( END, " ID   Make     Model    Size  Price     Quantity Total")
        listReport.insert( END, " ---- -------- -------- ----  --------- -------  ---------")  

    sqlCommandBikes = ( "SELECT orderItemsOrderID, orderItemsBikeID, quantity, "
                        "       bikeID, make, model, size, sellingPrice "
                        "FROM   orderItemsTable, bikeTable "
                        "WHERE  orderItemsOrderID = '" + orderID.get() + "' "
                        "AND    orderItemsBikeID = bikeID " )

    grandTotal = float(0)

    for bikeRow in bostonBikesDatabase.execute(sqlCommandBikes):

        bikeLine = ( " %-5s"     %(bikeRow[3]) +               # Bike ID
                     "%-9s"      %(bikeRow[4]) +               # Make
                     "%-10s"     %(bikeRow[5]) +               # Model
                     "%-5s"      %(bikeRow[6]) +               # Size
                     "£%8.2f"    %(bikeRow[7]) +               # Selling Price
                     "%4d      " %(bikeRow[2]) +               # Quantity
                     "£%8.2f"    %(bikeRow[7] * bikeRow[2]) )  # Sub Total

        listReport.insert( END, bikeLine)

        grandTotal += (bikeRow[7]) * (bikeRow[2])

    if grandTotal > 0:
        listReport.insert( END, " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        listReport.insert( END, " "*30 + "      Grand Total  £" + "%8.2f" %(grandTotal))              
        listReport.insert( END, " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    else:
        listReport.insert( END, "         ***  NO BIKES ON THE ORDER   ***                            ")            
        listReport.insert( END, "=====================================================================")


#----------------------------------------------------------------------------------------------------------
########  PROFIT REPORT  ####### 
#----------------------------------------------------------------------------------------------------------

def selectYearForProfitReport():     # SELECTION HERE USING COMBO BOX WITH YEARS
   
    clearWindowMain()
    
    windowMain.title("BOSTON BIKES - ORDER RECEIPT")
 
    labelEnterOrderID = Label(windowMain, text="Select Year for Profit Report : ", font=('Arial', 10))
    labelEnterOrderID.place( x=110, y=8, width=200, height=40)
    
    currentYear = int(date.today().strftime('%Y'))

    comboBoxValues = []

    for i in range(currentYear - 5, currentYear + 6):
        comboBoxValues.append(i)
    
    comboBoxYears = ttk.Combobox( state = "readonly", textvariable = yearForProfitReport, values = comboBoxValues )
    comboBoxYears.place(x=300, y=17)

    comboBoxYears.bind("<<ComboboxSelected>>", profitReport)

#----------------------------------------------------------------------------------------------------------
    
def profitReport(event):
    
    windowMain.title("BOSTON BIKES - PROFIT REPORT")

    # Place the Listbox to contain the Receipt
    listReport = Listbox(windowMain, width=71, height=26, font=("Consolas",10))
    listReport.place( x=100, y=55)
    listReport.config( bg="Light blue", highlightbackground="blue", highlightthickness=2)

    currentDate = date.today().strftime('%d-%m-%Y')

    listReport.insert( END, " ")
    listReport.insert( END, " =====================================================================")
    listReport.insert( END, "         BOSTON BIKES - PROFIT REPORT FOR " + yearForProfitReport.get())
    listReport.insert( END, " =====================================================================")
    listReport.insert( END, "         Created on  : " + currentDate )
    listReport.insert( END, " ---------------------------------------------------------------------")

    currentDate = date.today().strftime('%d-%m-%Y')
    
    sqlCommand = ( "SELECT orderID, orderDate, paid, "
                   "       orderItemsOrderID, orderItemsBikeID, quantity, "
                   "       bikeID, buyingPrice, sellingPrice, "
                   "       ((sellingPrice - buyingPrice) * quantity) " # ORDER PROFIT CALCULATED FIELD
                   "FROM   orderTable, orderItemsTable, bikeTable "
                   "WHERE  orderID = orderItemsOrderID "
                   "AND    bikeID = orderItemsBikeID "
                   "AND    SUBSTR(orderDate,7,10) = '" + yearForProfitReport.get() + "' " )                

    queryResults = bostonBikesDatabase.execute(sqlCommand)

    allQueryResults = queryResults.fetchall()

    totalBikesSold = int(0)
    totalOutGoings = float(0)
    totalIncome = float(0)
    unPaidIncome = float(0)
    unPaidProfit = float(0)
    totalProfit = float(0)
   
    listReport.insert( END, " Order Order      Paid Quantity Bike  Buying     Selling    Order Item ")
    listReport.insert( END, " ID    Date                     ID    Price      Price      Profit     ")
    listReport.insert( END, " ----- ---------- ---- -------- ----  ---------- ---------- ---------- ")
    
    for row in allQueryResults:

        orderItemLine = ( " %-6s"    %(row[0])  +  # Order ID
                          "%-12s"    %(row[1])  +  # Order Date
                          "%-8s"     %(row[2])  +  # Paid Y or N
                          "%-5s"     %(row[5])  +  # Quantity
                          "%-5s"     %(row[6])  +  # Bike Id
                          " £%8.2f"  %(row[7])  +  # Buying Price
                          "  £%8.2f" %(row[8])  +  # Selling Price
                          "  £%8.2f" %(row[9])  )  # Order Profit

        listReport.insert( END, orderItemLine)

        totalOutGoings += (row[7] * row[5])
        totalBikesSold += int(row[5])

        if row[2] == "Y":                      # Order has been Paid
            totalProfit += row[9]
            totalIncome += (row[8] * row[5])
        else:                                  # Order Not Paid
            unPaidProfit += row[9]
            unPaidIncome += (row[8] * row[5])
            
    listReport.insert( END, " =====================================================================")             
    listReport.insert( END, " Total Bikes Sold        " + "  %8d"  %(totalBikesSold))
    listReport.insert( END, " Total Out Goings        " + "£%9.2f" %(totalOutGoings))    
    listReport.insert( END, " Total Actual Income     " + "£%9.2f" %(totalIncome))
    listReport.insert( END, " ---------------------------------------------------------------------")
    listReport.insert( END, " TOTAL ACTUAL PROFIT     " + "£%9.2f" %(totalProfit))
    listReport.insert( END, " ---------------------------------------------------------------------")
    listReport.insert( END, " Missing Unpaid Income   " + "£%9.2f" %(unPaidIncome))
    listReport.insert( END, " Missing Unpaid Profit   " + "£%9.2f" %(unPaidProfit))
    listReport.insert( END, " =====================================================================")

#----------------------------------------------------------------------------------------------------------
########  BIKES IN STOCK REPORT  ####### 
#----------------------------------------------------------------------------------------------------------

def bikesInStock():
       
    clearWindowMain()
    
    windowMain.title("BOSTON BIKES - BIKES IN STOCK")
    
    listReport = Listbox(windowMain, width=71, height=26, font=("Consolas",10))
    listReport.place( x=100, y=15)
    listReport.config( bg="Light blue", highlightbackground="blue", highlightthickness=2)

    currentDate = date.today().strftime('%d-%m-%Y')

    listReport.insert( END, " ")
    listReport.insert( END, " =====================================================================")
    listReport.insert( END, "    BOSTON BIKES - STOCK REPORT WITH TOTAL                       ")
    listReport.insert( END, " =====================================================================")
    listReport.insert( END, "         Created on  : " + currentDate )
    listReport.insert( END, " ---------------------------------------------------------------------")
    listReport.insert( END, " Bike Bike     Bike     Bike   Stock ")
    listReport.insert( END, " ID   Make     Model    Size   Level")
    listReport.insert( END, " ---- -------- -------- ----   --------")
    
    sqlCommand = ( "SELECT bikeID, make, model, size, stockLevel "
                   "FROM   bikeTable " )

    queryResults = bostonBikesDatabase.execute(sqlCommand)

    allQueryResults = queryResults.fetchall()
    
    for row in allQueryResults:

        listReport.insert( END, " %-4s %-8s %-8s  %-4s %4d" %(row))

    listReport.insert( END, " ---------------------------------------------------------------------")
        
    sqlCommand = ( "SELECT SUM(stockLevel) FROM bikeTable" )   # Make a Total of all stock

    queryResults = bostonBikesDatabase.execute(sqlCommand)

    totalStock = queryResults.fetchone()[0]

    listReport.insert( END, " Total Bikes in stock :         " + str(totalStock) )
    listReport.insert( END, " =====================================================================")

#=========================================================================================================

#### CALL THE MAIN FUNCTION ####

main()

#=========================================================================================================
