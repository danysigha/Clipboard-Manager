class User():
    def __init__(self, userID, currentCardID, defaultFolderID, shelfTime, email, password="", passwordExists = 0):
        self.userID = userID
        self.password = password
        self.currentCardID = currentCardID
        self.defaultFolderID = defaultFolderID
        self.shelfTime = shelfTime
        self.email = email
        self.passwordExists = passwordExists

#         userdatas = [
#         (userID, password, passwordExists, currentCardID,
#         defaultFolderID, shelfTime, email, firstname, lastname )
#         ]

#         cursor.executemany("INSERT INTO user VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", user_datas)
#         conn.commit()
