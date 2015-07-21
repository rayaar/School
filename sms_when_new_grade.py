#!/usr/bin/env python
#-*- coding: iso-8859-1 -*-
#
#  sms_when_new_grade.py
#  
#  Copyright 2013 Raymond Aarseth <raymond@aarseth.me>
#  check UIB to see if there is any new grades out. can then send SMS or a push with pushbullet to your phone
#  with the new grade.
#
#
#from future import unicode_literals
from twill.commands import *
import getpass
from bs4 import BeautifulSoup
import os
import time
import pickle
import socket
import httplib, urllib
from nexmomessage import NexmoMessage #https://github.com/marcuz/libpynexmo

def karakterListe(fil):
    soup = BeautifulSoup(open(fil))
    fag = []
    nodes = []
    for node in (soup.find_all("tr", class_="pysj0")):
            nodes.append(node)
    for node in (soup.find_all("tr", class_="pysj1")):
            nodes.append(node)
    for node in nodes:
            for n in node.find_all("td"):
                p=n.get_text().split("\n")
                for e in p:
                    fag.append(e)
    fagliste = []
    for i in range(0,len(fag),10):
        fagliste.append([fag[i+1],fag[i+2],fag[i+6],fag[i+7]])
    return fagliste

def skrivFil(liste,fil):
    pickle.dump( liste, open( fil, "wb" ) )

def hentFraFil(fil):
    karakterer = pickle.load( open( fil, "rb" ) )
    return karakterer

def hentKaraktererDokument(url,uname,pin):
    go(url)
    fv("1","fodselsnr",uname)
    fv("1","pinkode",pin)
    submit("login")
    follow("Innsyn")
    follow("Resultater")
    fil ="ht.html"
    save_html(fil)
    karakterer = karakterListe(fil)
    return karakterer

def push(liste):
    a="Det har kommer nye karakter på studentweb:\n\n"
    liste = liste[3:6]
    for fag in liste:
        points = fag[3].encode("iso-8859-1")
        if points == "":
            points="0,0"
        a = a + fag[0].encode("iso-8859-1")+"-"+fag[1].encode("iso-8859-1")+":\n Grade: " + fag[2].encode("iso-8859-1") + "\n Points: " + points +"\n"
    host =(socket.gethostname())
    message = a
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.urlencode({
"token": "dinToken",
"user": "DinBruker",
"message": message,
    }), { "Content-type": "application/x-www-form-urlencoded" })


def sendSms(liste):
    print "sender sms"
    a="Det har kommer nye karakter på studentweb:\n\n"
    liste = liste[3:6]
    for fag in liste:
        points = fag[3].encode("iso-8859-1")
        if points == "":
            points="0,0"
        a = a + fag[0].encode("iso-8859-1")+"-"+fag[1].encode("iso-8859-1")+":\n Grade: " + fag[2].encode("iso-8859-1") + "\n Points: " + points +"\n"
    text = a.decode("iso-8859-1")
    print text
    msg = {
        'reqtype': 'json',
        'api_key': "dinNøkkel",
        'api_secret': "dinapihemmelighet",
        'from': "MiSide",
        'to': "mobilnummer",
        'text': text
    }
    sms = NexmoMessage(msg)
    sms.set_text_info(msg['text'])

    sms.send_request()
    


def main():
    url = "https://studentweb.uib.no/cgi-bin/WebObjects/studentweb2?inst=UiB"#"test"
    uname  = "00000" #raw_input("fødselsnummer  (11 siffer): ")
    pin = "55555" #getpass.getpass("Pinkode: ")
    fil = ".kar"
    if os.path.exists(fil) :
        print "existing file"
        karakterer=hentFraFil(fil)
    else:
        print "first run"
        karakterer=hentKaraktererDokument(url,uname,pin)
        skrivFil(karakterer,fil)
        exit(0)

    nyekarakterer=[]
    print "ser etter nye karakterer"
    karaktersjekk=hentKaraktererDokument(url,uname,pin)
    for el in karaktersjekk:
        if el not in karakterer:
            nyekarakterer.append(el)
            skrivFil(karaktersjekk,fil)
    if len(nyekarakterer) !=0:
        print "nye karakterer"
        karakterer =hentFraFil(fil)
        karaktersjekk=[]
        #push(nyekarakterer)
        sendSms(nyekarakterer)
        nyekarakterer=[]
    else:
        print "ingen nye karakterer"

if __name__ == '__main__':
	main()
