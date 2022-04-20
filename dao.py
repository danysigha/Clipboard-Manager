class dao():
	def __init__(self):
		#connect to database
		conn = sqlite3.connect('ClipboardManager_DB.db')
		cursor = conn.cursor()




	# some functions
	def print_table(table_content): # just for printing all the result
	    for i in range(len(table_content)):
	        print("=========== " + str(table_content[i][0]) +  " ===========")
	        for j in range(len(table_content[i])):
	            print(table_content[i][j])

	def print_card(cardID): # just for debugging
	    test_info_card = ["cardID", "cardContent", "cardCategory", "sourceApplication", "dataType", "cardAddedDate", "cardModifiedDate", "cardState", "favoriteSelected", "folderID"]
	    cursor.execute('SELECT ' + cardAttributes + ' FROM card WHERE cardID == ' + str(cardID) + ';')
	    table_list = cursor.fetchall()
	    for j in range(len(table_list[0])):
	        if (test_info_card[j] == "cardState"):
	            if (table_list[0][j]):
	                print(test_info_card[j] + ": Not Hidden")
	            else:
	                print(test_info_card[j] + ": Hidden")
	        elif (test_info_card[j] == "favoriteSelected"):
	            if (table_list[0][j]):
	                print(test_info_card[j] + ": Selected")
	            else:
	                print(test_info_card[j] + ": Not selected")
	        else:
	            print(test_info_card[j] + ": " + str(table_list[0][j]))

	def test_db(userID, data_type = "all"):
	    test_info_card = ["cardID", "cardContent", "cardCategory", "sourceApplication", "dataType", "cardAddedDate", "cardModifiedDate", "cardState", "favoriteSelected", "folderID"]
	    test_info_folder = ["folderID", "folderName", "userID"]
	    test_info_user = ["userID", "password", "saltText", "currentCardID", "currentFolderID", "shelfTime"]

	    # print user table
	    if (data_type == "user"):
	        cursor.execute('SELECT * FROM user WHERE userID == ' + str(userID) + ';')
	        table_list = cursor.fetchall()
	        for i in range(len(table_list)):
	            print("=============================")
	            for j in range(len(table_list[i])):
	                print(test_info_user[j] + ": " + str(table_list[i][j]))

	    # print folder table
	    elif (data_type == "folder"):
	        cursor.execute('SELECT * FROM folder WHERE userID == ' + str(userID) + ';')
	        table_list = cursor.fetchall()
	        for i in range(len(table_list)):
	            print("=============================")
	            for j in range(len(table_list[i])):
	                print(test_info_folder[j] + ": " + str(table_list[i][j]))

	    # print card table
	    elif (data_type == "card"):
	        cursor.execute('SELECT cardID, cardContent, cardCategory, sourceApplication, datatype, cardAddedDate, cardModifiedDate, cardState, favoriteSelected, card.folderID FROM card, folder WHERE folder.userID == ' + str(userID) + ' AND folder.folderID == card.folderID')
	        table_list = cursor.fetchall()
	        for i in range(len(table_list)):
	            print("=============================")
	            for j in range(len(table_list[i])):
	                if (test_info_card[j] == "cardState"):
	                    if (table_list[i][j]):
	                        print(test_info_card[j] + ": Not Hidden")
	                    else:
	                        print(test_info_card[j] + ": Hidden")
	                elif (test_info_card[j] == "favoriteSelected"):
	                    if (table_list[i][j]):
	                        print(test_info_card[j] + ": Selected")
	                    else:
	                        print(test_info_card[j] + ": Not selected")
	                else:
	                    print(test_info_card[j] + ": " + str(table_list[i][j]))

	            # result = cursor.fetchall()
	            # print(result)
	            # print("Belongs to user " + str(result[0][0]))

	    else:
	        print("========= USER =========")
	        test_db(userID, "user")
	        print("========= FOLDER =========")
	        test_db(userID, "folder")
	        print("========= CARD =========")
	        test_db(userID, "card")

	def addCard(userID, content, category, sourceApplication, dataType): # to be implemented even more later -> copy card
	    # find the user's default folder
	    cursor.execute('SELECT defaultFolderID FROM user WHERE userID == ' + str(userID) + ";")
	    defaultFolderID_loc = cursor.fetchall()[0][0]

	    cursor.execute('INSERT INTO card(cardContent, cardCategory, sourceApplication, datatype, cardAddedDate, cardModifiedDate, cardState, favoriteSelected, folderID) VALUES(?, ?, ?, ?, datetime("now", "localtime"), datetime("now", "localtime"), 1, 0, ?)', (content, category, sourceApplication, dataType, defaultFolderID_loc))

	    # get the currentCardID -> maybe can be done by the upper layer or dnt need it
	    cursor.execute('SELECT cardID FROM card, folder WHERE card.folderID == folder.folderID AND folder.userID == '+ str(userID) + ';')
	    result = cursor.fetchall()
	    cardIDs = list()
	    for i in range(len(result)):
	        cardIDs.append(result[i][0])
	    cardIDs.sort() # so cardIDs[-1] would be the most recent card added (currentCardID)

	    cursor.execute('UPDATE user SET currentCardID = ' + str(cardIDs[-1]) + ' WHERE userID == ' + str(userID) + ';')

	# paste function to be implemented later
	def pasteCard(cardID):
	    cursor.execute('SELECT cardContent FROM card WHERE cardID == ' + str(cardID) + ';')
	    result = cursor.fetchall()
	    return result[0][0]

	# delete
	def deleteCard(cardID):
	    cursor.execute('DELETE FROM card WHERE cardID == ' + str(cardID) + ';')

	def automaticDelete_shelftime(userID):
	    # this must be called once in a while by the main system for the system to check and delete
	    cursor.execute('SELECT userID, shelfTime FROM user WHERE userID == ' + str(userID))
	    shelftime_months = cursor.fetchall()[0][1]
	    # print(shelftime_months)
	    cursor.execute('SELECT cardAddedDate FROM card WHERE cardAddedDate <= datetime(\'now\', \'localtime\', \'-' + str(shelftime_months) +' months\');')

	# search
	    # search by title? <- not necessary
	    # search by keyword (content)
	    # search by date (from when to when)
	def searchCard(userID, searchType, searchContent):
	    # for keyword search please enter the search content as the user enters
	    # for date search please keep the format of start_date~end_date
	        # ex) '2013-02-21~2015-04-21' when start_date == 2013-02-21 AND end_date == 2015-04-21
	    if (searchType == "byKeyword"):
	        cursor.execute('SELECT ' + cardAttributes + ' FROM card, folder WHERE folder.userID == ' + str(userID) + ' AND cardContent LIKE "%' + str(searchContent) +'%" ORDER BY cardModifiedDate DESC;')
	        pass
	    elif (searchType == 'byDate'):
	        startDate = searchContent.split('~')[0]
	        endDate = searchContent.split('~')[1]
	        cursor.execute('SELECT ' + cardAttributes + ' FROM card, folder WHERE folder.userID == ' + str(userID) + ' AND folder.folderID == card.folderID AND cardAddedDate >= datetime("' + str(startDate) +'") AND cardAddedDate <= datetime("' + str(endDate) +'");')

	    return cursor.fetchall()

	# sorting
	def showAvailableFolders(userID):
	    cursor.execute('SELECT folderID, folderName FROM folder WHERE userID == ' + str(userID) + ';')
	    return cursor.fetchall()

	def showAllFavorite(userID):
	    cursor.execute('SELECT ' + cardAttributes + ' FROM folder, card WHERE userID == ' + str(userID) + ' AND folder.folderID == card.folderID AND favoriteSelected == 1;')

	    return cursor.fetchall()
	    # favorite_card_temp = cursor.fetchall()
	    # favoriteCard_List = []
	    #
	    # for i in range(len(favorite_card_temp)):
	    #     favoriteCard_List.append(favorite_card_temp[i][0])
	    #
	    # return favoriteCard_List

	def showCardDataType(userID, datatype):
	    cursor.execute('SELECT ' + cardAttributes + ' FROM folder, card WHERE userID == ' + str(userID) + ' AND folder.folderID == card.folderID AND card.datatype == "' + str(datatype).capitalize() + '";')
	    return cursor.fetchall()

	def sortCard(folderID, sortType, whatOrder):
	    # the folderID is included because we usually will sort within the folder that the user is looking at currently.
	    # please enter the folder that the user is currently taking a look at
	    cursor.execute('SELECT ' + cardAttributes + ' FROM card WHERE folderID == ' + str(folderID) + ' ORDER BY ' + str(sortType) + ' ' + str(whatOrder) + ';')
	    return cursor.fetchall()

	# change shelf time
	def changeShelfTime(userID, newShelfTime):
	    cursor.execute('UPDATE user SET shelfTime = ' + str(newShelfTime) + ' WHERE userID == ' + str(userID) + ';')

	# set password?
	    # hashing

	# hide card
	def changeStateCard(cardID):
	    cursor.execute('SELECT cardID, cardState FROM card WHERE cardID == ' + str(cardID) + ';')
	    if (cursor.fetchall()[0][1]):
	        cursor.execute('UPDATE card SET cardState = 0 WHERE cardID == ' + str(cardID) + ';')
	    else:
	        cursor.execute('UPDATE card SET cardState = 1 WHERE cardID == ' + str(cardID) + ';')
	    # print(cursor.fetchall()[0][1])
	    # return cursor.fetchall()
	    # cursor.execute('UPDATE user SET cardState = ' + str(newShelfTime) + ' WHERE userID == ' + str(userID) + ';')

	# favorite function
	def favoriteCard(cardID):
	    cursor.execute('SELECT cardID, favoriteSelected FROM card WHERE cardID == ' + str(cardID) + ';')
	    if (cursor.fetchall()[0][1]):
	        cursor.execute('UPDATE card SET favoriteSelected = 0 WHERE cardID == ' + str(cardID) + ';')
	    else:
	        cursor.execute('UPDATE card SET favoriteSelected = 1 WHERE cardID == ' + str(cardID) + ';')

	# create folder
	def createFolder(userID, folderName):
	    cursor.execute("INSERT INTO folder(folderName, userID) VALUES(?, ?)", (folderName, userID))

	# delete folder
	def deleteFolder(folderID):
	    cursor.execute('DELETE FROM folder WHERE folderID == ' + str(folderID) + ';')

	# update folder
	def updateFolderID_all(userID, currentFolderID, newFolderID):
	    # this function changes the folderID inside the card entity, not the folder itself
	    # this function changes all the folderIDs of the matching cards
	    # can be used to change entire card deck.
	    cursor.execute('UPDATE card SET folderID = ' + str(newFolderID) + ' WHERE folderID == ' + str(currentFolderID) + ';')

	def updateFolderID_indiv(userID, cardID, newFolderID):
	    # this function changes the folderID inside the card entity, but solely one card.
	    cursor.execute('UPDATE card SET folderID = ' + str(newFolderID) + ' WHERE cardID == ' + str(cardID) +';')

	# rename folder
	def updateFolder_Name(userID, currentFolderName, newFolderName): # because we do not know what the folderID is on point, let the program do it
	    # find currentFolderID
	    cursor.execute('UPDATE card SET folderName = ' + str(newFolderName) + ' WHERE folderName == ' + str(currentFolderName))

	# userID INTEGER primary key,
	# password TEXT NOT NULL,
	# saltText TEXT NOT NULL,
	# currentCardID INTEGER NOT NULL,
	# defaultFolderID INTEGER NOT NULL,
	# shelfTime INTEGER NOT NULL
	def addUser(password, saltText):
	    # this sets the currentCardID (the most recent cardID) and the defaultFolderID as -1 temporarily.
	    # the currentCardID will be changed if the user adds the first card
	    # the defaultFolderID will be changed soon within this function
	    cursor.execute('INSERT INTO user(password, saltText, currentCardID, defaultFolderID, shelfTime) VALUES(?, ?, -1, -1, 24)', (password, saltText))

	    cursor.execute('SELECT userID from user')
	    new_userID = cursor.fetchall()[-1][0]

	    createFolder(new_userID, "Default")

	    cursor.execute('SELECT folderID from folder WHERE userID == ' + str(new_userID) + ';')
	    new_user_defaultFolderID = cursor.fetchall()[0][0]

	    cursor.execute('UPDATE user SET defaultFolderID = ' + str(new_user_defaultFolderID) + ' WHERE userID == ' + str(new_userID) + ';')

	def showAllUsers():
	    # this function returns list of all the userIDs
	    cursor.execute('SELECT userID FROM user')

	    temp_userList = cursor.fetchall()
	    userID_list = []

	    for user in range(len(temp_userList)):
	        userID_list.append(temp_userList[user][0])

	    return userID_list