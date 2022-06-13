import boto3
from src.mongo_db_ops.db_operations import mongo_db_atlas_ops
from docx import Document
import os
import uuid
import datetime
from src.loggings import add_logger
class medical_report_management:
    '''
    Class that responsible for creating the medical report
    '''
    def __init__(self):
        pass
    def replace_string(self,filename,dic):
        '''
        Replacing the string from the template to create the file according to the user
        args: 
            filename: Name of the template file.
            dic: dictionary to replace the desired words from the templates.
        '''
        try:
            logger=add_logger()
            doc = Document(filename)
            for key,val in dic.items():
                for en,p in enumerate(doc.paragraphs):
                    if key in p.text:
                        inline = p.runs
                        if en<16 or en>22:
                            for i in range(len(inline)):
                                    text = inline[i].text.replace(key, val)
                                    inline[i].text = text
            doc.save(os.path.join('src','medical_report_file','report.docx'))
            logger.log('Sucessfully saved the file.docx file','create_medical_report.log',level_number=1)
            self.add_medical_report_to_s3()
            logger.log('add_medical_report_to_s3 method run sucessfully','create_medical_report.log',level_number=1)
        except Exception as e:
            logger.log(f'Could not saved the file.docx file, error: {str(e)}','create_medical_report.log',level_number=3)
        return 1
    def generate_the_report(self,email,prediction_text):
        '''
        It will generate the report and extract information from mongo_db database
        email: email from which that you want to extract the information
        prediction_text: prediction text from the model
        '''
        logger=add_logger()
        report_number=uuid.uuid4()
        logger.log(f'email is {email}, prediction_text is {prediction_text} report_number is: {report_number}','create_medical_report.log',1)
        try:
            client=mongo_db_atlas_ops().get_mongo_db_connection()
            login_credentials=client['Human_and_Plant_Health_SDM']
            table=login_credentials['login_credentials']
            for row in table.find():
                if row['email']==email:
                    fname=row['fname']
                    city=row['city']
                    state=row['state']
                    zip=row['zip']
                    lname=row['lname']
                    lname=row['lname']
            today=datetime.date.today()
            date = today.strftime("%b-%d-%Y")
            dic={'Report_': f'Report #: {report_number}',
                'First': f'First Name: {fname}',
                'Last': f'Last Name: {lname}',
                'Address': 'Address: (No address Provided)',
                'Postal': f'Postal Code: {zip}',
                'City': f'City: {city}',
                'Country': f'Country Name: {state}',
                'Email': f'Email: {email}',
                'info_pat':f' {prediction_text}',
                'Date':f'Date: {date}'
                }
            self.replace_string(os.path.join('src','medical_report_template','file.docx'),dic)
            logger.log(f'Sucessfully executed the method generate_the_report','create_medical_report.log',level_number=1)
        except Exception as e:
            logger.log(f'Could not execute the method generate_the_report, error: {str(e)}','create_medical_report.log',level_number=3)
    def add_medical_report_to_s3(self):
        '''
        Responsible to add the medical_report_file to aws s3 bucket
        '''
        logger=add_logger()
        try:
            AWS_ACCESS_KEY_ID=os.environ.get('_AWS_ACCESS_KEY_ID')
            AWS_SECRET_ACCESS_KEY=os.environ.get('_AWS_SECRET_ACCESS_KEY')
            s3_client = boto3.client('s3',aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
            s3_client.upload_file('src/medical_report_file/report.docx', 'my-medical-report-docfile', 'file.docx', ExtraArgs={'ACL':'public-read'})
            logger.log(f'Sucessfully uploaded the doc file to s3 bucket','create_medical_report.log',level_number=1)
        except Exception as e:
            logger.log(f'Error while connecting to aws s3, error: {str(e)}','create_medical_report.log',level_number=3)
