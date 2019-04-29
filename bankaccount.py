class BankAccount():

    def __init__(self):
        '''Constructor to set account_number to '0', pin_number to an empty string,
           balance to 0.0, interest_rate to 0.0 and transaction_list to an empty list.'''
        self.account_number = '0'
        self.pin_number = ''
        self.balance = 0.0
        self.interest_rate = 0.0
        self.transaction_list = []

    def changetoFloat(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def deposit(self, amount):
        '''Function to deposit an amount to the account balance. Raises an
           exception if it receives a value that cannot be cast to float.'''
        if not self.changetoFloat(amount):
            raise ValueError('Not a valid number')
        self.transaction_list.append(float(amount))
        self.balance =float(self.balance) + float(amount)
        # self.balance+=float(amount)

    def withdraw(self, amount):
        '''Function to withdraw an amount from the account balance. Raises an
           exception if it receives a value that cannot be cast to float. Raises
           an exception if the amount to withdraw is greater than the available
           funds in the account.'''
        if not self.changetoFloat(amount):
            raise ValueError('Not a valid number')
        if float(amount) > float(self.balance):
            raise ValueError('Fund not available')
        self.transaction_list.append(-float(amount))
        self.balance = float(self.balance) - float(amount)
        
        
    def get_transaction_string(self):
        '''Function to create and return a string of the transaction list. Each transaction
           consists of two lines - either the word "Deposit" or "Withdrawal" on
           the first line, and then the amount deposited or withdrawn on the next line.'''

        transaction_string=''
        for i in self.transaction_list:
            if i > 0:
                transaction_string=transaction_string+'Deposit'+"\n"
                transaction_string = transaction_string + str(i) + "\n"
            elif i < 0:
                transaction_string = transaction_string + 'Withdrawal' + "\n"
                transaction_string = transaction_string + str(-i) + "\n"
        return transaction_string


    def export_to_file(self):
        '''Function to overwrite the account text file with the current account
           details. Account number, pin number, balance and interest (in that
           precise order) are the first four lines - there are then two lines
           per transaction as outlined in the above 'get_transaction_string'
           function.'''
        with open(self.account_number+'.txt','w+') as f:
            f.write(self.account_number)
            f.write('\n')
            f.write(self.pin_number)
            f.write('\n')
            f.write(str(self.balance))
            f.write('\n')
            f.write(str(self.interest_rate))
            f.write('\n')
            f.write(self.get_transaction_string())
