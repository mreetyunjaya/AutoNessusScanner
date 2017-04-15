#!/usr/bin/env python

_author_="Shruti Sonawane"

from selenium import webdriver
import os
import time
import random
import requests
import subprocess
import sys
import json

requests.packages.urllib3.disable_warnings()



class AutoNessus:


    def __init__(self):
        self.token = ''
        self.username = '<your username>'
        self.password = '<your password>'
        self.nessus_url = 'https://localhost:8834'
        self.scanIdCtr = 0


    def checkIfUp(self,url):
        try:
            self.driver.get(url)
            print "Got access to ",url
            return True
        except Exception as ex:
            print ex
            return False


    def loginAgain(self,usr, pwd):
        # Login to Nessus.
        login = {'username': usr, 'password': pwd}
        data = self.connect('POST', '/session', data=login)
        return data['token']


    def logIn(self):
        self.driver = webdriver.Chrome()
        up = self.checkIfUp(self.nessus_url)
        if(up):
            login = {'username': self.username, 'password': self.password}
            data = self.connect('POST', '/session', data=login)
            self.token =  data['token']
            #print "token: ",self.token
            keepTrying = True
            try:
                while(keepTrying):
                    self.driver.get(self.nessus_url)
                    time.sleep(2)
                    self.driver.execute_script("document.getElementsByClassName('required login-username')[0].value='admin';")
                    self.driver.execute_script("document.getElementsByClassName('required login-password')[0].value='brickyard';")
                    self.driver.execute_script("document.getElementById('sign-in').click();")
                    time.sleep(6)
                    if self.driver.current_url == "https://localhost:8834/#/scans":
                        print "Logged in to tenable dashboard successfully!"
                        keepTrying = False
                    else:
                        print "Unable to log in. Trying again..."

            except Exception as ex:
                print ex


    def build_url(self,resource):
        return '{0}{1}'.format(self.nessus_url, resource)


    def connect(self,method, resource, data=None, params=None):
        requestHeaders = {'X-Cookie': 'token={0}'.format(self.token),'content-type': 'application/json'}
        data = json.dumps(data)
        if method == 'POST':
            r = requests.post(self.build_url(resource), data=data, headers=requestHeaders, verify=False)
        else:
            r = requests.get(self.build_url(resource), params=params, headers=requestHeaders, verify=False)

        if r.status_code != 200:
            e = r.json()
            print e['error']
            sys.exit()

        # When downloading a scan we need the raw contents not the JSON data.
        if 'download' in resource:
            return r.content
        try:
            return r.json()
        except ValueError:
            return r.content


    def launchScan(self,sid):
        print "Launching scan ",sid
        data = self.connect('POST', '/scans/{0}/launch'.format(sid))
        return data['scan_uuid']


    def listScans(self):
        try:
            print "Scan Name\t\tStatus\t\tScan ID"
            data = self.connect('GET', '/scans/')
            status_dict = dict((p['name'], p['status']) for p in data['scans'])
            id_dict = dict((b['name'], b['id']) for b in data['scans'])
            for statusName,status in status_dict.items():
                for id_name, id in id_dict.items():
                    if statusName == id_name:
                        print statusName,"\t",status,"\t\t", id

        except Exception as ex:
            print "No nessus scans found"


    def createScan(self):
        try:
            self.scanUrl = "https://localhost:8834/#/scans/new/731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65"
            if(self.checkIfUp(self.scanUrl)):
                self.driver.get(self.scanUrl)
                time.sleep(2)
                if(self.driver.current_url == "https://localhost:8834/#/scans/new/731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65"):
                    print "Creating a new Basic Network Nessus scan..."
                    #self.scanIdCtr+=1
                    scanName = "NessusScan"+str(random.randint(10000000,99999999))
                    scanIPfile = open('NessusScanIPs.txt')
                    IPs=""
                    for x,line in enumerate(scanIPfile):
                        if(x==0):
                            IPs+=line.strip()
                        else:
                            IPs+=", "+line.strip()
                    print "Creating a scan for following IPs:\n",IPs
                    self.driver.execute_script("document.getElementsByClassName('editor-input required')[0].value='"+scanName+"'")
                    self.driver.execute_script("document.getElementsByClassName('editor-input required')[1].value='"+IPs+"'")
                    self.driver.execute_script("document.getElementsByClassName('button secondary editor-action primary-action noselect')[0].click();")
                    time.sleep(3)
                    print "Created new scan: ",scanName

        except Exception as ex:
            print ex


    def main(self):
        print "******************************"
        print " Running auto nessus scanner"
        print "******************************"
        print "Logging into Nessus dashboard.."
        self.logIn()
        userOption=""
        while userOption!="4":
            userOption = raw_input("\n1. Create a new scan.\n2. List all scans.\n3. Perform nessus scan\n4. Exit\nEnter option: ")
            if(userOption=='1'):
                self.createScan()
            elif (userOption=='2'):
                self.listScans()
            elif (userOption=='3'):
                scanID = raw_input("Enter scan ID to perform nessus scan: ")
                uuid = self.launchScan(scanID)
                print uuid
            elif (userOption=='4'):
                sys.exit(0)

if __name__ == '__main__':
    AutoNessus().main()
