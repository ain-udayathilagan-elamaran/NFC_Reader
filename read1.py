import logging
import logging.config
import subprocess
import time

from Data import Details
from FileHand.File import FileHandleR
from Mqtt_Module.mqtt import mqtt_mod

username_mqtt=Details["username_mqtt"]
password_mqtt=Details["password_mqtt"]
mqtt_broker=Details["mqtt_broker"]
mqtt_port=Details["mqtt_port"]
Publish_Topic=Details["Publish_Topic"]
HeartBeat_Topic_Suffix=Details["HeartBeat_Topic_Suffix"]
Data_Topic_Suffix=Details["Data_Topic_Suffix"]
Main_Location=Details["Main_Location"]
HB_time=Details["HB_time"]
Main_Loop_Interval=Details["Main_Loop_Interval"]
MqTT=mqtt_mod(username_mqtt,password_mqtt,mqtt_broker,mqtt_port,Publish_Topic,HeartBeat_Topic_Suffix,Data_Topic_Suffix)
FileHandler=FileHandleR(Main_Location)
Program_Version=0.1
# Main_Loop_Interval=.2
# HB_time=60
HB_Mul=HB_time/Main_Loop_Interval
HB_Time_Interval=Main_Loop_Interval*HB_Mul


Er=0
C1=0

logging.config.fileConfig('./logging.conf')
logger = logging.getLogger()

def Get_IP_Address():
    c=0
    with open("/etc/dhcpcd.conf", 'r') as outfile:
        f=outfile.read()
        fdata=f.split()
        for i in fdata:
            if i =="eth0":
                c=1
            if i == "static" and c==1:
                c=2
            if "ip_address" in i and c==2 :
                ip_line=i[:-3]
                c=0
        IP_Address=ip_line.split('.')[-1]
        if len(IP_Address) <3:
            IP_Address='0{}'.format(IP_Address)
            return IP_Address

Device_ID=Get_IP_Address()


def MQtt_Publisher(Msg_To_Publish,EdgeID):
    MqTT_State,client=MqTT.MQTT_Connect()
    time.sleep(0.01)
    if MqTT_State:
        logger.info("Mqtt is {}_{}".format(str(MqTT_State),str(client)))
        pub_state,pub_error=MqTT.Publish_Data(client,EdgeID,Message=jsondata)
        logger.info("Publish is {}_{}".format(str(pub_state),str(pub_error)))
        MqTT.MQTT_Disconnect(client)
        MqTT_State=False
    else:
        logger.info(str(client))
        # MqTT_State,client=MqTT.MQTT_Connect()

def nfc_raw():
    global Er
    try :
        lines=subprocess.check_output("/usr/bin/nfc-poll", stderr=open('/dev/null','w'))
        return True,lines
    except Exception as F:
        Er=Er+1
        if Er < 5000:
            logger.error(str(F))
        return False,F

def read_nfc():
	state,lines=nfc_raw()
	if state:
		return lines

while True:
    
    time.sleep(Main_Loop_Interval)
    C1=1+C1
    if C1 <HB_Time_Interval:
        MqTT_State,client=MqTT.MQTT_Connect()
        HBjsondata='{{"Program_Version":{},"Time":"{}"}}'.format(Program_Version,time.strftime("%Y-%m-%dT%X"))
        if MqTT_State:
            MqTT.Publish_HeartBeat(client,EdgeId=Device_ID,Message=HBjsondata) 
            C1=0
    try:
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
    except Exception as ef:
        Er=Er+1
        if Er < 5000:
            logger.error("Error on Main while")
            logger.error(str(ef))
