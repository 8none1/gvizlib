#!/usr/bin/python
#
#  A simple MySQL to Google Charts Visualization library.
#
# Will Cooke
#
# Version 0.01  -   Decemember 2011 -   First attempt
# Version 0.02  -   January 2012    -   Few bug fixes and more testing
# Version 0.03  -   January 2014    -   Fixed the matching of datatypes to the simplified Google equivs

import MySQLdb
import sys
import os
import re
import datetime
import time
import gviz_api

# Get gviz_api from here: 


#  This is a look up table between the common MySQL data types and the Google data types
GOOGLE_TYPES_TO_SQL_TYPES = {
    "string"    : ['char','varchar','text'],
    "number"    : ['tinyint','smallint','mediumint','int','bigint','decimal','float','double'],
    "boolean"   : ['bool','boolean'],
    "date"      : ['date'],
    "datetime"  : ['datetime','timestamp'],
    "timeofday" : ['time']
}

# Reverse the sense of GOOGLE_TYPES_TO_SQL_TYPES so we can find one from the other easily.
SQL_TYPES_TO_GOOGLE_TYPES = {}
for gtype, sqltypelist in GOOGLE_TYPES_TO_SQL_TYPES.items():
    for sqltype in sqltypelist:
        SQL_TYPES_TO_GOOGLE_TYPES[sqltype] = gtype


class mysqlToJson(object):
    def __init__(self,server, username, password, database, table):
        self.server = server
        self.username = username
        self.password = password
        self.database = database
        self.table = table
        self.cursor = self.dbConnect()
    
    def dbConnect(self):
        db = MySQLdb.connect(host=self.server, user=self.username, passwd=self.password, db=self.database)
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        return cursor
        
    def dbDisconnect(self):
        self.cursor.close()
        
    def get_column_names_to_google_data_types(self,columns=None):
        # We get the MySQL structure for the full table and create a dict containing the column name(or id) and the Google Data type
        # Getting the structure for the full table when you only want to use a subset isn't really a problem.  Just pass the colums
        # you care about in the sort order of the gvz, and leave the others out.
        # e.g. datatable.ToJSon(columns_order=("col1","col2","col3"),order_by="col2")
        """Convert the MySQL table structure in to a gviz schema definition
        Where gviz data types are one of "string", "number", "boolean", "date", "datetime" or "timeofday"."""
        if columns is None:
            # Describe the whole table
            query = "DESCRIBE "+self.table
        else:
            fields = ",".join(['"%s"' % x for x in columns])
            query =  "SHOW COLUMNS FROM "+self.table
            query += ' WHERE Field IN (' + fields +')'
        self.cursor.execute(query)
        tabledef = self.cursor.fetchall()
        self.col2type = {}
        for row in tabledef:
            colname = row['Field']
            definition = row['Type']
            # Strip things like (11) from INT
	    definition = definition.split("(")[0]
            self.col2type[colname] = SQL_TYPES_TO_GOOGLE_TYPES[definition]
        return self.col2type
    
    def make_data_table(self,columns=None):
        """Construct a Google DataTable based on the description of a SQL table."""
        self.col2typedict = self.get_column_names_to_google_data_types(columns)
        # col2type is now a dict {"fieldname": gtype, ...}
        list_of_field_tuples = self.col2typedict.items()
        self.dt = gviz_api.DataTable(list_of_field_tuples)
        
        
    def populate_data(self,sql=None):
        """Extract the data, row by row, and load it into the datatable"""
        if sql == None:
            # The default action is to return all columns limited to 500 rows
            column_names = ",".join(self.col2typedict.keys())
            query = "SELECT "+column_names+" FROM "+self.table+" LIMIT 500"
        if sql is not None:
            # We can override by passing in our own SQL.  Dangerous much?
            query = sql
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            this_row_values_tuple = []
            for column_name in self.col2typedict:
                data = row[str(column_name)]
                datatype = self.col2typedict[column_name]
                this_row_values_tuple.append(data)
            this_row_values_tuple = tuple(this_row_values_tuple)
            self.dt.AppendData([this_row_values_tuple])
           
    def print_JSON(self,cols=None,sort=None):
        self.dbDisconnect()
        if cols is None and sort is None:
            # both args are None
            return self.dt.ToJSon()
        elif cols is not None and sort is None:
            # cols is populated, sort is not
            if type(cols) is tuple:
                  return self.dt.ToJSon(columns_order=(cols))
            else: 
                  return self.dt.ToJSon()
        elif cols is None and sort is not None:
            # col is None sort is not
            return self.dt.ToJSon(order_by=sort)
        else:
            # both are populated
            return self.dt.ToJSon(columns_order=(cols),order_by=sort)
        


