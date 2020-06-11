from tkinter import *
from tkinter import ttk
import mysql.connector
import socket

def init():
	window.title("Welcome to mis")
	window.geometry('450x450')
	window.configure(background = "white");

def setLabels():
	cardId = Label(window ,text = "id").grid(row = 0,column = 0)

	firstName = Label(window ,text = "First Name").grid(row = 2,column = 0)
	lastName = Label(window ,text = "Last Name").grid(row = 3,column = 0)
	email = Label(window ,text = "Email").grid(row = 4,column = 0)
	number = Label(window ,text = "Contact Number").grid(row = 5,column = 0)
	countryOrigin = Label(window ,text = "Country of Origin").grid(row = 6,column = 0)

	bloodType = Label(window ,text = "Blood Type").grid(row = 8,column = 0)
	bDonor = Label(window ,text = "Organ Donor").grid(row = 9,column = 0)

	bRefugee = Label(window ,text = "Refugee").grid(row = 11,column = 0)

def setLayoutGrid():
	cardId.grid(row = 0,column = 2)
	firstName.grid(row = 2,column = 2)
	lastName.grid(row = 3,column = 2)
	email.grid(row = 4,column = 2)
	number.grid(row = 5,column = 2)
	countryOrigin.grid(row = 6,column = 2)
	bloodType.grid(row = 8,column = 2)
	bDonor.grid(row = 9,column = 2)
	bRefugee.grid(row = 11, column = 2)

	col_count, row_count = window.grid_size()
	for col in range(col_count):
	    window.grid_columnconfigure(col, minsize=20)
	for row in range(row_count):
	    window.grid_rowconfigure(row, minsize=20)

def getCardID():
	conn.send(b'READ_CARD')
	data = conn.recv(BUFFER_SIZE)
	if not data: return
	print('Received data: ', data.decode("utf-8"))
	conn.send(data)
	return data.decode("utf-8")

def clearEntries():
	cardId.delete(0, 'end')
	firstName.delete(0, 'end')
	lastName.delete(0, 'end')
	email.delete(0, 'end')
	number.delete(0, 'end')
	countryOrigin.delete(0, 'end')
	bloodType.delete(0, 'end')
	bDonor.delete(0, 'end')
	bRefugee.delete(0, 'end')

def readFromCard():
	statusText.set("Reading from Card...")
	db = mysql.connector.connect(host="localhost", user="root", passwd="", database="mis")
	
	# procitaj id sa kartice
	statusText.set("Put the card on the reader")
	id = (getCardID(),)

	cursor = db.cursor()
	sqlform = "select * from refugee where id=%s"
	cursor.execute(sqlform, id)
	
	result = cursor.fetchall()
	if len(result) == 0:
		statusText.set("The card is not registered")
		return
	result = result[0]

	clearEntries()

	cardId.insert(0,result[0])
	firstName.insert(0, result[1])
	lastName.insert(0, result[2])
	email.insert(0, result[3])
	number.insert(0, result[4])
	countryOrigin.insert(0, result[5])
	bloodType.insert(0, result[6])

	if result[7] == 1:
		bDonor.insert(0, "Yes")
	else:
		bDonor.insert(0, "No")
	
	if result[8] == 1:
		bRefugee.insert(0, "Yes")
	else:
		bRefugee.insert(0, "No")

	db.close()

	statusText.set("Read data from Card")
	

def writeToCard():
	statusText.set("Validating data...")
	firstNameTxt = firstName.get() #dohvati sta pise u polju firstName
	lastNameTxt = lastName.get()
	emailTxt = email.get()
	numberTxt = number.get()
	countryOriginTxt = countryOrigin.get()
	bloodTypeTxt = bloodType.get()
	bDonorTxt = bDonor.get()
	bRefugeeTxt = bRefugee.get()

	if len(firstNameTxt) == 0:
		statusText.set("Missing first name")
		return
	elif len(lastNameTxt) == 0:
		statusText.set("Missing last name")
		return
	elif len(emailTxt) == 0:
		statusText.set("Missing email")
		return
	elif len(numberTxt) == 0:
		statusText.set("Missing number")
		return
	elif len(countryOriginTxt) == 0:
		statusText.set("Missing country of origin")
		return
	elif len(bloodTypeTxt) == 0:
		statusText.set("Missing blood type")
		return
	elif len(bDonorTxt) == 0:
		statusText.set("Missing donor status")
		return
	elif len(bRefugeeTxt) == 0:
		statusText.set("Missing refugee accessibility status")
		return

	if bDonorTxt.lower() != "yes" and bDonorTxt.lower() != "no":
		statusText.set("Donor status is not in format Yes / No")
		return
	elif bDonorTxt.lower() == "yes":
		bDonorTxt = "1"
	else:
		bDonorTxt = "0"
	
	if bRefugeeTxt.lower() != "yes" and bRefugeeTxt.lower() != "no":
		statusText.set("Refugee acessibility status is not in format Yes / No")
		return
	elif bRefugeeTxt.lower() == "yes":
		bRefugeeTxt = "1"
	else:
		bRefugeeTxt = "0"
	
	bloodtypes = ["O+", "A+", "B+", "AB+", "O-", "A-", "B-", "AB-"]
	if bloodTypeTxt not in bloodtypes:
		statusText.set("Blood type is not valid")
		return

	statusText.set("Put the card on the reader")
	id = getCardID()
	cardId.insert(0, id)

	statusText.set("Writing to database...")
	db = mysql.connector.connect(host="localhost", user="root", passwd="", database="mis")
	cursor = db.cursor()

	sqlcheck = """select * from refugee where id=%s"""
	cursor.execute(sqlcheck, (id,))
	if len(cursor.fetchall()) > 0:
		statusText.set("The card has already been asigned")
		db.close()
		return

	sqlform = """insert into refugee(
			id,
	        firstname,
	        lastname,
	        email,
	        number,
	        country,
	        bloodtype,
	        donor,
	        refugee
	    ) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

	immigrant = (id, firstNameTxt, lastNameTxt, emailTxt, numberTxt, countryOriginTxt, bloodTypeTxt, bDonorTxt, bRefugeeTxt)
	cursor.execute(sqlform, immigrant)
	db.commit()
	db.close()

	statusText.set("Successfully registered immigrant")


def set_text(text, entry):
    entry.delete(0,END)
    entry.insert(0,text)
    return
    

if __name__ == "__main__":

	window = Tk()
	init()
	setLabels()

	#set entries
	cardId = Entry(window)
	firstName = Entry(window)
	lastName = Entry(window)
	email = Entry(window)
	number = Entry(window)
	countryOrigin = Entry(window)
	bloodType = Entry(window)
	bDonor = Entry(window)
	bRefugee = Entry(window)

	statusText = StringVar()
	statusText.set("Waiting for card reader to connect...")
	status = Label(window, textvariable=statusText).grid(row = 16,column = 2)

	TCP_IP = '192.168.1.101'
	TCP_PORT = 5005
	BUFFER_SIZE = 1024
	s = socket.socket()
	s.bind((TCP_IP, TCP_PORT))
	s.listen(1)
	conn, addr = s.accept()
	
	print('Conection address: ', addr)
	statusText.set("Card reader connected")

	#set buttons
	btnReadFromCard = ttk.Button(window, text="Read", command = readFromCard).grid(row=14,column=1)
	btnWriteToCard = ttk.Button(window, text="Write", command = writeToCard).grid(row=14,column=2)
	
	#resizeovanje grida/velicina entrija
	setLayoutGrid()

	window.mainloop() #drzi prozor otvorenim sve dok se ne klikne X

	