gvizlib
=======

A simple Python library to make charts from MySQL tables.  It is intended to run as CGI and will spit a JSON object which can you load from your JS.  See the examples directory for a few ways of using the script.

This library builds on top of the Google Visualization library available from here: https://code.google.com/p/google-visualization-python/

Once you've got that install this library will allow you easily spit out compatible JSON which can be loaded in to a Google chart from JS.

From your own script, import this gvizlib.
Print your content headers:
* print "Content-type: application/json"
* print 


Create a connection to the database:

* dataset = gvizlib.mysqlToJson('<server>','<dbname>','<username>','<password>','<table>')

Make a datatable:

* dataset.make_data_table(columns=["watts"])

Note that the colums are optional.  If you leave them out the script will automatically discover and include all columns.
The script will also attempt to convert your database datatypes in to compatible GViz data types.

Then you can populate the datatable:

* dataset.populate_data(sql)

to pull in all the data from the table, or specify the exact SQL query you want to use:

* sql = "SELECT "+column_names+" FROM "+dataset.table+" ORDER BY time DESC LIMIT 1"
* dataset.populate_data(sql)


then just print the dataset as JSON:

* print dataset.print_JSON()

and you're done.
