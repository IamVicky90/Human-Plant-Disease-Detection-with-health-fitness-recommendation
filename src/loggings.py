import os
from src.utils.common_utils import create_directory
from datetime import datetime
class add_logger:
    def __init__(self) -> None:
        pass
    def log(self,message,filename,level_number=1):
        '''
        Funtion to take the logs for this project
        args: 
            message: Message that you want to write
            filename: Enter the filename to write logs
            level_number: Enter the level_number of the file
            expected 1,2,3
                1: For INFO
                2: For WARNING
                3.For ERROR
            by default, 1(INFO)
        '''
        if level_number==1: level='INFO'
        if level_number==2: level='WARNING'
        if level_number==3: level='ERROR'
        d=datetime.now()
        date=d.strftime('%d-%m-%y %H:%M:%S')
        with open(os.path.join(os.getcwd(),'Project_Logs',filename),'a') as f:
            f.write(f"{str(date)}\t{level}\t{str(message)}\n")
            f.close()