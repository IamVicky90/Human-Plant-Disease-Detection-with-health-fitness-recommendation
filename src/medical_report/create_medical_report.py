from src.mongo_db_ops.db_operations import mongo_db_atlas_ops
from docx import Document
import os
import uuid
import datetime
from src.loggings import add_logger
class medical_report_management:
    def __init__(self):
        pass
    def replace_string(self,filename,dic):
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
        except Exception as e:
            logger.log(f'Could not saved the file.docx file, error: {str(e)}','create_medical_report.log',level_number=3)
        return 1
    def generate_the_report(self,email,prediction_text):
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
