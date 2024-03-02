# importing the required modules for project
from tkinter import *  # importing all the modules and classes from tkinter
from tkinter import ttk as ttk  # importing the ttk module from tkinter
from tkinter import messagebox as mb  # importing the messagebox module from tkinter
import datetime  # importing the datetime module
import sqlite3  # importing the sqlite3 module
from tkcalendar import DateEntry  # importing the DateEntry class from the tkcalendar module


# --------------------- defining functions ---------------------

# function to list all the expenses
def listAllExpenses():
    '''''This function will retrieve the data from the database and insert it to the tkinter data table'''

    # using some global variables
    global dbconnector, data_table
    # clearing the table
    data_table.delete(*data_table.get_children())
    # executing the SQL SELECT command to retrieve the data from the database table
    all_data = dbconnector.execute('SELECT * FROM ExpenseTracker')

    # listing the data from the table
    data = all_data.fetchall()

    # inserting the values iteratively in the tkinter data table
    for val in data:
        data_table.insert('', END, values=val)

    # function to view an expense information


def viewExpenseInfo():
    '''''This function will display the expense information in the data frame'''

    # using some global variables
    global data_table
    global dateField, payee, description, amount, modeOfPayment

    # return a message box displaying error if no row is selected from the table
    if not data_table.selection():
        mb.showerror('No expense selected', 'Please select an expense from the table to view its details')

        # collecting the data from the selected row in dictionary format
    currentSelectedExpense = data_table.item(data_table.focus())

    # defining a variable to store the values from the collected data in list
    val = currentSelectedExpense['values']

    # retrieving the date of expenditure from the list
    expenditureDate = datetime.date(int(val[1][:4]), int(val[1][5:7]), int(val[1][8:]))

    # setting the listed data in their respective entry fields
    dateField.set_date(expenditureDate)
    payee.set(val[2])
    description.set(val[3])
    amount.set(val[4])
    modeOfPayment.set(val[5])


# function to clear the entries from the entry fields
def clearFields():
    '''''This function will clear all the entries from the entry fields'''

    # using some global variables
    global description, payee, amount, modeOfPayment, dateField, data_table

    # defining a variable to store today's date
    todayDate = datetime.datetime.now().date()

    # setting the values in entry fields back to initial
    description.set('')
    payee.set('')
    amount.set(0.0)
    modeOfPayment.set('Cash'), dateField.set_date(todayDate)
    # removing the specified item from the selection
    data_table.selection_remove(*data_table.selection())


# function to delete the selected record
def removeExpense():
    '''''This function will remove the selected record from the table'''

    # returning the message box displaying error if no row is selected
    if not data_table.selection():
        mb.showerror('No record selected!', 'Please select a record to delete!')
        return

        # collecting the data from the selected row in dictionary format
    currentSelectedExpense = data_table.item(data_table.focus())

    # defining a variable to store the values from the collected data in list
    valuesSelected = currentSelectedExpense['values']

    # displaying a message box asking for confirmation
    confirmation = mb.askyesno('Are you sure?', f'Are you sure that you want to delete the record of {valuesSelected[2]}')

    # if the user say YES, executing the SQL DELETE FROM command
    if confirmation:
        dbconnector.execute('DELETE FROM ExpenseTracker WHERE ID=%d' % valuesSelected[0])
        dbconnector.commit()

        # calling the listAllExpenses() function
        listAllExpenses()

        # returning the message box displaying the information
        mb.showinfo('Record deleted successfully!', 'The record you wanted to delete has been deleted successfully')

    # function to delete all the entries


def removeAllExpenses():
    '''''This function will remove all the entries from the table'''

    # displaying a message box asking for confirmation
    confirmation = mb.askyesno('Are you sure?', 'Are you sure that you want to delete all the expense items from the database?', icon='warning')

    # if the user say YES, deleting the entries from the table and executing the SQL DELETE FROM command to delete all the entries
    if confirmation:
        data_table.delete(*data_table.get_children())

        dbconnector.execute('DELETE FROM ExpenseTracker')
        dbconnector.commit()

        # calling the clearFields() function
        clearFields()

        # calling the listAllExpenses() function
        listAllExpenses()

        # returning the message box displaying the information
        mb.showinfo('All Expenses deleted', 'All the expenses were successfully deleted')
    else:
        # returning the message box, if the operation is aborted
        mb.showinfo('Ok then', 'The task was aborted and no expense was deleted!')

    # function to add an expense


def addAnotherExpense():
    '''''This function will add an expense to the table and database'''

    # using some global variables
    global dateField, payee, description, amount, modeOfPayment
    global dbconnector

    # if any of the field is empty, return the message box displaying error
    if not dateField.get() or not payee.get() or not description.get() or not amount.get() or not modeOfPayment.get():
        mb.showerror('Fields empty!', "Please fill all the missing fields before pressing the add button!")
    else:
        # executing the SQL INSERT INTO command
        dbconnector.execute(
            'INSERT INTO ExpenseTracker (Date, Payee, Description, Amount, ModeOfPayment) VALUES (?, ?, ?, ?, ?)',
            (dateField.get_date(), payee.get(), description.get(), amount.get(), modeOfPayment.get())
        )
        dbconnector.commit()

        # calling the clearFields() function
        clearFields()

        # calling the listAllExpenses() function
        listAllExpenses()

        # returning the message box displaying information
        mb.showinfo('Expense added', 'The expense whose details you just entered has been added to the database')

    # function to edit the details of an expense


def editExpense():
    '''''This function will allow user to edit the details of the selected expense'''

    # using some global variables
    global data_table

    # defining a nested to update the details of the selected expense
    def editExistingExpense():
        '''''This function will update the details of the selected expense in the database and table'''

        # using some global variables
        global dateField, amount, description, payee, modeOfPayment
        global dbconnector, data_table

        # collecting the data from the selected row in dictionary format
        currentSelectedExpense = data_table.item(data_table.focus())

        # defining a variable to store the values from the collected data in list
        content = currentSelectedExpense['values']

        # executing the SQL UPDATE command to update the record in database table
        dbconnector.execute(
            'UPDATE ExpenseTracker SET Date = ?, Payee = ?, Description = ?, Amount = ?, ModeOfPayment = ? WHERE ID = ?',
            (dateField.get_date(), payee.get(), description.get(), amount.get(), modeOfPayment.get(), content[0])
        )
        dbconnector.commit()

        # calling the clearFields() function
        clearFields()

        # calling the listAllExpenses() function
        listAllExpenses()

        # returning a message box displaying the message
        mb.showinfo('Data edited', 'We have updated the data and stored in the database as you wanted')
        # destroying the edit button
        editSelectedButton.destroy()

        # returning a message box displaying error if no record is selected

    if not data_table.selection():
        mb.showerror('No expense selected!', 'You have not selected any expense in the table for us to edit; please do that!')
        return

        # calling the viewExpenseInfo() method
    viewExpenseInfo()

    # adding the Edit button to edit the selected record
    editSelectedButton = Button(
        frameL3,
        text="Edit Expense",
        font=("Bahnschrift Condensed", "13"),
        width=30,
        bg="#90EE90",
        fg="#000000",
        relief=GROOVE,
        activebackground="#008000",
        activeforeground="#98FB98",
        command=editExistingExpense
    )

    # using the grid() method to set the position of the above button on the main window screen
    editSelectedButton.grid(row=0, column=0, sticky=W, padx=50, pady=10)


# function to display the details of selected expense into words
def selectedExpenseToWords():
    '''''This function will display the details of the selected expense from the table into words'''

    # using some global variables
    global data_table

    # returning a message box displaying error, if no record is selected from the table
    if not data_table.selection():
        mb.showerror('No expense selected!', 'Please select an expense from the table for us to read')
        return

        # collecting the data from the selected row in dictionary format
    currentSelectedExpense = data_table.item(data_table.focus())

    # defining a variable to store the values from the collected data in list
    val = currentSelectedExpense['values']

    # defining the message to be displayed in the message box
    msg = f'Your expense can be read like: \n"You paid {val[4]} to {val[2]} for {val[3]} on {val[1]} via {val[5]}"'

    # returning the message box displaying the message
    mb.showinfo('Here\'s how to read your expense', msg)


# function to display the expense details into words before adding it to the table
def expenseToWordsBeforeAdding():
    '''''This function will display the details of the expense into words before adding it to the table'''

    # using some global variables
    global dateField, description, amount, payee, modeOfPayment

    # if any of the field is empty, return the message box displaying error
    if not dateField.get() or not payee.get() or not description.get() or not amount.get() or not modeOfPayment.get():
        mb.showerror('Incomplete data', 'The data is incomplete, meaning fill all the fields first!')
    else:
        # defining the message to be displayed in the message box
        msg = f'Your expense can be read like: \n"You paid {amount.get()} to {payee.get()} for {description.get()} on {dateField.get_date()} via {modeOfPayment.get()}"'

        # displaying a message box asking for confirmation
    addQuestion = mb.askyesno('Read your record like: ', f'{msg}\n\nShould I add it to the database?')

    # if the user say YES, calling the addAnotherExpense() function
    if addQuestion:
        addAnotherExpense()
    else:
        # returning a message box displaying information
        mb.showinfo('Ok', 'Please take your time to add this record')

    # main function


if __name__ == "__main__":
    # connecting to the Database
    dbconnector = sqlite3.connect("Expense_Tracker.db")
    dbcursor = dbconnector.cursor()

    # specifying the function to execute whenever the application runs
    dbconnector.execute(
        'CREATE TABLE IF NOT EXISTS ExpenseTracker (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Date DATETIME, Payee TEXT, Description TEXT, Amount FLOAT, ModeOfPayment TEXT)'
    )
    # committing the above command
    dbconnector.commit()

    # creating the main window of the application

    # creating an instance of the Tk() class
    main_win = Tk()
    # setting the title of the application
    main_win.title("EXPENSE TRACKER - Infinity Survivor")
    # setting the size and position of the window
    main_win.geometry("1415x650+400+100")
    # disabling the resizable option for better UI
    main_win.resizable(0, 0)
    # configuring the background color to #FFFAF0
    main_win.config(bg="#FFFAF0")
    # setting the icon of the application
    main_win.iconbitmap("./piggyBank.png")

    # adding frames to the window to provide structure to the other widgets
    frameLeft = Frame(main_win, bg="#FFF8DC")
    frameRight = Frame(main_win, bg="#DEB887")
    frameL1 = Frame(frameLeft, bg="#FFF8DC")
    frameL2 = Frame(frameLeft, bg="#FFF8DC")
    frameL3 = Frame(frameLeft, bg="#FFF8DC")
    frameR1 = Frame(frameRight, bg="#DEB887")
    frameR2 = Frame(frameRight, bg="#DEB887")

    # using the pack() method to set the position of the above frames
    frameLeft.pack(side=LEFT, fill="both")
    frameRight.pack(side=RIGHT, fill="both", expand=True)
    frameL1.pack(fill="both")
    frameL2.pack(fill="both")
    frameL3.pack(fill="both")
    frameR1.pack(fill="both")
    frameR2.pack(fill="both", expand=True)

    # ---------------- Adding widgets to the frameL1 frame ----------------

    # adding the label to display the heading
    headingLabel = Label(
        frameL1,
        text="EXPENSE TRACKER",
        font=("Bahnschrift Condensed", "25"),
        width=20,
        bg="#8B4513",
        fg="#FFFAF0"
    )

    # adding the label to display the subheading
    subheadingLabel = Label(
        frameL1,
        text="Data Entry Frame",
        font=("Bahnschrift Condensed", "15"),
        width=20,
        bg="#F5DEB3",
        fg="#000000"
    )

    # using the pack() method to set the position of the above labels
    headingLabel.pack(fill="both")
    subheadingLabel.pack(fill="both")

    # ---------------- Adding widgets to the frameL2 frame ----------------

    # creating some labels to ask user to enter the required data
    # date label
    dateLabel = Label(
        frameL2,
        text="Date:",
        font=("consolas", "11", "bold"),
        bg="#FFF8DC",
        fg="#000000"
    )

    # description label
    descriptionLabel = Label(
        frameL2,
        text="Description:",
        font=("consolas", "11", "bold"),
        bg="#FFF8DC",
        fg="#000000"
    )

    # amount label
    amountLabel = Label(
        frameL2,
        text="Amount:",
        font=("consolas", "11", "bold"),
        bg="#FFF8DC",
        fg="#000000"
    )

    # payee label
    payeeLabel = Label(
        frameL2,
        text="Payee:",
        font=("consolas", "11", "bold"),
        bg="#FFF8DC",
        fg="#000000"
    )

    # mode of payment label
    modeLabel = Label(
        frameL2,
        text="Mode of \nPayment:",
        font=("consolas", "11", "bold"),
        bg="#FFF8DC",
        fg="#000000"
    )

    # using the grid() method to set the position of the above labels in the grid format
    dateLabel.grid(row=0, column=0, sticky=W, padx=10, pady=10)
    descriptionLabel.grid(row=1, column=0, sticky=W, padx=10, pady=10)
    amountLabel.grid(row=2, column=0, sticky=W, padx=10, pady=10)
    payeeLabel.grid(row=3, column=0, sticky=W, padx=10, pady=10)
    modeLabel.grid(row=4, column=0, sticky=W, padx=10, pady=10)

    # instantiating the StringVar() class to retrieve the data in the string format from the user
    description = StringVar()
    payee = StringVar()
    modeOfPayment = StringVar(value="Cash")
    # instantiating the DoubleVar() class to retrieve the amount detail in double datatype
    amount = DoubleVar()

    # creating a drop-down calendar for the user to enter the date
    dateField = DateEntry(
        frameL2,
        date=datetime.datetime.now().date(),
        font=("consolas", "11"),
        relief=GROOVE
    )

    # creating entry fields to enter the labelled data
    # field to enter description
    descriptionField = Entry(
        frameL2,
        text=description,
        width=20,
        font=("consolas", "11"),
        bg="#FFFFFF",
        fg="#000000",
        relief=GROOVE
    )

    # field to enter the amount
    amountField = Entry(
        frameL2,
        text=amount,
        width=20,
        font=("consolas", "11"),
        bg="#FFFFFF",
        fg="#000000",
        relief=GROOVE
    )

    # field to enter payee information
    payeeField = Entry(
        frameL2,
        text=payee,
        width=20,
        font=("consolas", "11"),
        bg="#FFFFFF",
        fg="#000000",
        relief=GROOVE
    )

    # creating a drop-down menu to enter the mode of payment
    modeField = OptionMenu(
        frameL2,
        modeOfPayment,
        *['Cash', 'Cheque', 'Credit Card', 'Debit Card', 'UPI', 'Paytm', 'Google Pay', 'PhonePe', 'Razorpay']
    )
    # using the config() method to configure the width, font style, and background color of the option menu
    modeField.config(
        width=15,
        font=("consolas", "10"),
        relief=GROOVE,
        bg="#FFFFFF"
    )

    # using the grid() method to set the position of the above widgets in the grid format
    dateField.grid(row=0, column=1, sticky=W, padx=10, pady=10)
    descriptionField.grid(row=1, column=1, sticky=W, padx=10, pady=10)
    amountField.grid(row=2, column=1, sticky=W, padx=10, pady=10)
    payeeField.grid(row=3, column=1, sticky=W, padx=10, pady=10)
    modeField.grid(row=4, column=1, sticky=W, padx=10, pady=10)

    # ---------------- Adding widgets to the frameL3 frame ----------------

    # creating buttons to manipulate data
    # insert button
    insertButton = Button(
        frameL3,
        text="Add Expense",
        font=("Bahnschrift Condensed", "13"),
        width=30,
        bg="#90EE90",
        fg="#000000",
        relief=GROOVE,
        activebackground="#008000",
        activeforeground="#98FB98",
        command=addAnotherExpense
    )

    # convert button
    convertButton = Button(
        frameL3,
        text="Convert to Text before Adding",
        font=("Bahnschrift Condensed", "13"),
        width=30,
        bg="#90EE90",
        fg="#000000",
        relief=GROOVE,
        activebackground="#008000",
        activeforeground="#98FB98",
        command=expenseToWordsBeforeAdding
    )

    # reset button
    resetButton = Button(
        frameL3,
        text="Reset the fields",
        font=("Bahnschrift Condensed", "13"),
        width=30,
        bg="#FF0000",
        fg="#FFFFFF",
        relief=GROOVE,
        activebackground="#8B0000",
        activeforeground="#FFB4B4",
        command=clearFields
    )

    # using the grid() method to set the position of the above buttons
    insertButton.grid(row=0, column=0, sticky=W, padx=50, pady=10)
    convertButton.grid(row=1, column=0, sticky=W, padx=50, pady=10)
    resetButton.grid(row=2, column=0, sticky=W, padx=50, pady=10)

    # ---------------- Adding widgets to the frameR1 frame ----------------

    # creating buttons to manipulate data
    # view button
    viewButton = Button(
        frameR1,
        text="View Selected Expense\'s Details",
        font=("Bahnschrift Condensed", "13"),
        width=35,
        bg="#FFDEAD",
        fg="#000000",
        relief=GROOVE,
        activebackground="#A0522D",
        activeforeground="#FFF8DC",
        command=viewExpenseInfo
    )

    # edit button
    editButton = Button(
        frameR1,
        text="Edit Selected Expense",
        font=("Bahnschrift Condensed", "13"),
        width=35,
        bg="#FFDEAD",
        fg="#000000",
        relief=GROOVE,
        activebackground="#A0522D",
        activeforeground="#FFF8DC",
        command=editExpense
    )

    # convert button
    convertSelectedButton = Button(
        frameR1,
        text="Convert Selected Expense to a Sentence",
        font=("Bahnschrift Condensed", "13"),
        width=35,
        bg="#FFDEAD",
        fg="#000000",
        relief=GROOVE,
        activebackground="#A0522D",
        activeforeground="#FFF8DC",
        command=selectedExpenseToWords
    )

    # delete button
    deleteButton = Button(
        frameR1,
        text="Delete Selected Expense",
        font=("Bahnschrift Condensed", "13"),
        width=35,
        bg="#FFDEAD",
        fg="#000000",
        relief=GROOVE,
        activebackground="#A0522D",
        activeforeground="#FFF8DC",
        command=removeExpense
    )

    # delete all button
    deleteAllButton = Button(
        frameR1,
        text="Delete All Expense",
        font=("Bahnschrift Condensed", "13"),
        width=35,
        bg="#FFDEAD",
        fg="#000000",
        relief=GROOVE,
        activebackground="#A0522D",
        activeforeground="#FFF8DC",
        command=removeAllExpenses
    )

    # using the grid() method to set the position of the above buttons
    viewButton.grid(row=0, column=0, sticky=W, padx=10, pady=10)
    editButton.grid(row=0, column=1, sticky=W, padx=10, pady=10)
    convertSelectedButton.grid(row=0, column=2, sticky=W, padx=10, pady=10)
    deleteButton.grid(row=1, column=0, sticky=W, padx=10, pady=10)
    deleteAllButton.grid(row=1, column=1, sticky=W, padx=10, pady=10)

    # ---------------- Adding widgets to the frameR2 frame ----------------

    # creating a table to display all the entries
    data_table = ttk.Treeview(
        frameR2,
        selectmode=BROWSE,
        columns=('ID', 'Date', 'Payee', 'Description', 'Amount', 'Mode of Payment')
    )

    # creating a horizontal scrollbar to the table
    Xaxis_Scrollbar = Scrollbar(
        data_table,
        orient=HORIZONTAL,
        command=data_table.xview
    )

    # creating a vertical scrollbar to the table
    Yaxis_Scrollbar = Scrollbar(
        data_table,
        orient=VERTICAL,
        command=data_table.yview
    )

    # using the pack() method to set the position of the scrollbars
    Xaxis_Scrollbar.pack(side=BOTTOM, fill=X)
    Yaxis_Scrollbar.pack(side=RIGHT, fill=Y)

    # configuring the horizontal and vertical scrollbars on the table
    data_table.config(yscrollcommand=Yaxis_Scrollbar.set, xscrollcommand=Xaxis_Scrollbar.set)

    # adding different headings to the table
    data_table.heading('ID', text='S No.', anchor=CENTER)
    data_table.heading('Date', text='Date', anchor=CENTER)
    data_table.heading('Payee', text='Payee', anchor=CENTER)
    data_table.heading('Description', text='Description', anchor=CENTER)
    data_table.heading('Amount', text='Amount', anchor=CENTER)
    data_table.heading('Mode of Payment', text='Mode of Payment', anchor=CENTER)

    # adding different columns to the table
    data_table.column('#0', width=0, stretch=NO)
    data_table.column('#1', width=50, stretch=NO)
    data_table.column('#2', width=95, stretch=NO)
    data_table.column('#3', width=150, stretch=NO)
    data_table.column('#4', width=450, stretch=NO)
    data_table.column('#5', width=135, stretch=NO)
    data_table.column('#6', width=140, stretch=NO)

    # using the place() method to set the position of the table on the main window screen
    data_table.place(relx=0, y=0, relheight=1, relwidth=1)

    # using mainloop() method to run the application
    main_win.mainloop()
