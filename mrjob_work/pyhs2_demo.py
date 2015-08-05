#coding=utf-8
__author__ = 'Carry lee'
import pyhs2
import cStringIO as stringIO

with pyhs2.connect(host='211.152.60.33',
                   port=10000,
                   authMechanism="PLAIN",
                   user='hadoop',
                   password='hadoop123',
                   database='default') as conn:
    with conn.cursor() as cur:
        #Show databases
        print cur.getDatabases()

        #Execute query
        cur.execute("select * from idatabase_collection_553dac8fb1752fa45f8b5d3d limit 3")

        #Return column info from query
        print cur.getSchema()

        #Fetch table results
        for i in cur.fetch():
            print i
