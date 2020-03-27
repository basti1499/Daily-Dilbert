Daily Dilbert Service
=========================

Description
----------------

This is a Python script which allows you to send the daily Dilbert comic strip to a list of recipients via email.

Used technologies
-----------------------

The script is written in Python 3 and can be executed on a Linux machine using Cron. It makes use of the following libraries:

 * **requests** to handle HTTP requests and access the dilbert website.
 * **BeautifulSoup** to handle the HTML code received from the HTTP request.
 * **SMTPLib** for the communication with the mailserver.
 * **shutil** for file operations like downloading the image.
 * **EmailMessage, MIMEMultipart, MIMEText and MIMEImage** to create a HTML-based email and insert the image downloaded.
 * **mysql-connector** to grab the list of recipients from a MySQL database.

Copyright
---------

This project is licensed under [_Creative Commons Namensnennung 4.0 International_](http://creativecommons.org/licenses/by/4.0/)
The Dilbert comic strip is owned and published by Scott Adams at [Dilbert.com](https://dilbert.com/)

© 2020 Bastian Hartenstein <br/>

E-Mail: [Bastian Hartenstein](mailto:basti@bastih.dev) <br/>
