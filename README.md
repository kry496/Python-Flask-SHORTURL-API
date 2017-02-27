# Python-Flask-SHORTURL-API

#ABOUT:

    HTTP-based RESTful API for managing Short URLs and redirecting 
    Generate Short URL from Long Url < 1:1 uniqueness is maintained>
    Redirect when short URL is entered on the browser
    

#BREAKDOWN
    Maintain Idempotency for all requests.
    The SHORT URL and LONG URL have a 1:1 relationship.
    When a LONG URL is in the body of the POST request, the corresponding SHORT URL should be returned.
    When a SHORT URL is argument of query string in a GET request, access time stats data should be returned.
    When SHORT URL is entered in the browser, redirection should be immediate.
    Store data in a database to meet the persistence requirements.

#SYSTEM COMPONENTS:
    One Ubuntu 16.04.1 LTS Virtual Machine with 8 GB of RAM.
    Python 2.7 (Virtual Environment).
    A lightweight Python web framework – FLASK.
    Native Database Included with Python -- SQLite.
    Optional RESTCLIENT browser plugin for testing API End Points with GET and POST requests.    
    
    
#FLASK:

    Web Framework for exposing end points as app routes.
    End Points are not named in /api/version/<> format for convenience.
    POST Requests: http://localhost:5000/addurl
    GET Requests: http://localhost:5000/getstats
    URL REDIRECTION: http://localhost:5000/<Short_url>
   
# DATABASE SQLite:

    Lightweight and natively available, no setup or installation is required.
        Sqlite3 module part of the python standard library is used for connections and executions.
        Making a connection will create the database, if it doesn’t exist.
        Super easy exception handling.
        Can handle up to 400K to 500K HTTP requests per day.
    Tuple loading:
        Followed best practice and loaded the data into a tuple before using it for query operations.
    Foreign Key constraints:
        Sqlite3 Database should be pre-compiled to support foreign key constraints.
        Pre-complied Database will restrict Database deletion and recreation.
        Work around is to explicitly set it for every connection. [principle followed]
    Date/Time data types and functions:
        Easy to record timestamp for each SHORT URL retrieval.
        Easy to filter and count access times based on stipulated intervals.
    Database Schema:
        Table One: Contains INTEGER PRIMARY KEY, LONGURLs and SHORTURLs.
        Table Two: Contains INTEGER PRIMARY KEY, ShortID which references Table One’s Primary Key (Foreign Key
        Constraint), TIMESTAMP for each redirect request.
        Table One has a ONE: MANY relationship with Table Two.
        To sum up, this foreign key ensures that the stats in Table Two have a corresponding SHORT URL in Table One.

#Short_url Module:

    External module, Python 2 and Python3 compatible.
    Integer to SHORT URL encoder/decoder.
    Primary keys are unique, best fit for this purpose.
    Custom SHORTURL generator based on bit shuffling approach, can customize output length and block size.
    Timestamp insertions per SHORT URL access are dependent on the encoder/decoder functions as well.

#WORKFLOW FOR POST REQUEST:

    POST REQUEST with LONGURL;
        ACCEPT PLAINTEXT INPUT;
        REMOVE THE SCHEME from the LONGURL;
        VALIDATE IF URL PRESENT IN DATABASE;
    IF PRESENT;
        RETURN SHORTURL;
    IF NOT PRESENT;
        STORE IN DATABASE;
        FETCH PRIMARY KEY ID;
        ENCODE the INTEGER ID (PK) to GENERATE SHORTURL;
        RETURN SHORTURL;

#SOME KEY INFO ABOUT THE POST REQUEST:
    
    Content-Type is Plain/Text: Easy to Make requests.
    Difference in Scheme of the URL aka <http or https or blank> won’t result in a different SHORTURL.
    Repeated POST requests with same URL will always return same SHORT URL; Once generated its unique.
    The system is not capable of treating the URLs with and without the WWW as same, it will be treated as unique URLs as
    its part of the domain segment of the URL.
    Compiling REGULAR EXPRESSIONs to fulfil this would need more testing to ensure URL integrity.
    Non-Working URLS when entered, will result in 404 error on the browsers during redirection to allow graceful end
    point behavior.


#WORKFLOW FOR GET REQUEST:
    
    GET REQUEST with SHORTURL as QUERY PARAMETER STRING on URL;
        READ SHORTURL;
    DECODE URL INTO PRIMARY KEY ID;
    SELECT TIMESTAMPS RELATED TO PRIMARY KEY ID;
    FILTER & COUNT TIMESTAMPS PER TIME INTERVAL; (24hrs, 1 week, etc.)
       RETURN VALUES;

#SOME KEY INFO ABOUT THE GET REQUEST:
    
    Content-Type is Plain/Text: Easy to read.
    Unregistered/Invalid SHORTURLs will return the result as zero hits or page not found to ensure graceful behavior.

# WORKFLOW FOR REDIRECT:
    
    ACCEPT REDIRECT REQUEST; on FLASK APP ROUTE <single variable based route to accept any SHORTURL>
    READ SHORTURL;
    RETRIVE CORRESPONDING LONGURL;
    ADD URL SCHEME;
    REDIRECT; <via FLASK’s built in “redirect(<url>)” function>
    RECORD TIME STAMP; < for maintaining Access stats>
    
#SOME KEY INFO ABOUT THE REDIRECT:
    
    Invalid URLS when registered via POST request, will result in 404 error upon redirect to allow graceful behavior.

#FUTURE CONSIDERATIONS:
    
    Reduce to single Database connection when app starts to further optimize performance.
    Port to full SQL DB instances to support foreign key constraints and overcome other limitations if needed.
    Build Database object model and use Flask-SQLAlchemy extensions.
    Change Data presentation format to JSON.
    Python 3 portability.
    Remove String Concatenation operations; currently in use to optimize raw data format responses.
    Set Default values for DATABASE COLUMNS; less clutter in the code;
    Incorporate Flask -testing module for testing the application.
    Validate URL before inserting into database.
    Better naming convention for API end points.
    Better naming conventions for variables, tables etc. to understand workflow.
