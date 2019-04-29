#!/usr/bin/env python3
from tkinter import *
import tkinter.messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from bankaccount import BankAccount

win = Tk()
win.title('FedUni Banking')
win.geometry("440x640+0+0")

# The account number entry and associated variable
account_number_var = StringVar()




pin_number_var = StringVar()
amount_balance_var = StringVar()

# The balance label and associated variable
balance_var = StringVar()
balance_var.set('Balance: $0.00')
balance_label = Label(win, textvariable=balance_var)

# The Entry widget to accept a numerical value to deposit or withdraw
amount_entry = Entry(win, font=('arial', 10),  bd=10,
                        insertwidth=6, bg="white", justify='right' ,textvariable=amount_balance_var)

# The transaction text widget holds text of the accounts transactions
transaction_text_widget = Text(win, height=10, width=48)


# The bank account object we will work with
account = BankAccount()

#---------------------remove this later only for test purpose--------------------------------------------------------
account_number_var.set('123456')
pin_number_var.set('7890')

account_file_name =None
# ---------- Button Handlers for Login Screen ----------

def clear_pin_entry():
    '''Function to clear the PIN number entry when the Clear / Cancel button is clicked.'''
     # Clear the pin number entry here
    global account_number_var
    global pin_number_var
    pin = ""
    pin_number_var.set(pin)
    account_number_var.set(pin)


def handle_pin_button(numbers):
    '''Function to add the number of the button clicked to the PIN number entry via its associated variable.'''
# Limit to 4 chars in length
# Set the new pin number on the pin_number_var
    pin = numbers.widget['text']
    if len(pin_number_var.get()) >= 4:
        return
    # Set the new pin number on the pin_number_var
    pin_number_var.set(pin_number_var.get() + pin)


def log_in():
    '''Function to log in to the banking system using a known account number and PIN.'''
    global account
    global pin_number_var
    global pin
    account_number_filename=account_number_var.get()+".txt"

    try:
        global account_filename
        f = open(account_number_filename, 'r')
        file = f.name
        filename, fileextention = file.split('.')
        if not filename:
            raise Exception("Account doesn't exist")

        account_filename=open(account_number_filename,'r+')

        with open(account_number_filename, 'r') as f:
            f_contents = f.readlines()
            account.account_number = f_contents[0].strip()
            pin_number=f_contents[1].strip()

        if pin_number_var.get() != pin_number:
            raise Exception("Invalid PIN code")

        account.pin_number = pin_number
        tkinter.messagebox.showinfo("Login", "Logged in successfully")

        account.balance = f_contents[2].strip()
        account.interest_rate = f_contents[3].strip()

        # Section to read account transactions from file - start an infinite 'do-while' loop here
        while True:
            line = read_line_from_account_file().strip()
            if not line:
                break
            if line == 'Deposit':
                account.transaction_list.append(float(read_line_from_account_file().strip()))
            elif line == 'Withdrawal':
                account.transaction_list.append(-float(read_line_from_account_file().strip()))
        remove_all_widgets()
        create_account_screen()
        # Attempt to read a line from the account file, break if we've hit the end of the file. If we
        # read a line then it's the transaction type, so read the next line which will be the transaction amount.
        # and then create a tuple from both lines and add it to the account's transaction_list

        # Close the file now we're finished with it
        f.close()

    except Exception as error:
        # Show error messagebox and & reset BankAccount object to default...
        # traceback.print_exc()
        tkinter.messagebox.showinfo("Login Error", error)
        #  ...also clear PIN entry and change focus to account number entry
        pin_number_var.set('')
        account_number_var.set('')

# ---------- Button Handlers for Account Screen ----------

def save_and_log_out():
    global account

    # Save the account with any new transactions
    account.export_to_file()
    # Reset the bank acount object
    account=BankAccount()
    # Reset the account number and pin to blank
    account_number_var.set('')
    pin_number_var.set('')


    # Remove all widgets and display the login screen again
    remove_all_widgets()
    create_login_screen()



def perform_deposit():
    global account
    global balance_label
    global balance_var
    global amount_balance_var

    try:
        amount_value=amount_balance_var.get()
        account.export_to_file()

        account.deposit(amount_value)
        # Update the transaction widget with the new transaction by calling account.get_transaction_string()
        # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
        #       contents, and finally configure back to state='disabled' so it cannot be user edited.
        account_transaction_string = account.get_transaction_string()
        transaction_text_widget.config(state=NORMAL)
        transaction_text_widget.delete(1.0, END)
        transaction_text_widget.insert(END, account_transaction_string)
        transaction_text_widget.config(state=DISABLED)

        # Change the balance label to reflect the new balance
        balance_var.set('Balance: $' + str(account.balance))
        balance_label.config(text=balance_var)

        # Clear the amount entry
        amount_balance_var.set('')

        # Update the interest graph with our new balance
        plot_interest_graph()

        # Catch and display exception as a 'showerror' messagebox with a title of 'Transaction Error' and the text of the exception
    except Exception as e:
        # traceback.print_exc()
        amount_balance_var.set('')
        tkinter.messagebox.showerror("Transaction Error", e)

    # Try to increase the account balance and append the deposit to the account file

    # Get the cash amount to deposit. Note: We check legality inside account's deposit method

    # Deposit funds

    # Update the transaction widget with the new transaction by calling account.get_transaction_string()
    # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
    #       contents, and finally configure back to state='disabled' so it cannot be user edited.

    # Change the balance label to reflect the new balance

    # Clear the amount entry

    # Update the interest graph with our new balance

    # Catch and display exception as a 'showerror' messagebox with a title of 'Transaction Error' and the text of the exception


def perform_withdrawal():
    '''Function to withdraw the amount in the amount entry from the account balance and add an entry to the transaction list.'''
    global account
    global balance_label
    global balance_var
    global amount_balance_var

    # Try to increase the account balance and append the deposit to the account file
    try:
        # Get the cash amount to deposit. Note: We check legality inside account's withdraw method
        amount_entry_value = amount_balance_var.get()

        # Withdraw funds
        account.withdraw(amount_entry_value)

        # Update the transaction widget with the new transaction by calling account.get_transaction_string()
        # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
        #       contents, and finally configure back to state='disabled' so it cannot be user edited.
        account_transaction_string = account.get_transaction_string()
        transaction_text_widget.config(state=NORMAL)
        transaction_text_widget.delete(1.0, END)
        transaction_text_widget.insert(END, account_transaction_string)
        transaction_text_widget.config(state=DISABLED)

        # Change the balance label to reflect the new balance
        balance_var.set('Balance: $' + str(account.balance))
        balance_label.config(text=balance_var)

        # Update the interest graph with our new balance
        plot_interest_graph()
        # Clear the amount entry
        amount_balance_var.set('')



    except Exception as e:
        # Catch and display any returned exception as a messagebox 'showerror'
        tkinter.messagebox.showerror("Transaction Error", e)
        amount_balance_var.set('')

    # Try to increase the account balance and append the deposit to the account file

    # Get the cash amount to deposit. Note: We check legality inside account's withdraw method

    # Withdraw funds

    # Update the transaction widget with the new transaction by calling account.get_transaction_string()
    # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
    #       contents, and finally configure back to state='disabled' so it cannot be user edited.

    # Change the balance label to reflect the new balance

    # Clear the amount entry

    # Update the interest graph with our new balance

    # Catch and display any returned exception as a messagebox 'showerror'


# ---------- Utility functions ----------

def remove_all_widgets():
    '''Function to remove all the widgets from the window.'''
    global win
    for widget in win.winfo_children():
        widget.grid_remove()



def read_line_from_account_file():
    '''Function to read a line from the accounts file but not the last newline character.
       Note: The account_file must be open to read from for this function to succeed.'''
    global account_filename
    if account_filename is not None:
        return account_filename.readline()[0:-1]

def plot_interest_graph():
    '''Function to plot the cumulative interest for the next 12 months here.'''

    # YOUR CODE to generate the x and y lists here which will be plotted
    x = []
    y = []
    # This code to add the plots to the window is a little bit fiddly so you are provided with it.
    # Just make sure you generate a list called 'x' and a list called 'y' and the graph will be plotted correctly.
    figure = Figure(figsize=(5, 2), dpi=100)
    figure.suptitle('Cumulative Interest 12 Months')
    a = figure.add_subplot(111)

    oldbalance=float(account.balance)
    for x_value in range(1, 12):
        value = oldbalance + float(account.interest_rate) / 12 * oldbalance
        x.append(x_value)
        y.append(value)
        oldbalance = value
    print(y)
    a.plot(x, y, marker='o')
    a.grid()

    canvas = FigureCanvasTkAgg(figure, win)
    canvas.draw()
    graph_widget = canvas.get_tk_widget()
    graph_widget.grid(row=4, column=0, columnspan=5, sticky='nsew')


# ---------- UI Screen Drawing Functions ----------


def create_login_screen():
    '''Function to create the login screen.'''


    # ----- Row 0 -----
    # 'FedUni Banking' label here. Font size is 32.
    title = Label(win, height=2, text="FedUniBanking", font=("arial", 32, 'bold'), bd=10, anchor=CENTER)
    title.grid(row=0, column=0, columnspan=3)

    # # ----- Row 1 -----
    # Acount Number / Pin label here

    accounttext = Label(win, height='5', text="Account Number/PIN")
    accounttext.grid(row=1, column=0)

    # # # Account number entry here

    account_number_entry = Entry(win, width=15, font=('arial', 10), textvariable=account_number_var, bd=10,
                                    insertwidth=15, bg="white", justify='right')
    account_number_entry.grid(row=1, column=1)

    # # # Account pin entry here
    account_pin_entry = Entry(win, width=12, font=('arial', 12), textvariable=pin_number_var, bd=10,
                                 insertwidth=12, bg="white", justify='right', show='*')
    account_pin_entry.grid(row=1, column=2)

    # # ----- Row 2 -----
    button1 = Button(win, padx=60, pady=37, bd=8, fg="black", font=('arial', 8, 'bold'), text="1",bg="white")
    button1.bind('Button-1',handle_pin_button)
    button1.grid(row=2, column=0,sticky=N + S + E + W)

    button2 = Button(win, padx=60, pady=37, bd=8, fg="black", font=('arial', 8, 'bold'), text="2",bg="white")
    button2.bind('Button-1',handle_pin_button)
    button2.grid(row=2, column=1,sticky=N + S + E + W)

    button3 = Button(win, padx=57, pady=37, bd=8, fg="black", font=('arial', 8, 'bold'), text="3",bg="white")
    button3.bind('Button-1',handle_pin_button)
    button3.grid(row=2, column=2,sticky=N + S + E + W)
    # # Buttons 1, 2 and 3 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.


    # # ----- Row 3 -----
    button4 = Button(win, padx=60, pady=37, bd=8, fg="black", font=('arial', 8, 'bold'), text="4",
                          bg="white")
    button4.bind('Button-1',handle_pin_button)
    button4.grid(row=3, column=0,sticky=N + S + E + W)

    button5 = Button(win, padx=60, pady=37, bd=8, fg="black", font=('arial', 8, 'bold'), text="5",bg="white")
    button5.bind('Button-1',handle_pin_button)
    button5.grid(row=3, column=1,sticky=N + S + E + W)

    button6 = Button(win, padx=57, pady=37, bd=8, fg="black", font=('arial', 8, 'bold'), text="6",bg="white")
    button6.bind('Button-1',handle_pin_button)
    button6.grid(row=3, column=2,sticky=N + S + E + W)
    # # Buttons 4, 5 and 6 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.

    # # ----- Row 4 -----
    button7 = Button(win, padx=60, pady=37, bd=8, fg="black", font=('arial', 8, 'bold'), text="7",bg="white")
    button7.bind('Button-1',handle_pin_button)
    button7.grid(row=4, column=0,sticky=N + S + E + W)

    button8 = Button(win, padx=60, pady=37, bd=8, fg="black", font=('arial', 8, 'bold'), text="8", bg="white")
    button8.bind('Button-1',handle_pin_button)
    button8.grid(row=4, column=1,sticky=N + S + E + W)

    button9 = Button(win, padx=57, pady=37, bd=8, fg="black", font=('arial', 8, 'bold'), text="9", bg="white")
    button9.bind('Button-1',handle_pin_button)
    button9.grid(row=4, column=2,sticky=N + S + E + W)
    #
    # # ----- Row 5 -----

    # # Cancel/Clear button here. 'bg' and 'activebackground' should be 'red'. But calls 'clear_pin_entry' function.
    clearbtn = Button(win, padx=30, pady=36, bd=8, fg="black", font=('arial', 8, 'bold'),
                           text="Cancel/Clear",
                           bg="red", command=clear_pin_entry)
    clearbtn.grid(row=5, column=0,sticky=N + S + E + W)

    # Button 0 here

    button0 = Button(win, padx=60, pady=36, bd=8, fg="black", font=('arial', 8, 'bold'), text="0",bg="white")
    button0.bind('Button-1',handle_pin_button)
    button0.grid(row=5, column=1,sticky=N + S + E + W)

    # # Login button here. 'bg' and 'activebackground' should be 'green'). Button calls 'log_in' function.
    loginbtn = Button(win, padx=45, pady=36, bd=8, fg="black", font=('arial', 8, 'bold'), text="Login",
                           bg="green", command=log_in)
    # loginbtn.bind("<Button-1>", clear_pin_entry())
    loginbtn.grid(row=5, column=2,sticky=N + S + E + W)

    button1.bind('<Button-1>', handle_pin_button)
    button2.bind('<Button-1>', handle_pin_button)
    button3.bind('<Button-1>', handle_pin_button)
    button4.bind('<Button-1>', handle_pin_button)
    button5.bind('<Button-1>', handle_pin_button)
    button6.bind('<Button-1>', handle_pin_button)
    button7.bind('<Button-1>', handle_pin_button)
    button8.bind('<Button-1>', handle_pin_button)
    button9.bind('<Button-1>', handle_pin_button)
    button0.bind('<Button-1>', handle_pin_button)

    # Set column and row weights. There are 5 columns and 6 rows (0..4 and 0..5 respectively)
    win.columnconfigure(0, weight=1)
    win.columnconfigure(1, weight=1)
    win.columnconfigure(2, weight=1)
    win.rowconfigure(0, weight=1)
    win.rowconfigure(1, weight=5)
    win.rowconfigure(2, weight=0)
    win.rowconfigure(3, weight=0)
    win.rowconfigure(4, weight=0)
    win.rowconfigure(5, weight=0)


def create_account_screen():
    global account
    global transaction_text_widget

    '''Function to create the account screen.'''
    # ----- Row 0 -----

    # FedUni Banking label here. Font size should be 24.
    title1 = Label(win, text="FedUniBanking", font=("arial", 24, 'bold'), bd=10)
    title1.grid(row=0, column=0,columnspan=5)



    accountno_txt= Label(win, text="Account number:"+account.account_number)
    accountno_txt.grid(row=1, column=1)


    balance_var.set('Balance: $' +str(account.balance))
    balance_label.grid(row=1, column=2)

    logoutbtn =Button(win, padx=17,pady=5,text="log out", bd=8, command=save_and_log_out)
    logoutbtn.grid(row=1, column=3)


    amount_txt= Label(win, height=5, width=10, text="Amount($)")
    amount_txt.grid(row=2, column=0)

    amount_entry.grid(row=2, column=1)

    depositbtn = Button(win,   padx=5, pady=10, bd=8, fg="black", font=('arial', 8, 'bold'), text="Deposit",
                      command=perform_deposit)
    depositbtn.grid(row=2, column=2)

    withdrawbtn = Button(win, padx=5, pady=10, bd=8, fg="black", font=('arial', 8, 'bold'), text="Withdraw",
                    command=perform_withdrawal)
    withdrawbtn.grid(row=2, column=3)

    scrollbar=Scrollbar(win)
    transaction_text_widget.insert(END, account.get_transaction_string())
    transaction_text_widget.grid(row=3, column=0, columnspan=5,sticky=N + S + E + W)
    scrollbar.config(command=transaction_text_widget.yview)
    transaction_text_widget.config(state=DISABLED)


    scrollbar.config(command=transaction_text_widget.yview,orient='vertical')
    scrollbar.grid(row=3, column=5, sticky=N+S)
    transaction_text_widget.configure(yscrollcommand=scrollbar.set, )
    # ----- Row 4 - Graph -----

    # Call plot_interest_graph() here to display the graph
    plot_interest_graph()

#

    # Set column and row weights here - there are 5 rows and 5 columns (numbered 0 through 4 not 1 through 5!)
    win.columnconfigure(0, weight=0)



# ---------- Display Login Screen & Start Main loop ----------
if __name__ =="__main__" :
    create_login_screen()
    win.mainloop()
