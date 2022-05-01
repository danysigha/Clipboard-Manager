class User():
    def __init__(self, userID, password=None, currentCardID, defaultFolderID, shelfTime, email, firstname, lastname, passwordExists = 0):
        self.userID = userID
        self.password = password
        self.currentCardID = currentCardID
        self.defaultFolderID = defaultFolderID
        self.shelfTime = shelfTime
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.passwordExists = passwordExists

        userdatas = [
        (userID, password, passwordExists, currentCardID, 
        defaultFolderID, shelfTime, email, firstname, lastname )
        ]

        cursor.executemany("INSERT INTO user VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", user_datas)
        conn.commit()

