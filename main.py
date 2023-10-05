# Password Manager

### LIBRARIES ###

try:
	import hashlib as h
	import datetime as d
	import secrets as s
	import re
	import smtplib
	import csv


except ImportError:
	print("Error... necessary libraries are unavailable.")



def randomInt(bits):  # Returns a strong random integar of "bits" bits
	try:
		num = s.randbits(bits)
		return num
	except:
		print("Error... please try again.")


def randomStr(x):  # Returns a strong random string of length "x" of characters selected from "dictionary"
	try:
		dictionary = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-_+=@[](),./#~!£$%^&*:;"
		string = ""
		for i in range(x):
			string += s.choice(dictionary)
		return string
	except:
		print("Error... please try again.")


def gen_sha3512_hash(x):  # Returns the SHA3-512 hash of "inp"
	try:
		obj = h.sha3_512()
		obj.update(x.encode())
		return str(obj.hexdigest())
	except:
		print("Error... please try again.")


def genSalt():  # Returns a stronly random 512 bit salt
	try:
		randomness = str(randomInt(4096)) + randomStr(4096)
		salt = gen_sha3512_hash(randomness)
		return salt
	except:
		print("Error... please try again.")


def addUser(username, password):  # Hashes, salts, and stores credentials in their respective files#
	try:
		usernames = []

		with open("user.db", "rt") as userFile:  # Fills the array "usernames"
			for userLine in userFile:
				usernames.append(userLine.strip("\n"))
			userFile.close()

		p = open("pass.db", "a")  # Open the database files
		s = open("salt.db", "a")
		u = open("user.db", "a")

		salt = genSalt()  # Generate hashes to store
		userHash = gen_sha3512_hash(username)
		passSalt = password + salt
		passHash = gen_sha3512_hash(passSalt)

		available = True

		for i in range(len(usernames)):
			if usernames[i] == userHash:  # Check if the username is available
				available = False

				salt = ""  # Clear variables
				userHash = ""
				passSalt = ""
				passHash = ""

		if available == True:
			p.write(passHash + "\n")  # Write values to files
			s.write(salt + "\n")
			u.write(userHash + "\n")

			salt = ""  # Clear variables
			userHash = ""
			passSalt = ""
			passHash = ""

			p.close()  # Close files
			s.close()
			u.close()

			print("Your credentials have been added!\n")

		elif available == False:
			print("That username is taken! Please try again...\n")

		else:
			print("Error! Please try again...\n")

		salt = ""  # Clear variables
		userHash = ""
		passSalt = ""
		passHash = ""

		p.close()  # Close files
		s.close()
		u.close()
	except:
		print("Error... please try again.")


def login(username, password):  # Verifies the user entered "username" and "password", and prints "Logged in!" if they're in the database
	# Test Credentials: "testUser", "testPass"

	try:
		usernames = []  # Define credential lists
		passwords = []
		salts = []

		with open("pass.db", "rt") as passFile:  # Fill lists with credentials
			for passLine in passFile:
				passwords.append(passLine.strip("\n"))
			passFile.close()

		with open("salt.db", "rt") as saltFile:
			for saltLine in saltFile:
				salts.append(saltLine.strip("\n"))
			saltFile.close()

		with open("user.db", "rt") as userFile:
			for userLine in userFile:
				usernames.append(userLine.strip("\n"))
			userFile.close()

		# Generate "username" hash for comparison & lookup
		userHash = gen_sha3512_hash(username)
		salt = ""
		passHash = ""
		location = 0  # Location of credentials in list
		found = False

		go = True
		while go:
			for i in range(len(usernames)):  # Look up location of credentials
				if usernames[i] == userHash:
					location = i
					found = True
					go = False
			go = False

		if found == True:  # Look up the rest of the credentials
			salt = salts[location]
			passSalt = password + salt
			passHash = gen_sha3512_hash(passSalt)

		# Verify the credentials and return True if correct
		if userHash == usernames[location] and passHash == passwords[location]:
			print("Logged in!\n")
		elif userHash != usernames[location] or passHash != passwords:
			print("Credentials not found! Please try again...\n")

		usernames = []  # Clear credential lists
		passwords = []
		salts = []

		userHash = ""
		salt = ""
		passHash = ""
		location = 0
	except:
		print("Error... please try again.")

### END FUNCTIONS ###


regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

def check(email):
	if(re.fullmatch(regex, email)):
		return 1

	else:
		return 0


def check_date(date):
	format = "%d-%m-%Y"
	res = False
	try:
		res = bool(datetime.strptime(test_str, format))
	except ValueError:
		res = False
	return res


def has_header(csv_file):
    with open(csv_file, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        first_row = next(csv_reader, None)
        if first_row is not None and any(first_row):
            return True
        else:
            return False

def add_to_csv(email, expdate):
	fields = ['Email', 'ExpDate']
	row = [[email, expdate]]

	filename = "expDate.csv"
	if(not has_header(filename)):
		with open(filename, 'w') as csvfile:  
			csvwriter = csv.writer(csvfile) 
			csvwriter.writerow(fields)
			csvwriter.writerows(row)
	else:
		with open(filename, 'a') as csvfile:
			csvwriter = csv.writer(csvfile)
			csvwriter.writerows(row)

### MAIN PROGRAM ###

go = True
while go:
	try:
		option = int(input("Enter 1 to sign up\nEnter 2 to login\nEnter 3 to exit\n: "))

		if option == 1:
			username = input("\nPlease enter a username: ")
			valid_email1 = True
			while valid_email1:
				email = input("Please enter a email: ")
				if not check(email):
					print("Please enter a valid email")
					continue
				else:
					valid_email1 = False

			password = input("Please enter a password: ")

			valid_date = True
			while valid_date:
				exp_date = input("Please give expiration date (yyyy-mm-dd) : ")
				if not check_date(exp_date):
					print("Please enter a valid date")
					continue
				else:
					valid_date = False

			add_to_csv(email, exp_date)
			addUser(username, password)
	
		elif option == 2:
			username = input("\nPlease enter a username: ")
			email = input("Please enter a email: ")
			if not check(email):
				print("Please enter a valid email")
				continue
			password = input("Please enter a password: ")
			addUser(username, password)
	
			
		elif option == 3:
			go = False
	except:
		print("Error... please try again.\n")

### END MAIN PROGRAM ###
