#!/usr/bin/python

# Read the latest power readings as a JSON string compatible with the Google Visualization stuff
# http://code.google.com/apis/chart/interactive/docs/index.html

import gvizlib

print "Content-type: application/json"
print 

dataset = gvizlib.mysqlToJson('localhost','database','username','password','table')
dataset.make_data_table(columns=['time','temperature'])
column_names = ",".join(dataset.col2typedict.keys())
sql = "select time,CONVERT(avg(temperature),UNSIGNED) as temperature from readings where time > DATE_SUB(NOW(), INTERVAL 7 DAY) group by DATE(time),HOUR(time)"

dataset.populate_data(sql)

print dataset.print_JSON(cols=("time","temperature"))


