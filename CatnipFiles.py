

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

def aboutBox():
    messagebox.showinfo("About", "Catnip Files Version 1.0\nSusanna Pohto 2021")

def searchBox():
    messagebox.showwarning("Your search", "Nothing was found")

root = Tk()
root.title("CATNIP FILES")
root.geometry("1050x500")
root.iconbitmap("C:/Users/icon.ico")
root.configure(bg = "#1ABC9C")

comboLabel = Label(root, text = "Choose field", bg = "#1ABC9C").place(x = 10, y = 20)
comboBox = ttk.Combobox(root, values=["All", 
                                    "Criminal ID",
                                    "Criminal name",
                                    "Gang name",
                                    "Gang role"])
comboBox.place(x = 10, y = 40)
comboBox.current(0) # default is All
searchLabel = Label(root, text = "Search value", bg = "#1ABC9C").place(x = 10, y = 70)
searchEntry = Entry(root, width = 20)
searchEntry.place(x = 10, y = 90)
searchEntry.configure(state = "disable")
showLabel = Label(root, text = "Database", bg = "#1ABC9C").place(x = 200, y = 20)
tree =  ttk.Treeview(root, column = ("column1", "column2", "column3", "column4"), show = 'headings', height = 12)
tree.heading("#1", text = "CRIMINAL ID", anchor = W)
tree.heading("#2", text = "CRIMINAL NAME", anchor = W)
tree.heading("#3", text = "GANG NAME", anchor = W)
tree.heading("#4", text = "GANG ROLE", anchor = W)
tree.place(x = 200, y = 40)

def readCombo(event = None):
    searchEntry.delete(0, "end")
    a = comboBox.get()
    if a != "All":
        searchEntry.configure(state = "normal")
    else:
        searchEntry.configure(state = "disable")
comboBox.bind("<<ComboboxSelected>>", readCombo) # reads the box without button press

nameLabel = Label(root, text = "Add / edit name", bg = "#1ABC9C").place(x = 10, y = 170)
nameEntry = Entry(root, width = 20)
nameEntry.place(x = 10, y = 190)
gangLabel = Label(root, text = "Add / edit gang name", bg = "#1ABC9C").place(x = 10, y = 220)
gangEntry = Entry(root, width = 20)
gangEntry.place(x = 10, y = 240)
roleLabel = Label(root, text = "Add / edit gang role", bg = "#1ABC9C").place(x = 10, y = 270)
roleEntry = Entry(root, width = 20)
roleEntry.place(x = 10, y = 290)
idEntryHidden = Entry(root)

def clearEntries():
    idEntryHidden.delete(0, "end")
    nameEntry.delete(0, "end")
    gangEntry.delete(0, "end")
    roleEntry.delete(0, "end")

def showAll():
    conn = sqlite3.connect("cats.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM myTable")
    result = cur.fetchall()
    if result:
        tree.delete(*tree.get_children()) # clears the treeview
        for row in result:
            tree.insert("", END, values = row)
    else:
        searchBox()
    cur.close()
    conn.close()

def showChosen():
    clearEntries()
    conn = sqlite3.connect("cats.db")
    cur = conn.cursor()
    a = comboBox.get()
    b = searchEntry.get()
    if a == "All":
        cur.execute("SELECT * FROM myTable")
    elif a == "Criminal ID":
        cur.execute("SELECT * FROM myTable WHERE criminal_id = ?", (b))
    elif a == "Criminal name":
        cur.execute("SELECT * FROM myTable WHERE criminal_name LIKE ?", (b,)) # b, reads the whole value
    elif a == "Gang name":
        cur.execute("SELECT * FROM myTable WHERE gang_name LIKE ?", (b,))
    elif a == "Gang role":
        cur.execute("SELECT * FROM myTable WHERE gang_role LIKE ?", (b,))
    result = cur.fetchall()
    if result:
        tree.delete(*tree.get_children()) # clears the treeview
        for row in result:
            tree.insert("", END, values = row)
    else:
        searchBox()
    cur.close()
    conn.close()
    searchEntry.delete(0, "end")

def addInfo():
    conn = sqlite3.connect("cats.db")
    cur = conn.cursor()
    name = nameEntry.get()
    gang = gangEntry.get()
    role = roleEntry.get()
    #--- making a table ---
    table = "CREATE TABLE IF NOT EXISTS myTable (criminal_id INTEGER PRIMARY KEY,  criminal_name TEXT, gang_name TEXT, gang_role TEXT);"
    cur.execute(table)
    #--- adding to table ---
    cur.execute("INSERT INTO myTable (criminal_id, criminal_name, gang_name, gang_role) VALUES (?,?,?,?)", (None, name, gang, role))
    conn.commit()
    #--- updates the tree
    cur.execute("SELECT * FROM myTable")
    result = cur.fetchall()
    if result:
        tree.delete(*tree.get_children()) # clears the treeview
        for row in result:
            tree.insert("", END, values = row)
    else:
        searchBox()
    cur.close()
    conn.close()
    clearEntries()

def selectCriminal():
    clearEntries()
    selected = tree.selection()[0]
    values = tuple(tree.item(selected)["values"])
    a, b, c, d = values # unpacking tuple
    # set values
    idEntryHidden.insert(0, a)
    nameEntry.insert(0, b)
    gangEntry.insert(0, c)
    roleEntry.insert(0, d)

def editCriminal():
    # get values
    a = idEntryHidden.get()
    b = nameEntry.get()
    c = gangEntry.get()
    d = roleEntry.get()
    conn = sqlite3.connect("cats.db")
    cur = conn.cursor()
    cur.execute("UPDATE myTable SET criminal_name = ?, gang_name = ?, gang_role = ? WHERE criminal_id = ?", (b, c, d, a))
    conn.commit()
    cur.close()
    conn.close()
    clearEntries()

def deleteCriminal():
    selected = tree.selection()[0]
    values = tuple(tree.item(selected)["values"])
    a, b, c, d = values # unpacking tuple
    tree.delete(selected)
    conn = sqlite3.connect("cats.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM myTable WHERE criminal_id = ?", (a,)) # a, needed or value error
    conn.commit()
    cur.close()
    conn.close()

Button(root, text = 'Search', command = showChosen).place(x = 10, y = 130)
Button(root, text = 'Add', command = addInfo).place(x = 10, y = 330)
Button(root, text = 'Edit', command = editCriminal).place(x = 50, y = 330)
Button(root, text = 'Select', command = selectCriminal).place(x = 200, y = 330)
Button(root, text = 'Delete', command = deleteCriminal).place(x = 250, y = 330)

menubar = Menu(root)
filemenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "File", menu = filemenu)
filemenu.add_command(label = "Exit", command = root.quit)

aboutmenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "About", menu = aboutmenu)
aboutmenu.add_command(label = "About", command = aboutBox)

root.config(menu = menubar)

root.mainloop()
