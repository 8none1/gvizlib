#!/usr/bin/python

# Read the latest power readings as a JSON string compatible with the Google Visualization stuff
# http://code.google.com/apis/chart/interactive/docs/index.html

import gvizlib
import gviz_api


print "Content-type: application/json"
print 

dataset = gvizlib.mysqlToJson('server','database','user','password','table')
dataset.col2typedict = {"MinMax":"string","min":"number","max":"number"}
dataset.dt = gviz_api.DataTable(dataset.col2typedict.items())

sql = """SELECT "MinMax",MIN(temperature) AS min, MAX(temperature) AS max FROM readings"""
dataset.populate_data(sql)
print dataset.print_JSON(cols=("MinMax","min","max"))


