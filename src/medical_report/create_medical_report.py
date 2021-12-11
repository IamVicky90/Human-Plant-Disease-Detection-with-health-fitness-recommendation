from docx import Document
import os
def replace_string(filename,dic):
    doc = Document(filename)
    for key,val in dic.items():
        for en,p in enumerate(doc.paragraphs):
            if key in p.text:
                inline = p.runs
                if en<16 or en>22:
                    for i in range(len(inline)):
                            text = inline[i].text.replace(key, val)
                            inline[i].text = text
                    print( p.text)

    doc.save(os.path.join('src','medical_report_file'))
    return 1
dic={'Report_': 'Report: {report_number}',
    'First': 'First Name: {opipipoFirst Name }',
    'Last': 'Last Name: {opipipoLast Name }',
    'Address': 'Address: hdfs dsfkhhjsfd dkshjkfds dfsjkhkjdfs sdfjhkjfds dfsjkhfdkjshd fdshkhdfsjkhdf djfshsdjksd dsfhjfdhkdfsj dkjdfshdfs sdjfhfdjkdfs',
    'Postal': 'Postal Code: {opipipoLast Name }',
    'City': 'City: {opipipoLast Name }',
    'Country': 'Country Name: {opipipoLast Name }',
    'Email': 'Email: {opipipoLast Name }',
    'info_pat':'Disease by the model kdhjk dfskhkfd fdshkjfd dfhkjsdf dfshjhdf mdfhjdf dfhjshdf mdfhfjdf djfhjfd dmshkjsdf mdfhfsdh mdfhjfds',
    'Date':'{Date}: {56-67-90}'
    }
replace_string(os.path.join('src','medical_report_template','file.docx'),dic)