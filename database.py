import cv2
import sqlite3
import base64
import os
from datetime import datetime

class Database(object):

    def __init__(self):
        self.createDatabase()
        self.createTables()
        #self.createTestUsers()

    def convertToBinaryData(self,filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData

    def write_file(self,data, filename):
        # Convert binary data to proper format and write it on Hard Disk
        with open(filename, 'wb') as file:
            file.write(data)

    def createDatabase(self):
        self.db = sqlite3.connect("my.db")
    
    def closeConnection(self):
        self.db.close()

    def createTables(self):
        cur = self.db.cursor()
        cur.execute("create table IF NOT EXISTS USER_ACTIVITY(id string, d1 text, img blob)")
        cur.execute("create table IF NOT EXISTS USER_CREDENTIALS(id string, passHash blob)")
        self.db.commit()

    def insertImageRecord(self,id,filename): 
        self.db.execute("insert into USER_ACTIVITY values(?, datetime('now'), ?)", (id, self.convertToBinaryData(filename)))
        self.db.commit()

    def retrieveImage(self,id):
        cur = self.db.cursor()
        query = "select img from USER_ACTIVITY where _rowid_ = ?"
        cur.execute(query,(id,))
        img  =cur.fetchone()[0];
        return img

    def saveImageToDisk(self,img,filename):
        self.write_file(img,filename)

    def encryptPassword(self,password):
        return base64.b64encode(password.encode("ascii"))

    def createTestUsers(self):
        self.db.execute("insert into USER_CREDENTIALS values(?,?)" ,("tanmay",self.encryptPassword("test1@123")))
        self.db.execute("insert into USER_CREDENTIALS values(?,?)" ,("testuser1",self.encryptPassword("test2@123")))
        self.db.execute("insert into USER_CREDENTIALS values(?,?)" ,("testuser2",self.encryptPassword("test3@123")))
        self.db.commit()

    def checkCredentials(self,id,password):
        cur = self.db.cursor()
        query = "select passHash from USER_CREDENTIALS where id = ?"
        cur.execute(query,(id,))
        DbpassHash  =cur.fetchone()[0];
        if DbpassHash == self.encryptPassword(password):
            return True
        else:
            return False

    def generateReport(self):
        cur = self.db.cursor()
        query = "select id, d1 , _rowid_ from USER_ACTIVITY"
        cur.execute(query)

        rows = cur.fetchall()
       
        table = ""
        for row in rows:
            table += "<tr>\n"
            table += "<td>"+row[0]+"</td><td>"+row[1]+"</td><td> <a href=\"http://0.0.0.0:8080/view/"+str(row[2])+"\">Image</a></td>"
            table += "</tr>\n"

        return table

#Program starts here
if __name__ == "__main__":
    dbObj = Database()
    dbObj.insertImageRecord("tanmay","./images/image1.png")
    img=dbObj.retrieveImage("tanmay")
    dbObj.saveImageToDisk(img,"./images/retrievedFile.png")
    val = dbObj.checkCredentials("tanmay","test1@1234")
    print ("Pass CHeck" + str(val))
    print( dbObj.generateReport())