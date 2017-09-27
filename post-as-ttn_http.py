import httplib


host='myserver.com'

res='/ttn/ttn2emoncms2.py?apikey=05502b73a9151ff4be599c5fd3f0bbc4&pwd=mypassword&aport=7'

body='{"app_id":"marco2017","dev_id":"marco02","hardware_serial":"0000000000000002","port":7,"counter":25,"payload_raw":"AIDdQQ==","payload_fields":{"t1" : 27.6875,"t2" : 12.33},"metadata":{"time":"2017-09-07T16:51:07.364340848Z","frequency":868.1,"modulation":"LORA","data_rate":"SF7BW125","coding_rate":"4/5","gateways":[{"gtw_id":"eui-b827ebfffeb52c5b","timestamp":641130131,"time":"2017-09-07T16:51:07.40716Z","channel":0,"rssi":-49,"snr":9.2,"rf_chain":1,"latitude":45.53392,"longitude":9.24047,"altitude":170}]}}'

httpServ = httplib.HTTPConnection(host, 80)
httpServ.connect()

httpServ.request('POST', res, body)

response = httpServ.getresponse()
#if response.status == httplib.OK:
print response.read()


httpServ.close()