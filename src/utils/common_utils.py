import os
from src import loggings
def create_directory(dirnames:list,exist_ok=True):
    '''
    args:
        dirnames: expected directory names with path in list
        exist_ok: will not raise except if directory already exists by default True
    '''
    log=loggings.add_logger()
    for dir in dirnames:
        try:
            os.makedirs(dir,exist_ok=exist_ok)
            with open(os.path.join(dir,'.gitkeep'),'w+') as f:
                pass
            log.log(f'directory {dir} sucessfully created by create_directory funtion','common_utils.log',1)
        except Exception as e:
            try:
                log.log(f'directory {dir} could not be created by create_directory funtion error, {str(e)}','common_utils.log',3)
            except Exception as NameError:
                log.log(f'{str(NameError)} while creating the directory by create_directory funtion error, {str(e)}','common_utils.log',3)
                