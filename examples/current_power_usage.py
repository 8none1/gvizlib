#!/usr/bin/python

# Read the latest power readings as a JSON string compatible with the Google Visualization stuff
# http://code.google.com/apis/chart/interactive/docs/index.html

import gvizlib

print "Content-type: application/json"
print 

dataset = gvizlib.mysqlToJson('server','dbname','username','password','table')
dataset.make_data_table(columns=["watts"])
column_names = ",".join(dataset.col2typedict.keys())
sql = "SELECT "+column_names+" FROM "+dataset.table+" ORDER BY time DESC LIMIT 1"
dataset.populate_data(sql)

print dataset.print_JSON()


