#!/usr/bin/python
import requests
from bs4 import BeautifulSoup
import smtplib, ssl
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import shutil
from datetime import datetime
from datetime import date
import mysql.connector
import getDilbertInc
import getDilbertEmail

##############################################
#                                            #
#      Finding the image on dilbert.com      #
#                                            #
##############################################

todaysDate = str(datetime.date(datetime.now()))
page = "https://dilbert.com/strip/"
page += todaysDate
result = requests.get(page)
if result.status_code != 200:
    exit()
soup = BeautifulSoup(result.content, "html.parser")
img = soup.find('img', {'class':'img-responsive img-comic'})
img_url = img['src']
if not img_url.startswith('http'):
    img_url = "http:" + img_url

##############################################
#                                            #
#   Downloading the image from dilbert.com   #
#                                            #
##############################################

resp = requests.get(img_url, stream=True)
local_file = open('local_image.jpg', 'wb')
resp.raw.decode_content = True
shutil.copyfileobj(resp.raw, local_file)
del resp

##############################################
#                                            #
# Finding and adding recipients to the email #
#                                            #
##############################################

mydb = mysql.connector.connect(host=getDilbertInc.mysql_host, user=getDilbertInc.mysql_user, passwd=getDilbertInc.mysql_pw, database=getDilbertInc.mysql_db)
cursor = mydb.cursor()
cursor.execute("SELECT email FROM daily_dilbert")
recipients = cursor.fetchall()

msgRoot = MIMEMultipart('related')
msgRoot['Subject'] = 'Daily Dilbert (' + todaysDate + ')'
msgRoot['From'] = '"Daily Dilbert" <' + getDilbertInc.mail_username + '>'
msgRoot['To'] = '"Daily Dilbert" <' + getDilbertInc.mail_username + '>'
msgRoot.preamble = 'This is a multi-part message in MIME format.'

##############################################
#                                            #
#         Creating the email message         #
#                                            #
##############################################

msgAlternative = MIMEMultipart('alternative')
msgRoot.attach(msgAlternative)

msgText = MIMEText('Leider kann dein Emailprogramm die Mail nicht richtig darstellen. Tut mir Leid!')
msgAlternative.attach(msgText)

today = date.today()
dateString = ""
dateString += ("Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag")[today.weekday()]
dateString += ", den "
dateString += str(today.day)
dateString += ". "
dateString += ("Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember")[today.month-1]
dateString += " " + str(today.year)

msgText = MIMEText(getDilbertEmail.email_text % (dateString), 'html')
msgAlternative.attach(msgText)

fp = open('local_image.jpg', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()

msgImage.add_header('Content-ID', '<image1>')
msgRoot.attach(msgImage)

##############################################
#                                            #
#         Sending the finished email         #
#                                            #
##############################################

smtp = smtplib.SMTP_SSL("smtp.eu.mailgun.org", 465)
smtp.login(getDilbertInc.mail_username, getDilbertInc.mail_password)
smtp.sendmail(getDilbertInc.mail_username, recipients, msgRoot.as_string())
smtp.quit()
