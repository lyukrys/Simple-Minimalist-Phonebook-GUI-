from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import sqlite3

app = QtWidgets.QApplication([])
dlg = uic.loadUi("phonebook.ui")


class SqliteHelper(): # Setting up Sqlite3
    
    def __init__(self, name):
        self.cursor = None
        self.conn = None
        
        if name: # If name is valid then run this function to open name.db
            self.open(name)
            
    def open(self, name): # open file
        self.conn = sqlite3.connect(name) # Sett up conn in Sqlite3 and open db
        self.cursor = self.conn.cursor() # Define cursor
        print(sqlite3.version) # Print Sqlite Version (for debug only)
        
    def create_table(self): # Create a table if it doesn't exist (used once since table is hard-coded)
        c = self.cursor
        c.execute("""CREATE TABLE IF NOT EXISTS users (phonenumber INTEGER PRIMARY KEY, 
                  contact_name TEXT)""") # table with rows [phonenumber(id), contact_name]
        
    def add_user(self, phone_number, contact_name): # add a new user to table
        c = self.cursor
        c.execute("""INSERT INTO users (phonenumber, contact_name) VALUES (?,?)""",
                  (phone_number, contact_name)) # Take in variables phone_number and contact_name
        self.conn.commit() # Commit change made to table
        
    def delete_user(self, phone_number): # Delete a user
        c = self.cursor
        c.execute(""" SELECT * FROM users WHERE phonenumber="%d" """ % (phone_number)) # Select the user with given phonenumber
        
        c.execute(""" DELETE FROM users WHERE phonenumber="%d" """ % (phone_number)) # Delete user based on given phonenumber
        self.conn.commit() # Commit change made to table

contact_db = SqliteHelper("phonebook_DATA_BASE.db")
contact_db.create_table()
#test.add_user(1234567890, "test1")
#test.delete_user(1234567890)

def addPerson():
    
    name = dlg.lineEdit_name.text() # Get name from lineEdit_name
    phonenumber = dlg.lineEdit_phone.text() # Get phonenumber from lineEdit_phone
    
    try: # Catch sqlite3 errors
        if name != "" and phonenumber != "": # If text entered into field is valid
            contact_db.add_user(phonenumber, name) # Add user to db
            dlg.listWidget.addItem("Name: %s | #: %s" % (name, phonenumber)) # Add user to listWidget 
        
        else:
            errorMessage("Error","Either what you entered is not valid or you must have left a field empty")
    
    except sqlite3.Error as e:
        errorMessage("Error", str(e) + """\nWhat you have entered is either a duplicate or not valid, please try again""")
        print(e)
    
    # Cleaning everything up and setting focus
    dlg.lineEdit_name.clear()
    dlg.lineEdit_phone.clear()
    dlg.lineEdit_name.setFocus()


def delPerson():
    for item in dlg.listWidget.selectedItems():
        
        # Finding where the phone # starts
        text = item.text()
        start = text.find("#")
        
        # Deleting user based on phonenumber
        contact_db.delete_user(int(  text[(start+3):]  ))
        
        #print(item.text())
        
        dlg.listWidget.takeItem(dlg.listWidget.row(item))        

        
        
        # DELETE USER FROM phonebook.db

def main(): # Run at the start of the application
    conn = sqlite3.connect("phonebook_DATA_BASE.db")
    c = conn.cursor()
    
    c.execute("""SELECT contact_name, phonenumber FROM users""")
    for row in c.fetchall()[::-1]: # Run list in reverse since c.fetchalso() reverses list itself
        dlg.listWidget.addItem("Name: %s | #: %s" % (row[0], row[1])) # Add contact info to listWidget
        print(row)
    
    c.close()
    conn.close()
    
        

def errorMessage(title, message): # Display error message
    QMessageBox.information(None, title, message)

if __name__ == "__main__": # Check if first time application running
    dlg.listWidget.setAlternatingRowColors(True)
    main()
    


# Checking for user input
dlg.pushButton_enter.clicked.connect(addPerson)
dlg.lineEdit_phone.returnPressed.connect(addPerson)

dlg.listWidget.itemClicked.connect(delPerson)

# Display the app
dlg.show()
app.exec()