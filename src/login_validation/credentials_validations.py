import pymongo
import hashlib
import os
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
        '''Used to validate the funtion'''
        client=self.get_mongo_db_connection()
        login_credentials=client['Human_and_Plant_Health_SDM']
        email_validation=login_credentials['login_credentials'].find({'email':str(self.email)})
        password_validation=login_credentials['login_credentials'].find({'password':self.password})
        if email_validation.count()>0 and password_validation.count()>0:
            return True
        return False
    def get_mongo_db_connection(self):
        '''Responsible for the connection with MongoDB Atlas'''
        user=os.environ.get('MONGO_USER')
        mongo_password=os.environ.get('MONGO_PASSWORD')
        return pymongo.MongoClient(f"mongodb+srv://{user}:{mongo_password}@cluster0.hpbfo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")