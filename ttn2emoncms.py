#!/usr/bin/env python
# bridge software that receives a PST from http integration and sends data to emomcms for logging
# on ttn use a similar URL to call this script http://myserver.com/ttn2emoncms.py?apikey=05502b73a9151ff4be599c5fd3f0bbc4&pwd=mypassword&aport=7


import cgitb
import cgi
import sys
import json
import urllib2
import os
cgitb.enable()


password='mypassword'

def log_emoncms(data_json,node_id,apikey):
    host='https://emoncms.org/input/post.json?'
    url=host+'apikey='+apikey+'&node='+node_id+'&json='+data_json
    print url
    try:
        ret=urllib2.urlopen(url, timeout=10)
        response=ret.read()
        print response
        #if not(response.startswith('ok')):
            #print response
    except Exception, e:
        print 'ERROR= '  + e.message


def get_p(storage,name):
    p1=storage.find(name)
    if p1>=0:
        p2=p1+len(name)+1
        p3=storage.find("&",p2)
        if p3==-1:
            p3=len(storage)
        sout=storage[p2:p3]
        return sout
    else:
        return ''

print "Content-type: text/plain\r\n\r\n"

qs=os.environ['QUERY_STRING']
#print qs

apikey=get_p(qs,'apikey')
pwd=get_p(qs,'pwd')
aport=get_p(qs,'aport')

post_data=sys.stdin.read()
#print post_data

parsed_json = json.loads(post_data)
port=str(parsed_json['port'])
node=str(parsed_json['dev_id'])
fields_j=parsed_json['payload_fields']

#print fields_j
             
fields_s=json.dumps(fields_j)
fields_s=fields_s.replace(' ','')
fields_s=fields_s.replace('"','')
#fields_s=fields_s.replace('\n','')
#fields_s=fields_s.replace('\r','')
#print fields_s


if (pwd==password):
    if((port==aport) and (apikey!='')):
        log_emoncms(fields_s, node, apikey)
else:
    print 'not authorized'
