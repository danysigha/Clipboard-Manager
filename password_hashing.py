import hashlib
import string
import random

# Trying to synchronize
def encryptPassword(password):
    saltText = "secretPassword"
    num = 100

    systemFinal = saltText + password
    finalPassword = ''
    result = hashlib.sha256(systemFinal.encode())
    finalPassword += result.hexdigest()
    result = hashlib.sha256(finalPassword.encode())

    for i in range(1, num + 1):
        result = hashlib.sha256(finalPassword.encode())

        if (i < num):
            finalPassword = ''
            finalPassword += result.hexdigest()

    return finalPassword, result.hexdigest()
