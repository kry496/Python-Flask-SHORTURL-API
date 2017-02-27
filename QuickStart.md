#QUICK START GUIDE
  
1)On your Linux machine, as root, make a folder, let’s call it ‘poc’:
Command: mkir poc
Command: cd poc
2) Setup a python virtual environment:
Command: pip install virtualenv
Command: virtualenv -p /usr/bin/python2.7 venv
Command: source venv/bin/activate
Command: cd venv
3) Install extra modules needed for the flask app to work:
Command: pip install flask short_url
4) Copy the myapp.py from email to this folder:
5) start the flask app on the local system and do not close this terminal:
Command: python myapp.py
# shebang not set, you can set it, change permissions and run it as a program.
6) Now, use another terminal to communicate with the flask app via HTTP-REST API as follows:
# so, that the app can run in the foreground for debugging.
7) To get the short url for google.com, run the following command
Command: curl -i -H "Content-Type: text/plain" -X POST -d 'http://google.com' http://localhost:5000/addurl
#Example response: YOUR SHORT URL is - > http://localhost:5000/867nv
#Note: You can choose to delete the database and reset the app.
#Note: Removing the Database will reset all timestamps collected for testing Access times analytics.
#Note: Ignore variable assignment warning, for first run of the app. (since Debugger is on)
8) Click the short url generated from previous command or enter it in the browser for redirection.
#if you put it in the browser, it should redirect immediately.
9) To get Daily, weekly and total access details for a short Url, set the short Url to the bitlink query parameter
Command: curl -v -L -G -d "bitlink=http://localhost:5000/867nv" http://localhost:5000/getstats
#Example response: Daily Hits: <value> Weekly Hits: <Value> Total Hits: <Value>
# On Fresh DB, all values will be same.
# Steps to insert older time stamps shown in README file.
