from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
import json
import os
import re

def pull_xml(file_name):
    input_file = 'docx/'+file_name
    output_file = 'docx/xml/'+file_name
    
    document = Document(input_file)
    
    resultTable:Table 
    headerFound = False
    
    for content in document.iter_inner_content():
        if(headerFound):
            if(isinstance(content, Table)):
                resultTable = content
                break
            continue
        
        if(isinstance(content, Paragraph)):
            if("Схема вида сведений" in content.text):
                headerFound = True

    text = ""
    header=""
    try:
        for paragraph in resultTable.rows[0].cells[0].paragraphs:
            text+=(paragraph.text + "\n")

        pattern = r"(«(\n|.)*»)"
    
        aggregated_text = ''
        for content in document.iter_inner_content():
            aggregated_text += content.text
            
            match = re.search(pattern, aggregated_text)
            if(match):
                name = match.group()
                break
    except Exception as e: 
        print("Error in file " + file_name + ":\n" + str(e))
        return file_name,'error'
    
    return name, text
        
dict = {}
for filename in os.listdir("docx/"):
    if(filename.endswith(".docx")):
        key, val = pull_xml(filename)
        dict[key] = val
        
with open("docx/json/xmls.json", 'w', encoding='utf-8') as f:
    s = json.dump(dict, f, ensure_ascii=False)