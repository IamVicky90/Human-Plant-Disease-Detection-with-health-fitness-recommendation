import os
import pymongo
import hashlib
class mongo_db_atlas_ops:
    def __init__(self):
        pass
    def get_mongo_db_connection(self):
        '''Responsible for the connection with MongoDB Atlas'''
        user=os.environ.get('MONGO_USER')
        mongo_password=os.environ.get('MONGO_PASSWORD')
        return pymongo.MongoClient(f"mongodb+srv://{user}:{mongo_password}@cluster0.hpbfo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    def find_in_database(self,table_name,email,password)->bool:
        email_validation=table_name['login_credentials'].find({'email':str(email)})
        password_validation=table_name['login_credentials'].find({'password':password})
        if email_validation.count()>0:
            for item in email_validation:
                email_id=item.get('_id')
            email_validation_flag= True
        else:
            email_validation_flag= False
        if email_validation_flag:
            if password_validation.count()>0:
                for item in password_validation:
                    pass_id=item.get('_id')
                    if email_id==pass_id:
                        password_validation_flag= True
                        break
                    else:
                        password_validation_flag= False
                        
        else:
            password_validation_flag= False
        return email_validation_flag, password_validation_flag
    def insert_signup_credentials(self,fname,lname,email,password,city,state,zip):
        client=self.get_mongo_db_connection()
        login_credentials=client['Human_and_Plant_Health_SDM']
        table=login_credentials['login_credentials']
        result = hashlib.sha256(password.encode())
        table.insert_one({'fname':str(fname),'lname':str(lname),'email':str(email),'password':str(result.hexdigest()),'city':str(city),'state':str(state),'zip':str(zip)})
    def update_password(self,email,password):
        client=self.get_mongo_db_connection()
        login_credentials=client['Human_and_Plant_Health_SDM']
        table=login_credentials['login_credentials']
        email_validation=login_credentials['login_credentials'].find({'email':str(email)})
        for password_ in email_validation:
            old_password=password_['password']
        myquery = { "password": old_password }
        Result = hashlib.sha256(password.encode())
        newvalues = { "$set": { "password": Result.hexdigest() } }
        table.update_one(myquery, newvalues)
            