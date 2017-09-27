
import json
import paho.mqtt.client as mqtt
import urllib2

#ttn credentials
mqtt_server='eu.thethings.network'
mqtt_port=1883
mqtt_user='marco2017' #Username: Application ID
mqtt_pass= 'ttn-account-v2.jeXs0ZJ4tEn31rMu4Tkpgg-CfKMIDPZv7G9fyocOuyU'#Password: Application Access Key (base64).

application_id='marco2017'
device_id='marco01'
aport='7'

#emoncms credentials
apikey='05502b73a9151ff4be599c5fd3f0bbc4'



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


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")
    #client.subscribe("#")
    client.subscribe(application_id+'/devices/'+ device_id+ '/up')
    
def on_disconnect(client, userdata, rc):
    print "disconect"


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    #print "len" ,len(msg.payload)
    #print "data" ,msg.payload
    log_payload(msg.payload)

def log_payload(json_string):
    #json_string={"app_id":"marco2017","dev_id":"marco02","hardware_serial":"0000000000000002","port":7,"counter":25,"payload_raw":"AIDdQQ==","payload_fields":{"t":27.6875},"metadata":{"time":"2017-09-07T16:51:07.364340848Z","frequency":868.1,"modulation":"LORA","data_rate":"SF7BW125","coding_rate":"4/5","gateways":[{"gtw_id":"eui-b827ebfffeb52c5b","timestamp":641130131,"time":"2017-09-07T16:51:07.40716Z","channel":0,"rssi":-49,"snr":9.2,"rf_chain":1,"latitude":45.53392,"longitude":9.24047,"altitude":170}]}}
    parsed_json = json.loads(json_string)
    
    port=str(parsed_json['port'])
    node=str(parsed_json['dev_id'])
    
    fields_j=parsed_json['payload_fields']
    fields_s=json.dumps(fields_j)
    fields_s=fields_s.replace(' ','')
    fields_s=fields_s.replace('"','')    
    
    if port==aport:
        log_emoncms(fields_s, node, apikey)
   
client = mqtt.Client("py_client-mb",True,"my_user_data")
client.username_pw_set(mqtt_user,password=mqtt_pass)  
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect(mqtt_server, mqtt_port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()













