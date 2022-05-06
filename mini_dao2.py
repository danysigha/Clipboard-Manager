import bcrypt
import sqlite3
import smtplib, ssl
import string
import random


class password_decorator():
	def __init__(self, function):
		self.function = function

	def password_is_valid(self,pwd):
		h = self.get_password()
		return bcrypt.checkpw(pwd.encode('utf-8'), h)

	def get_password(self):
			conn = sqlite3.connect('ClipboardManager_DB.db')
			cursor = conn.cursor()
			records = cursor.execute("""SELECT password FROM user LIMIT 1""")
			h = ''
			for row in records:
				h = row[0]
			conn.close()
			return h;
		
	def __call__(self, *args, **kwargs):
		pwd = args[0]
		if self.password_is_valid(pwd):
			self.function(*args, **kwargs)
			result = True
		else:
			result = False

		return result

class dao():

	def __init__(self):
		pass


	#sends encrypted password to database
	@password_decorator
	def change_password(oldpwd,newpwd):
		conn = sqlite3.connect('ClipboardManager_DB.db')
		cursor = conn.cursor()
		salt = bcrypt.gensalt()
		hashed_pwd = bcrypt.hashpw(newpwd.encode('utf-8'), salt)
		cursor.execute("""UPDATE user SET password = (?) WHERE userID = 1""" ,(hashed_pwd,))
		conn.commit()

	def set_password(self,newpwd):
		conn = sqlite3.connect('ClipboardManager_DB.db')
		cursor = conn.cursor()
		salt = bcrypt.gensalt()
		hashed_pwd = bcrypt.hashpw(newpwd.encode('utf-8'), salt)
		cursor.execute("""UPDATE user SET password = (?) WHERE userID = 1""", (hashed_pwd,))
		cursor.execute("""UPDATE user SET password_exists = 1 WHERE userID = 1""")
		conn.commit()

	
	def set_email(email):
		conn = sqlite3.connect('ClipboardManager_DB.db')
		cursor = conn.cursor()
		cursor.execute("""UPDATE user SET email = (?) WHERE userID = 1""" ,(email))
		conn.commit()


	def password_is_valid(self,pwd):
		h = self.get_password()
		return bcrypt.checkpw(pwd.encode('utf-8'), h)

	def get_password(self):
			conn = sqlite3.connect('ClipboardManager_DB.db')
			cursor = conn.cursor()
			records = cursor.execute("""SELECT password FROM info LIMIT 1""")
			h = ''
			for row in records:
				h = row[0]
			conn.close()
			return h;


	def get_password_exists():
		conn = sqlite3.connect('ClipboardManager_DB.db')
		cursor = conn.cursor()
		records = cursor.execute("""SELECT password_exists FROM user LIMIT 1""")
		email = ''
		for row in records:
			h = row[0]

		return h;

	def changeShelftime(month):
		conn = sqlite3.connect('ClipboardManager_DB.db')
		cursor = conn.cursor()
		cursor.execute("""UPDATE user SET shelfTime = (?) WHERE userID = 1""", (month,))

	def send_email():
		conn = sqlite3.connect('ClipboardManager_DB.db')
		cursor = conn.cursor()
		records = cursor.execute("""SELECT email FROM user LIMIT 1""")
		email = ''
		for row in records:
			email = row[0]
		port = 465  # For SSL
		smtp_server = "smtp.gmail.com"
		sender_email = "yourclipboardmanager@gmail.com" 
		receiver_email = email  
		password = "ecqibpmoeknjxwbm"

		temp = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 10))
		
		conn = sqlite3.connect('ClipboardManager_DB.db')
		cursor = conn.cursor()
		salt = bcrypt.gensalt()
		hashed_pwd = bcrypt.hashpw(temp.encode('utf-8'), salt)
		cursor.execute("""UPDATE user SET password = (?) WHERE userID = 1""", (hashed_pwd,))
		conn.commit()



		message = ("""\
		Subject: Your temporary password.

		This is your temporary password: {}. Please use this password to sign in and
		remember to change password to your own.""".format(temp))

		context = ssl.create_default_context()
		with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
		    server.login(sender_email, password)
		    server.sendmail(sender_email, receiver_email, message)




