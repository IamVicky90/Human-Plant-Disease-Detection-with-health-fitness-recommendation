import hashlib
from src.mongo_db_ops.db_operations import mongo_db_atlas_ops
class user_validation:
    def __init__(self,email,password):
        '''This class is for user Authentication when he or she tries to login
        args:
            email: email of the user
            password: password of the user
        '''
        self.email = email
        self.password = self.encrypt_password(password)
    def encrypt_password(self,password)->str:
        '''
        This funtion is used to encrypt the password of the user.
        args: 
            password: password of the user
        '''
        result = hashlib.sha256(password.encode())
        return str(result.hexdigest())
    def validate_password_and_email(self)->bool:
        '''Used to validate the password and email'''
        mongo_conn=mongo_db_atlas_ops()
        client=mongo_conn.get_mongo_db_connection()
        login_credentials=client['Human_and_Plant_Health_SDM']
        return mongo_conn.find_in_database(login_credentials,str(self.email),str(self.password))
        
    