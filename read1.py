import subprocess
import time
from Mqtt_Module.mqtt import mqtt_mod
from Data import Details

username_mqtt=Details["username_mqtt"]
password_mqtt=Details["password_mqtt"]
mqtt_broker=Details["mqtt_broker"]
mqtt_port=Details["mqtt_port"]
Publish_Topic=Details["Publish_Topic"]
HeartBeat_Topic_Suffix=Details["HeartBeat_Topic_Suffix"]
Data_Topic_Suffix=Details["Data_Topic_Suffix"]

MqTT=mqtt_mod(username_mqtt,password_mqtt,mqtt_broker,mqtt_port,Publish_Topic,HeartBeat_Topic_Suffix,Data_Topic_Suffix)


Device_ID="NFC_Test1"

def MQtt_Publisher(Msg_To_Publish,EdgeID):
    MqTT_State,client=MqTT.MQTT_Connect()
    time.sleep(0.02)
    if MqTT_State:
        print(MqTT_State,client)
        pub_state,pub_error=MqTT.Publish_Data(client,EdgeID,Message=jsondata)
        print("ss is ",pub_state,pub_error)
        MqTT.MQTT_Disconnect(client)
        MqTT_State=False
        print("after df")
        # if not pub_state:
        #     MqTT_State,client=MqTT.MQTT_Connect()
    else:
        print("sduo thsdf jdod climnert ")
        print(client)
        # MqTT_State,client=MqTT.MQTT_Connect()

def nfc_raw():
	try :
		lines=subprocess.check_output("/usr/bin/nfc-poll", stderr=open('/dev/null','w'))
	# print(lines)
		print("Yeah bro data recived :)")
		return True,lines
	except Exception as F:
		print(F)
		return False,F
def read_nfc():
	state,lines=nfc_raw()
	if state:
		return lines

try:
	while True:
		time.sleep(.2)
		state,lines=nfc_raw()
		if state:
			myLines=lines.decode('utf-8')
			buffer=[]
			for line in myLines.splitlines():
				line_content=line.split()
				if line_content[0] =='UID':
					Uidd=line_content[2:]
					jsondata='{{"UUID_Len":{},"UUID":{},"Time":"{}"}}'.format(len(Uidd),Uidd,time.strftime("%Y-%m-%dT%X"))
					jsondata=jsondata.replace("'",'"')
					MQtt_Publisher(Msg_To_Publish=jsondata,EdgeID=Device_ID)
except KeyboardInterrupt:
        pass
    
