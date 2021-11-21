import random
import os
from src.loggings import add_logger
file_path=os.path.join(os.getcwd(),'code.txt')
def generate_code():
    try:
        log=add_logger()
        number=str(random.randint(100000,200000))
        with open(file_path,'w') as f:
            f.write(number)
        log.log(f'generate_code method sucessfully run','generate_random_code_for_validation.log',1)
    except Exception as e:
        log.log(f'generate_code method could not run sucessfully error, {str(e)}','generate_random_code_for_validation.log',3)
        
def read_code():
    log=add_logger()
    try:
        with open(file_path,'r') as f:
            code=f.read()
        log.log(f'read_code method sucessfully run','generate_random_code_for_validation.log',1)
    except Exception as e:
        log.log(f'read_code method could not run sucessfully error, {str(e)}','generate_random_code_for_validation.log',3)    
    return code
