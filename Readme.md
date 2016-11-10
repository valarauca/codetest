Interface Scrapper
---

#Server:

This is an extremely simple web.py server. It is currently hosted natively. In python. This is less then ideal, but prefectly functional provided there are not THOUSANDS of clients hitting it daily. The server is currently in debug mode, with no error or 404 handling.

The _backend_ if you could call it that is a Sqlite3 database. Very little data is stored per client upload, so sqlite is a fine choice for DB. It prevents additional ORM/connection depedencies.

To run:

      $ git clone https://github.com/valarauca/codetest
      $ cd codetest/if_server/
      $ pip install web.py
      $ python2.7 app.py [PORT] 

That will create a locally hosted app. The app is required to be running
for the client to function. 

#Client:

Is a single python2.7 script. It used 1 external dependency `requests`. 

To run this

     $ git clone https://github.com/valarauca/codetest
     $ pip install requests
     $ cd codetest/if_client
     $ python2.7 if_client.py 'http://[where server is]:[Server Port]/upload'

The client supports both Windows and Linux. The operation is the same
on both systems. Compability between OS's is handled internally.

The server URL is a cli arg to allow for changes in backend provided they follow a general RESTful architecture.

The nature of a simple CLI tool like this means it is fairly trivial to
embedd within a scheduled task in windows

     location:
     	-where ever if_client.py is-

     execute:
     	c:\python27\python.exe

     arg:
     	if_client.py, 'url'


For Linux you can embedd the python script within a bash script. And save t
at bash script within `/etc/cron.daily`, `/etc/cron.weekly`, or
`/etc/cron.monthly` to run it at a regular schedule. 

#Tests:

Unit tests are listed in both `if_client/` and `if_server/` their file names start with `test_`. 

There are no full integration tests.


#DB Stuff:

If you dig into the server directory there is a simple sqlite repl. 

