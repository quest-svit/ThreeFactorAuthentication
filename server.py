#!/usr/bin/env python

from __future__ import print_function # adds compatibility to python 2
from __future__ import unicode_literals

import sys
import logging
import web
import json
import numpy as np  # useful for many scientific computing in Python
import pandas as pd # primary data structure library
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import xlrd
import os
import webbrowser
import database as db
import capture_and_identify as ci

#reload(sys)

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s %(message)s',filename='logs/FaceRecogntionApp.log',level=logging.INFO)
web.config.debug = False

urls = (
    "/", "Index", 
    '/(js|css|images)/(.*)', 'static', 
    "/app/(.*)" ,"ImageDisplay", 
    "/app" , "Application" , 
    "/error" , "error" , 
    "/report" , "report" , 
    "/view/(.*)" , "view")
        
render = web.template.frender('static/form.html')
render2 = web.template.frender('static/plot.html')
error_render = web.template.frender('static/error.html')

def plotBarChart(country,chartType):
    logging.info("[Country] " + country)
    df_corona = pd.read_csv('./data/corona_Tracker_09-24-2020.csv')
    df_corona.drop(['FIPS','Admin2', 'Last_Update','Province_State','Lat', 'Long_', 'Combined_Key', 'Confirmed','Incidence_Rate','Case-Fatality_Ratio'], axis=1, inplace=True)
    df_corona.set_index('Country_Region', inplace=True)
    df_country = df_corona.loc[country]
    df_country.plot(kind=chartType, figsize=(7, 6))
    plt.xlabel('Category') # add to x-label to the plot
    plt.xticks(rotation=None)
    plt.ylabel('Number of Patients') # add y-label to the plot
    plt.title(country + ' Corona Status') # add title to the plot
    #plt.legend()
    fileName =  country +'_Corona_'+chartType+'_Chart.png'
    logging.info("[FileName] "+ fileName)
    plt.savefig('images/'+fileName)
    plt.close();
    del df_corona
    del df_country
    del country
    return fileName


class Application(object):
    def GET(self):
        return render2()

class Index(object):
    # In the browser, this displays "Index", but also causes the error on the server side.
    def GET(self):
        return render()

    def POST(self):
        dbObj = db.Database()
        data = web.data()
        web.header('Content-Type', 'application/json')
        #result  = data;
        try:
            result = json.loads(data)
            val = dbObj.checkCredentials(result["username"],result["password"])

            if val == True:
                logging.info("Password Verification : Success")
                Person,confidence=ci.captureAndIdentify()

                if result["username"] == Person:
                    logging.info("Face Recognition : Success")	
                    webbrowser.open("http://0.0.0.0:8080/app")

                else:
                    logging.error("Face Recognition : Failed")
                    logging.error("Login User: " +result["username"])
                    logging.error("Face Identified: " + Person)
                    dbObj.insertImageRecord(result["username"],"./images/image1.png")
                    webbrowser.open("http://0.0.0.0:8080/error")
            else:
                logging.error("Password Verification or Face Recognition Failed")
                webbrowser.open("http://0.0.0.0:8080/error")
            
            dbObj.closeConnection()

        except ValueError as err:
            dbObj.closeConnection()
            return render2()

class ImageDisplay(object):
    def GET(self,country):
        if (country == 'favicon.ico'):
            pass
        else:
            user_data = web.input(ctype=None)
            
            if user_data.ctype is None:
                logging.info("No params passed")
                chartType="bar"  #default type
            else:
                logging.info("[ChartType] " + user_data.ctype)
                chartType = user_data.ctype
            
            logging.info("[Server] " + country)
            logging.info("[ChartType] " + chartType)
            fileName= plotBarChart(country,chartType)
            imageBinary = open("./images/"+fileName,'rb').read()
            del fileName
            del country
            return imageBinary

class static:
    def GET(self, media, file):
        try:
            f = open(media+'/'+file, 'r')
            return f.read()
        except:
            return '' # you can send an 404 error here if you want   

class error:
    def GET(self):
        return error_render()         


class report:
    def GET(self):
        dbObj = db.Database()

        html =  "<html>\n"
        html += "<head>\n"
        html += "<link rel=\"stylesheet\" type=\"text/css\" href=\"http://0.0.0.0:8080/static/myview.css\" media=\"all\">\n"
        html += "</head>\n"
        html += "<body id=\"main_body\">\n"
        html += "<img id=\"top\" src=\"./static/top.png\" alt=\"\" >\n"
        html += "<div>\n"
        html += "<h1>Suspicious Activity Report</h1>\n"
        html += "<div id=\"form_container\" class=\"form_container\">\n"
        html += "<h2>Suspicious Activity Report</h2>\n"
        html += "<table class=\"table\">\n"
        html += "<tbody>\n"
        html += "<tr><th>UserID</th><th>Timestamp</th><th>Link</th></tr>"

        tableRows = dbObj.generateReport()

        html += tableRows
        html += "</tbody>\n"
        html += "</table>\n"
        html += "</div>\n"
        html += "</div>\n"
        html += "<img id=\"bottom\" src=\"./static/bottom.png\" alt=\"\">"
        html += "</body>\n"
        html += "</html>\n"
        dbObj.closeConnection()
        return html


class view:
    def GET(self,id):
        dbObj = db.Database()
        img =  dbObj.retrieveImage(id)
        dbObj.closeConnection()
        return img


if __name__ == "__main__":
    logging.info("[Server] Starting server.")
    app = web.application(urls, globals())
    app.run()
