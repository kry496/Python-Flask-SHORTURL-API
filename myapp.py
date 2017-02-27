from flask import Flask, request, Response, redirect
from sqlite3 import OperationalError
import sqlite3
import short_url as shrt
from urlparse import urlparse


app = Flask(__name__)

host = 'http://localhost:5000/'

#DB and table will be created only if they don't exist
def db_create():
    with sqlite3.connect('test3.db') as con:
        try:
            con.execute("pragma foreign_keys=ON") # Need to enable foreign key constraint per DB connection
            con.execute("CREATE TABLE Test2table(ID INTEGER PRIMARY KEY, Longurl TEXT NOT NULL, Shorturl TEXT NOT NULL);")
            con.execute("CREATE TABLE Table2(ID INTEGER PRIMARY KEY, Shortid INTEGER, Timestamp TEXT NOT NULL, FOREIGN KEY(Shortid) REFERENCES Test2table(ID));")
            con.commit()
            print "DB created"
        except OperationalError:
            pass


#Test if a LONGURL is already present in DB
def test_content(longurl):
    with sqlite3.connect('test3.db') as con:
        l = (longurl,) #Best practice to consolidate values in a tuple before passing it to database
        try:
            res = con.execute("SELECT Shorturl FROM Test2table WHERE Longurl= ?", l)
            for x in res:
                surl = x[0].decode('UTF-8')
        except OperationalError:
            print " empty table" 
    return surl


# Write the LONGURL into DB, Sets the shorturl to 'shorturl' to meet NOT NULL constraint
def write_content(longurl,shorturl='shorturl'):
    with sqlite3.connect('test3.db') as con:
        l = (longurl, shorturl)
        cur = con.cursor()
        try:
            con.execute("INSERT INTO Test2table (LONGURL, SHORTURL) VALUES (?, ?)", l)
            con.commit()
        except OperationalError:
            print 'unable to insert the URL'


#MAKES THE SHORTURL UPDATE
def read_content(longurl,shorturl):
    with sqlite3.connect('test3.db') as con:
        test =(shorturl,)
        cur = con.cursor()
        try:
            res = con.execute("SELECT ID FROM Test2table WHERE SHORTURL= ?", test)
            for x in res:
                url = shrt.encode_url(x[0])
                uurl = "".join([host,url])
                cur.execute("UPDATE Test2table SET SHORTURL = ? WHERE ID = ?", (uurl, x[0]))
                con.commit()
        except OperationalError:
            print 'update of shorturl failed'
    return uurl


#NOT CORE FUNCTIONALITY USED FOR TESTING
def read_all():
    with sqlite3.connect('test3.db') as con:
        con.execute("pragma foreign_keys=ON")
        try:
            res = con.execute("SELECT * FROM Test2table")
            print 'table1'
            for x in res:
                print x
            res = con.execute("SELECT * FROM Table2")
            print 'table2'
            for x in res:
                print x
        except OperationalError:
            print ' unable to read the database'


#UPDATES STATS TO SECOND TABLE
def add_hits(short_url):
    pk = shrt.decode_url(short_url)
    with sqlite3.connect('test3.db') as con:
        l = (pk,)
        try:
            con.execute("pragma foreign_keys=ON")
            con.execute("INSERT INTO Table2 (Shortid, Timestamp) VALUES (?, datetime('now'))", l)
            con.commit()
        except OperationalError:
            print 'unable to insert the hits'


#RETRIVE STATS
def get_stats(strurl):
    parser = urlparse(strurl)
    incoming = parser.path.strip('/')
    pk = shrt.decode_url(incoming)
    l = (pk,)
    stats = [] 
    with sqlite3.connect('test3.db') as con:
        try:
            con.execute("pragma foreign_keys=ON")
            day = con.execute("SELECT COUNT(Timestamp) FROM Table2 WHERE Timestamp >= datetime('now', '-1 day') and Shortid=?", l)
            for x in day:
                daytotal = str(x[0])   
            week = con.execute("SELECT COUNT(Timestamp) FROM Table2 WHERE Timestamp >= datetime('now', '-7 day') and Shortid=?", l)
            for x in week:
                weektotal = str(x[0])
            total = con.execute("SELECT COUNT(Timestamp) FROM Table2 WHERE Shortid=?", l)
            for x in total:
                total = str(x[0])
            stats_complete = "daily hits: " + daytotal + "\tweekly hits: " + weektotal + "\ttotal hits:" + total + "\n"
        except OperationalError:
            print 'date time access failure'
    return stats_complete


#END POINT FOR GET METHOD
@app.route('/getstats', methods=['GET'])
def return_stats():
    plaintext = request.args.get('bitlink')
    return_data = get_stats(plaintext)
    return Response(return_data, mimetype="text/plain")


#END POINT FOR POST METHOD
@app.route('/addurl', methods=['POST'])
def get_url():
    plaintext = str(request.get_data())
    parsed = urlparse(plaintext)
    if parsed.scheme == '':
        cleanurl = plaintext
    else:
        scheme = "%s://" % parsed.scheme
        cleanurl = parsed.geturl().replace(scheme, '', 1)
    return_value = 'notfound'
    try:
        return_value = test_content(cleanurl)
        if return_value is None:
            return_value = 'notfound'
    except Exception as e:
        print e
    if return_value == 'notfound': 
        write_content(cleanurl, shorturl='shorturl')
        shorturl = 'shorturl'
        return_value = read_content(cleanurl, shorturl)
    return_value = "YOUR SHORT URL IS:\t" + return_value + "\n"
    return Response(return_value, mimetype="text/plain")


#END POINT FOR REDIRECTION
@app.route('/<short_url>')
def reroute_url(short_url):
    ss = "".join([host,short_url])
    sl =(ss,)
    with sqlite3.connect('test3.db') as con:
        try:
            res = con.execute("SELECT LONGURL FROM Test2table WHERE SHORTURL= ?", sl)
            for x in res:
                redirect_url = 'https://' + x[0].decode('UTF-8')
            add_hits(short_url)
        except OperationalError:
            print 'unable to retrive long url'
    return redirect(redirect_url)


if __name__ == '__main__':
    db_create()
    app.run(debug=True)
    #read_all()
