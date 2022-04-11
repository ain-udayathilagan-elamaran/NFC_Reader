import os 
import json

class FileHandleR:
    def __init__(self,Main_path):
        self.Main_path =Main_path+"/"
        
    def read_from_file(self,FileName,permission):
        try:   
            with open(self.Main_path+FileName, permission) as outfile:
                kc=outfile.read()
                return True,kc.strip()
        except Exception as kc:
            return False,kc

    def Read_Json(self,Path,FileName,permission):
        try:   
            with open(Path+FileName, permission) as outfile:
                kc=outfile.read()
                data = json.loads(kc)
                PASSWORD=data["PASSWORD"]
                HOST=data["HOST"]
                TOPICPREFIX=data["TOPICPREFIX"]
                USERNAME=data["USERNAME"]
                return True,HOST,USERNAME,PASSWORD,TOPICPREFIX
        except Exception as kc:
            return False,kc



    def write_on_file(self,data_To_Write,FileName,permission):
        try:
            with open(self.Main_path+FileName, permission) as outfile:
                outfile.write(data_To_Write)
            return True
        except Exception as sd:
            return False
            print(sd)
            # DateTimeSetter(30)


    def T1_writter(self,T1,RTC_State,RTC_Time,Rpi_Time,Camera_Time,FileName,permission):
        try :
            change_log={
            "T1":T1 ,
            "T2":"",
            "RTC_State":RTC_State,
            "RTC_Time":RTC_Time,
            "Rpi_Time":Rpi_Time,
            "Camera_Time":Camera_Time
            }
            json_ob = json.dumps(change_log, indent = 4)
            with open(FileName, permission) as outfile:
                outfile.write(json_ob) 
                return True  
        except Exception as df:
            return False
            print(df)
            
            
    def T1_Reader(self,FileName,permission):
        try:
            with open(FileName, permission) as outfile:
                kc=outfile.read()
                data = json.loads(kc)
            # To_time=T2
            T1=data["T1"]
            RTC_State=data["RTC_State"]
            RTC_Time=data["RTC_Time"]
            Rpi_Time=data["Rpi_Time"]
            Camera_Time=data["Camera_Time"]
            
            return T1,RTC_State,RTC_Time,Rpi_Time,Camera_Time
        except Exception as d:
            print(d) 
            return False
        
    def Update_Config(self,File_Name,Backup_File_Name):#Not Used
        with open(Backup_File_Name, "r") as fl:
            with open(File_Name, "w") as f:
                f.write(fl.read())
            # f.close()
    
    def Config_Checker_Retrive(File_Name,permission,Backup_File_Name):
        try :
            if not os.path.exists(File_Name):#if file not available
                data= ("File Not found ")
                with open(Backup_File_Name, "r") as fl:
                    with open(File_Name, "w") as f:
                        f.write(fl.read())
                with open(File_Name, permission) as fl:
                    ConfigData = json.loads(fl.read())  
                    return True,ConfigData,data
            # with open(DT_File_Name,'r') as hh:
            #     k=len(hh.read())
            #     print(k)
                
            elif len(open(File_Name).read()) == 0 :#if file available and emty 
                data=("File is empty")
                with open(Backup_File_Name, "r") as fl:
                    with open(File_Name, "w") as f:
                        f.write(fl.read())
                with open(File_Name, permission) as fl:
                    ConfigData = json.loads(fl.read())  
                    return True,ConfigData,data
            else :
                data="Config file is available"
                with open(File_Name, permission) as fl:
                    ConfigData = json.loads(fl.read())  
                    return True,ConfigData,data
        except Exception as df :
            print(df)
            data=""
            return False,df,data