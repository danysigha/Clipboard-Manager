import bcrypt
import sqlite3


class password_decorator():
	def __init__(self, function):
		self.function = function

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
		cursor.execute("""UPDATE user SET password = (?) WHERE userID = 1""" ,(hashed_pwd))
		conn.commit()

	def set_password(newpwd):
		conn = sqlite3.connect('ClipboardManager_DB.db')
		cursor = conn.cursor()
		salt = bcrypt.gensalt()
		hashed_pwd = bcrypt.hashpw(newpwd.encode('utf-8'), salt)
		cursor.execute("""UPDATE user SET password = (?) WHERE userID = 1""", (hashed_pwd,))
		cursor.execute("""UPDATE user SET password_exists = 1 WHERE userID = 1""")
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

	def get_email(self):
		conn = sqlite3.connect('ClipboardManager_DB.db')
		cursor = conn.cursor()
		records = cursor.execute("""SELECT email FROM user LIMIT 1""")
		email = ''
		for row in records:
			h = row[0]

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
		# connect with Google's servers
		smtp_ssl_host = 'smtp.gmail.com'
		smtp_ssl_port = 465
		# use username or email to log in
		username = 'yourclipboardmanager@gmail.com'
		password = 'ClipboardManager2022'

		from_addr = 'yourclipboardmanager@gmail.com'
		email = self.get_email()
		to_addrs = [email]

		# the email lib has a lot of templates
		# for different message formats,
		# on our case we will use MIMEText
		# to send only text
		#generate temporary password for user
		temp_password = random.choice()
		self.set_password(newpwd)
		message = MIMEText('Your temporary password is: {}. Please change your password ASAP by inserting your temporary password in the current password field.'.format(temp_password))
		message['Subject'] = ('Your temporary password')
		message['from'] = from_addr
		message['to'] = ', '.join(to_addrs)

		# we'll connect using SSL
		server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
		# to interact with the server, first we log in
		# and then we send the message
		server.login(username, password)
		server.sendmail(from_addr, to_addrs, message.as_string())
		server.quit()




