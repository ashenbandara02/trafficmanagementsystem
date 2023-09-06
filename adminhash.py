import hashlib

def hasher(password):
    """Admin must be added manually so in order for that when adding by executing sql queries we must provided the hashed password to the password field for that we use this script"""
    print("Hashed Pass: " + hashlib.md5(password.encode('utf-8')).hexdigest())

if __name__ == "__main__":
    hasher(password=str(input("Password to Hash : ")))