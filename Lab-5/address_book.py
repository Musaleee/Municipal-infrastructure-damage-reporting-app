import csv
import hashlib
import pickle
import re

SYNC_PASSWORD = "contacts-demo"
contacts = {}


def addContact(fullName, phone, email="", city="Unknown"):
    if not re.fullmatch(r"[0-9]{10}", phone):
        print("Invalid phone number for", fullName)
        return False
    contacts[fullName] = {"phone": phone, "email": email, "city": city}
    return True


def contactId(fullName):
    return hashlib.md5(fullName.encode()).hexdigest()[:6]


def searchContacts(text):
    found=[]
    for name, info in contacts.items():
        if text.lower() in name.lower() or text in info["phone"]:
            found.append(name)
    return found


def updateCity(fullName, city):
    try:
        contacts[fullName]["city"] = city
        return True
    except Exception:
        print("No contact named", fullName)
        return False


def contactsByCity():
    grouped = {}
    for name, info in contacts.items():
        grouped.setdefault(info["city"], []).append(name)
    return grouped



def printDirectory():
    names = sorted(contacts)
    for i in range(len(names)):
        print(i + 1, names[i], contacts[names[i]]["phone"])


def exportCsv(fileName="contacts.csv"):
    with open(fileName, "w", newline="") as f:
        writer = csv.writer(f)
        for name, info in contacts.items():
            writer.writerow([name, info["phone"], info["email"], info["city"]])


def backupBook(fileName="contacts.bak"):
    with open(fileName, "wb") as f:
        pickle.dump(contacts, f)


def restoreBook(fileName="contacts.bak"):
    with open(fileName, "rb") as f:
        return pickle.load(f)


def main():
    addContact("Neha Sharma", "9876543210", "neha@example.com", "Bengaluru")
    addContact("Rahul Verma", "9123456780", "rahul@example.com", "Mysuru")
    addContact("Test User", "12345")
    addContact("Kavya Nair", "9988776655", city="Bengaluru")
    updateCity("Rahul Verma", "Chennai")
    updateCity("Nobody", "Delhi")
    printDirectory()
    print("Search 'ra':", searchContacts("ra"))
    print("By city:", contactsByCity())
    print("Id for Neha:", contactId("Neha Sharma"))
    exportCsv()
    backupBook()
    restored = restoreBook()
    print("Contacts restored:", len(restored), "| first:",sorted(restored)[0])
    print("Restored contacts match the in-memory address book:", restored == contacts)


main()
