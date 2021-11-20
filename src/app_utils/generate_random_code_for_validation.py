import random
import os
file_path=os.path.join(os.getcwd(),'code.txt')
number=str(random.randint(100000,200000))
def generate_code():
    with open(file_path,'w') as f:
        f.write(number)
def read_code():
    with open(file_path,'r') as f:
        code=f.read()
    return code
