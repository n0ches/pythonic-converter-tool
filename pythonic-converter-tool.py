# -*- coding: utf-8 -*-
import csv
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from lxml import etree

#function to read csvFile
def readCSV(fileName):
    data=csv.reader(open(fileName))
    return data
#function to read csvFile

#function to take the first row of sample csv file. I will use
#this function for writing headers in xml to csv or json to csv convertions
def takeHeaders(csvFile):
    headers=[]
    data=readCSV(csvFile) #read all csv file and put it a variable
    count=0
    for row in data:
        if(count==0):#first row
            str=''.join(row)
            headers=str.split(";") #split first row and put the string into an array
            count+=1
        else:
            break
    return headers

#function to delete special characters  
def deleteTurkishCaharacters(str):
      str=str.lower()           #tolower does not work for big turkis characters(Ö,Ç) 
      str=str.replace("Ü","u")  #that's why, this method takes a bit long
      str=str.replace("ü","u")
      str=str.replace("ğ","g")
      str=str.replace("Ğ","g")
      str=str.replace("Ç","c")
      str=str.replace("ç","c")
      str=str.replace("Ş","s")
      str=str.replace("ş","s")
      str=str.replace("Ö","o")
      str=str.replace("ö","o")
      str=str.replace("İ","i")
      str=str.replace("I","i")
      str=str.replace("ı","i")
      return str
    
#function to delete special characters 

#function to convert csv file to xml file
def convertCSVtoXML(csvFile,xmlFile):
    csvData=csv.reader(open(csvFile)) #read all csvfile. I will take rows by using foreach
    departments = ET.Element("deparments")#this is root for xml file
    count=0
    for row in csvData:#for loop to take rows.
        if count==0:
            str=''.join(row)#row store the first row of csv(headers)
            str=deleteTurkishCaharacters(str)#turkish characters handling
            headers=str.lower().split(";")#turkish characters handling
            for i in range(len(headers)):
                headers[i]=headers[i].replace("̇","")#there are some errors for using lower method. I handle them
        else:
            str=''.join(row)#csv row is put into string for splittig process
            str=deleteTurkishCaharacters(str)
            attribs=str.split(";")#split row
            for i in range(len(attribs)):
                attribs[i]=attribs[i].replace("̇","")#lower error's handling
            for i in range(4):
                if(attribs[13]!=''):#this if statements is for score attribute.
                    point = ''.join(attribs[13])
                    point=point[:i]+','+point[i:]#score was not well format, it likes 4253657.
            if(count>0):                         #I edit score as 425,3657
                if(count==1):#I put datas for count>0 because first row of csv is not data, it is header
                    university=ET.Element("university")#element added as university. It is subelement of department(root)
                    university.set("name",attribs[1])#attribute of university is set
                    university.set("uType",attribs[0])#attribute of university is set
                    tempUniversity=attribs[1]       #I have to store the university name,
                if(tempUniversity != attribs[1]):   #beacuse if university name changes, xml element will end
                    departments.append(university)#university element appends into departments(root)
                    university=ET.Element("university")
                    university.set("name",attribs[1])
                    university.set("uType",attribs[0])         
                    tempUniversity=attribs[1]
                item=ET.Element("item")#element added as item. It is subelement of university
                item.set("id",attribs[3])#attribute of item is set
                item.set("faculty",attribs[2])#attribute of item is set

                #subelement of item is added

                #name element handling
                if((attribs[5] == "ingilizce") and (attribs[6] is '')):
                    ET.SubElement(item, "name", lang="en", second="No").text=attribs[4]#subelement of item is added
                elif((attribs[5] == "ingilizce") and (attribs[6] != '')):
                    ET.SubElement(item, "name", lang="en", second="Yes").text=attribs[4]
                elif((attribs[5] is '') and (attribs[6] is '')):
                     ET.SubElement(item, "name", lang="tr", second="No").text=attribs[4]
                elif((attribs[5] is '') and (attribs[6] != '')):
                    ET.SubElement(item, "name", lang="tr", second="Yes").text=attribs[4]
                #name element handling

                #period element handling
                ET.SubElement(item, "period").text=attribs[8]
                #period element handling

                #quota and spec element handling
                if(attribs[11] is ""):
                    ET.SubElement(item, "quota",spec="0").text=attribs[10]
                else:
                    ET.SubElement(item, "quota",spec=attribs[11]).text=attribs[10]
                 #quota and spec element handling

                 #field element handling
                ET.SubElement(item, "field").text=attribs[9]
                  #field element handling

                #score and order element handling
                if(attribs[12] is ""):
                    if(point is "-,"):
                        ET.SubElement(item, "last_min_score",order="0").text="0"
                    else:
                        ET.SubElement(item, "last_min_score",order="0").text=point
                else:
                    if(point is "-,"):
                        ET.SubElement(item, "last_min_score",order=attribs[12]).text="0"
                    else:
                        ET.SubElement(item, "last_min_score",order=attribs[12]).text=point
                #score and order element handling
                        
                #grant element handling
                if(attribs[7] is ''):
                    ET.SubElement(item, "grant")
                else:
                     ET.SubElement(item, "grant").text=attribs[7]
                #grant element handling

                #subelements of item are added

                university.append(item)#item append into university
        count+=1
    departments.append(university)#university append into department(root)

    #writing into xml file
    tree = minidom.parseString(ET.tostring(departments)).toprettyxml(indent="   ", encoding='utf-8')
    with open(xmlFile, "wb") as f:
        f.write(tree)
    #writing into xml file
        
#function to convert csv file to xml file

#function to convert xml file to csv file
def convertXMLtoCSV(xmlFile,csvFile):
    tree = ET.parse(xmlFile)#parsing xml file
    root = tree.getroot()#get root of xml

    #open csv file for writing
    csv_data = open(csvFile, 'w')
    f=csv.writer(csv_data,delimiter=';')
    #open csv file for writing

    #writing first row of csv file
    csv_headers=takeHeaders('DEPARTMENTS.csv')
    f.writerow(csv_headers)
    #writing first row of csv file

    
    for members in root.iter('university'):#root's subelement as 'university' is taken as members
        attribs=[]#store the rows attributes
        uType=members.get('uType')#get uType attribute of university element
        university=members.get('name')#get name attribute of university element
        for items in members.iter('item'):#university's subelement as 'item' is taken as items
            attribs=[]#store the rows attributes
            attribs.append(uType)#put the attributes into an array
            attribs.append(university)
            faculty=items.get('faculty')#get faculty attribute of item element
            attribs.append(faculty)
            Id=items.get('id') #get id attribute of item element
            attribs.append(Id)
            for names in items.iter('name'):#item's subelement as 'name' is taken as names
                program=names.text#get faculty name attribute of name element
                attribs.append(program)
                lang=names.get('lang')#get language name attribute of name element
                if(lang == "tr"):
                    attribs.append('')
                elif(lang == "en"):
                    attribs.append('ingilizce')
                    
                second=names.get('second')#get education type attribute of name element
                if(second is "Yes"):
                    attribs.append('ikinci ogretim')
                else:
                    attribs.append('')
                    
            for grants in items.iter('grant'):#get grant attribute of items element
                grant=grants.text #.text take the string 
                if(grant == "50"):
                    attribs.append("50")
                elif(grant == "25"):
                    attribs.append("25")
                elif(grant == "100"):
                    attribs.append("100")
                else:
                    attribs.append('')
            
            for periods in items.iter('period'):#get period attribute of items element
                period=periods.text
                attribs.append(period)

            for fields in items.iter('field'):#get field attribute of items element
                field=fields.text
                attribs.append(field)

            for quotas in items.iter('quota'):#get quota attribute of items element
                quota=quotas.text
                attribs.append(quota)
                spec=quotas.get('spec')#get grant attribute of quota element
                if(spec is "0"):
                    attribs.append('')
                else:
                    attribs.append(spec)

            for scores in items.iter('last_min_score'):#get score attribute of items element
                order=scores.get('order')#get order attribute of scores element
                if(order is "0"):
                    attribs.append('')
                else:
                    attribs.append(order)
                score=scores.text#get quota attribute of items element
                if(score == "-,"):
                    attribs.append('')
                else:
                    attribs.append(score)
            f.writerow(attribs)#writing the attribs array into csv as a row with ';' delimeter
    csv_data.close()
#function to convert xml file to csv file               

#function to convert csv file to json file        
def convertCSVtoJSON(csvFile,jsonFile):
    json_format=[]#array to store all json format 
    items=[]#array to store the items
    departments_arr=[] #array to store the departments.It has departmentDicts
    universityDict={} #dictionary to store a university
    facultyDict={}#dictionary to store a faculty
    departmentDict={}#dictionary to store a department
    csvData=csv.reader(open(csvFile))
    count=0
    for row in csvData:
        if count==0:# first row handling
            str=''.join(row)
            str=deleteTurkishCaharacters(str)
            headers=str.lower().split(";")
            for i in range(len(headers)):
                headers[i]=headers[i].replace("̇","")
             
        else:
            str=''.join(row)#row is put into string
            str=deleteTurkishCaharacters(str)#handling turkish characters
            attribs=str.split(";")
            for i in range(len(attribs)):
                attribs[i]=attribs[i].replace("̇","")
            for i in range(4):
                if(attribs[13]!=''):
                    point = ''.join(attribs[13])
                    point=point[:i]+','+point[i:]
            if(count>0):
                if(count==1):
                    uType=attribs[0]#take university type attribute
                    university=attribs[1]#take university namet attribute
                    faculty=attribs[2]
                    tempFaculty=faculty       #ı have to store faculty and university name
                    tempUniversity=university #beacuses if they change, json format should change.
                    universityDict['university name']=university
                    universityDict['uType']=uType
                if(tempUniversity != attribs[1]):
                    facultyDict['department']=departments_arr
                    items.append(facultyDict) #faculty dict put into items array
                    universityDict['items']=items
                    json_format.append(universityDict) #university put into json_format array
                    #clean the storage variables
                    universityDict={}
                    items=[]
                    facultyDict={}
                    departments_arr=[]
                     #clean the storage variables
                    uType=attribs[0]
                    university=attribs[1]
                    faculty=attribs[2]
                    tempFaculty=faculty
                    tempUniversity=university
                    universityDict['university name']=university
                    universityDict['uType']=uType
                if(tempFaculty != attribs[2]):
                    facultyDict['department']=departments_arr
                    items.append(facultyDict)
                    facultyDict={}
                    departments_arr=[]
                    faculty=attribs[2]
                    tempFaculty=faculty
                facultyDict['faculty']=faculty
                departmentDict={}

                #id is put into departmentDict
                if(attribs[3]==''):#id is put into departmentDict
                    departmentDict['id']="null"
                else:
                    departmentDict['id']= attribs[3]

                #name is put into departmentDict
                if(attribs[4]==''):
                    departmentDict['name']="null"
                else:  
                    departmentDict['name']= attribs[4]

                #lang is put into departmentDict   
                if(attribs[5] == "ingilizce"):
                    departmentDict['lang']= "en"
                elif(attribs[5] == ''):
                    departmentDict['lang']= "tr"

                #second is put into departmentDict  
                if(attribs[6] == ''):
                    departmentDict['second']= "No"
                elif(attribs[6] != ''):
                    departmentDict['second']= "Yes"

                #period is put into departmentDict
                if(attribs[8]==''):
                    departmentDict['period']="null"
                else:
                    departmentDict['period']= attribs[8]

                #period is put into departmentDict
                if(attribs[11]==''):
                    departmentDict['spec']="0"
                else:
                    departmentDict['spec']= attribs[11]   
                
                #quota is put into departmentDict
                if(attribs[10]==''):
                    departmentDict['quota']="null"
                else:
                    departmentDict['quota']= attribs[10]

                #field is put into departmentDict  
                if(attribs[9]==''):
                    departmentDict['field']="null"
                else:
                    departmentDict['field']= attribs[9]

                #score is put into departmentDict  
                if(point=='-,'):
                    departmentDict['last_min_score']="0"
                else:
                    departmentDict['last_min_score']=point

                #order is put into departmentDict
                if(attribs[12]==''):
                    departmentDict['last_min_order']="0"
                else:
                    departmentDict['last_min_order']= attribs[12]

                #grant is put into departmentDict   
                if(attribs[7] == ''):
                    departmentDict['grant']= "null"
                else:
                    departmentDict['grant']= attribs[7]
                    
                departments_arr.append(departmentDict)#department attribs put into department array
                    
        count=count+1
    #writing into json file, I use to sort_keys to write well formed but it does not work in vscode.
    with open(jsonFile,'w') as jsonWriter:
        jsonWriter.write(json.dumps(json_format, indent = 4, sort_keys=False))        
    #writing into json file
#function to convert csv file to json file

#function to convert json file to csv file
def convertJSONtoCSV(jsonFile,csvFile):
    #open csv file to write
    csv_data = open(csvFile, 'w')#open csv file to write
    f=csv.writer(csv_data, delimiter=';')
    csv_headers=takeHeaders('DEPARTMENTS.csv')
    f.writerow(csv_headers)
    #open csv file to write

    #open json file to read
    with open (jsonFile) as json_file:
        data=json.load(json_file)
    #open json file to read

    #json format like this, university->items->departments
    for i in range(len(data)):
        tempData=data[i]#take root
        university=tempData['university name']#take university name attribute
        uType=tempData['uType']#take university type attribute
        items=tempData['items']
        for j in range(len(items)):#take elements 
            tempItems=items[j]
            faculty=tempItems['faculty']#take faculty name attribute
            departments=tempItems['department']
            for k in range(len(departments)):#take department

                #taking department attributes
                attribs=[]
                tempDepartments=departments[k]

                if(tempDepartments['id']=="null"):
                    Id=''
                else:
                    Id=tempDepartments['id']

                if(tempDepartments['name']=="null"):
                    name=''
                else:
                    name=tempDepartments['name']
                    
                if(tempDepartments['lang']=="en"):
                    lang="ingilizce"
                elif(tempDepartments['lang']=="tr"):
                    lang=''

                if(tempDepartments['second']=="No"):
                    second=''
                elif(tempDepartments['second']=="Yes"):
                    second='ikinci ogretim'

                if(tempDepartments['period']=="null"):
                    period=''
                else:
                    period=tempDepartments['period']

                if(tempDepartments['spec']=="0"):
                    spec=''
                else:
                    spec=tempDepartments['spec']

                if(tempDepartments['quota']=="null"):
                    quota=''
                else:
                    quota=tempDepartments['quota']

                if(tempDepartments['field']=="null"):
                    field=''
                else:
                    field=tempDepartments['field']
                
                if(tempDepartments['last_min_score']=="0"):
                    last_min_score=''
                else:
                    last_min_score=tempDepartments['last_min_score']

                if(tempDepartments['last_min_order']=="0"):
                    last_min_order=''
                else:
                    last_min_order=tempDepartments['last_min_order']
                    
                if(tempDepartments['grant']=="null"):
                    grant=''
                else:
                    grant=tempDepartments['grant']
                #taking department attributes

                #appending the attributes    
                attribs.append(uType)
                attribs.append(university)
                attribs.append(faculty)
                attribs.append(Id)
                attribs.append(name)
                attribs.append(lang)
                attribs.append(second)
                attribs.append(grant)
                attribs.append(period)
                attribs.append(field)
                attribs.append(quota)
                attribs.append(spec)
                attribs.append(last_min_order)
                attribs.append(last_min_score)
                #appending the attributes 
                f.writerow(attribs) # writing attributes into csv file as a row
    csv_data.close()
#function to convert json file to csv file

#function to convert xml file to json file
def convertXMLtoJSON(xmlFile,jsonFile):
    tree = ET.parse(xmlFile)#parse xml
    root = tree.getroot()#take root
    json_format=[]#store the all json formet
    for members in root.iter('university'): #reach the university element from root
        #neccassery arrays and dicts for converting to json
        count=0
        items_arr=[]
        departments_arr=[]
        universityDict={}
        facultyDict={}
        departmentDict={}
         #neccassery arrays and dicts for converting to json
        
        uType=members.get('uType')#take univ type
        university=members.get('name')  #take univ name

        if(university != ''):
            universityDict['university name']=university
        else:
            universityDict['university name']="null"

        if(uType != ''):
            universityDict['uType']=uType
        else:
            universityDict['uType']="null"
            
        for items in members.iter('item'):#reaching the item

            if(count==0):
                faculty=items.get('faculty')
                tempFaculty=faculty
                if(faculty !=''):
                    facultyDict['faculty']=faculty
                else:
                    facultyDict['faculty']="null"                                    
            Id=items.get('id')
            if(Id !=''):
                departmentDict['id']=Id
            else:
                departmentDict['id']="null"

            for names in items.iter('name'):#reaching the name

                program=names.text
                if(program != ''):
                    departmentDict['name']=program
                else:
                    departmentDict['name']="null"

                lang=names.get('lang')
                if(lang == "tr"):
                    departmentDict['lang']="tr"
                elif(lang == "en"):
                    departmentDict['lang']="en"

                second=names.get('second')
                if(second is "Yes"):
                    departmentDict['second']="Yes"
                else:
                    departmentDict['second']="No"

            for periods in items.iter('period'):#reaching the period
                period=periods.text
                departmentDict['period']=period
                
            for quotas in items.iter('quota'):#reaching the quota and spec

                spec=quotas.get('spec')
                departmentDict['spec']=spec
                

                quota=quotas.text
                departmentDict['quota']=quota
                
            
            for fields in items.iter('field'):#reaching the fields
                field=fields.text
                departmentDict['field']=field
                
                     
            for scores in items.iter('last_min_score'):#reaching the score and order

                score=scores.text
                departmentDict['last_min_score']=score
                    
                order=scores.get('order')
                departmentDict['last_min_order']=order
            

            for grants in items.iter('grant'):#reaching the grant
                grant=grants.text
                if(grant != ''):
                    departmentDict['grant']=grant
                else:
                     departmentDict['grant']="null"              
            count+=1
            if(tempFaculty!=items.get('faculty')):#if faculty is chang
                    facultyDict['department']=departments_arr
                    departments_arr=[]#clear the department array
                    departments_arr.append(departmentDict)
                    departmentDict={}
                    items_arr.append(facultyDict)
                    facultyDict={}
                    faculty=items.get('faculty')
                    tempFaculty=faculty
                    if(faculty !=''):
                        facultyDict['faculty']=faculty
                    else:
                        facultyDict['faculty']="null"
            else:
                departments_arr.append(departmentDict)
                departmentDict={}
        facultyDict['department']=departments_arr
        items_arr.append(facultyDict)
        universityDict['items']=items_arr
        json_format.append(universityDict)
    #writing into json file, I use to sort_keys to write well formed but it does not work in vscode.
    with open(jsonFile,'w') as jsonWriter:
        jsonWriter.write(json.dumps(json_format, indent = 4, sort_keys=False))
     #writing into json file
#function to convert xml file to json file

#function to convert json file to xml file
def convertJSONtoXML(jsonFile,xmlFile):
    departments = ET.Element("deparments")#take root from json

    #open json for reading
    with open (jsonFile) as json_file:
        data=json.load(json_file)
    for i in range(len(data)):#for loop to reach attributes
        count=0
        tempData=data[i]
        university=tempData['university name']#take univ name
        uType=tempData['uType'] #take univ type
        items=tempData['items']#take items
        for j in range(len(items)):
            tempItems=items[j]
            faculty=tempItems['faculty']#take faculty name
            departments_json=tempItems['department']#take departments
            for k in range(len(departments_json)):
                attribs=[]
                tempDepartments=departments_json[k]

                if(tempDepartments['id']=="null"):#take id
                    Id=''
                else:
                    Id=tempDepartments['id']

                if(tempDepartments['name']=="null"):#take departments name
                    name=''
                else:
                    name=tempDepartments['name']
                    
                if(tempDepartments['lang']=="en"):#take lang
                    lang="ingilizce"
                elif(tempDepartments['lang']=="tr"):
                    lang=''

                if(tempDepartments['second']=="No"):#take education type
                    second=''
                elif(tempDepartments['second']=="Yes"):
                    second='ikinci ogretim'

                if(tempDepartments['period']=="null"):#take period
                    period=''
                else:
                    period=tempDepartments['period']

                spec=tempDepartments['spec']#take spec

                if(tempDepartments['quota']=="null"):#take quota
                    quota=''
                else:
                    quota=tempDepartments['quota']

                if(tempDepartments['field']=="null"):#take field
                    field=''
                else:
                    field=tempDepartments['field']
                
                last_min_score=tempDepartments['last_min_score']#take score

                last_min_order=tempDepartments['last_min_order']#take order                    

                if(tempDepartments['grant']=="null"):#take grant
                    grant=''
                else:
                    grant=tempDepartments['grant']                
    
                #appending the attributes
                attribs.append(uType)
                attribs.append(university)
                attribs.append(faculty)
                attribs.append(Id)
                attribs.append(name)
                attribs.append(lang)
                attribs.append(second)
                attribs.append(grant)
                attribs.append(period)
                attribs.append(field)
                attribs.append(quota)
                attribs.append(spec)
                attribs.append(last_min_order)
                attribs.append(last_min_score)
                #appending the attributes
                if(count==0):
                    university=ET.Element("university")
                    university.set("name",attribs[1])
                    university.set("uType",attribs[0])
                    count+=1
                #putting attribs array into xml elements
                item=ET.Element("item")
                item.set("id",attribs[3])
                item.set("faculty",attribs[2])
                if((attribs[5] == "ingilizce") and (attribs[6] is '')):
                    ET.SubElement(item, "name", lang="en", second="No").text=attribs[4]
                elif((attribs[5] == "ingilizce") and (attribs[6] != '')):
                    ET.SubElement(item, "name", lang="en", second="Yes").text=attribs[4]
                elif((attribs[5] is '') and (attribs[6] is '')):
                     ET.SubElement(item, "name", lang="tr", second="No").text=attribs[4]
                elif((attribs[5] is '') and (attribs[6] != '')):
                    ET.SubElement(item, "name", lang="tr", second="Yes").text=attribs[4]
                ET.SubElement(item, "period").text=attribs[8]
                ET.SubElement(item, "quota",spec=attribs[11]).text=attribs[10]
                ET.SubElement(item, "field").text=attribs[9]
                ET.SubElement(item, "last_min_score",order=attribs[12]).text=attribs[13]
                if(attribs[7] is ''):
                    ET.SubElement(item, "grant")
                else:
                     ET.SubElement(item, "grant").text=attribs[7]
                 #putting attribs array into xml elements
                university.append(item)
        departments.append(university)
    #writing
    tree = minidom.parseString(ET.tostring(departments)).toprettyxml(indent="   ", encoding='utf-8')
    with open(xmlFile, "wb") as f:
        f.write(tree)
     #writing
#function to convert json file to xml file

#function to validate xml file
def validate(xmlFile,xsdFile):
    doc = etree.parse(xmlFile)
    root = doc.getroot()
    xmlschema_doc = etree.parse(xsdFile)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    doc = etree.XML(etree.tostring(root))
    validation_result = xmlschema.validate(doc)
    if(validation_result == True):
        print("Validation result is: ",validation_result)
        print("XSD validation is completed")
    else:
        print("Validation result is: ",validation_result)
        print("XSD validation is completed")
    xmlschema.assert_(doc)
#function to validate xml file

#menu method
def menu():
    print("      ###  WELCOMTE TO 'Pythonic Converter Tool'  ###")
    flag=True
    while(flag):
        print("\n")
        print(" 1) Enter command line")
        print(" 2) Help page")
        print(" 3) Exit")
        menuInput=input()
        if(menuInput is '1'):
            print("\n Enter commdan line: ")
            inputLine=input()
            split=inputLine.split(" ")
            pySplit=split[1].split(".")
            inputFile=split[2]
            outputFile=split[3]
            convertType=split[4]
            #wrong input handling
            if(split[0] !="python"):
                print("Wrong command line. Please enter command line again!")
                continue
            if(pySplit[1] != "py"):
                print("Wrong source file format. Please enter command line again!")
                continue
            #wrong input handling
            if(convertType is '1'):
                inputFormat=inputFile.split(".")
                outputFormat=outputFile.split(".")
                #wrong input handling
                if(inputFormat[1] != 'csv'):
                    print("Wrong input file format. It must be .csv file")
                elif(outputFormat[1] != "xml"):
                    print("Wrong output file format. It must be .xml file")
                elif(inputFormat[1] != "csv" and outputFormat[1] != "xml"):
                    print("Wrong input output file format. They must be .csv and .xml file")
                #wrong input handling
                else:
                    convertCSVtoXML(inputFile,outputFile)
                    print("CSV to XML convertion is completed!")
            elif(convertType is '2'):
                inputFormat=inputFile.split(".")
                outputFormat=outputFile.split(".")
                if(inputFormat[1] != "xml"):
                    print("Wrong input file format. It must be .xml file")
                elif(outputFormat[1] != "csv"):
                    print("Wrong output file format. It must be .csv file")
                elif(inputFormat[1] != "xml" and outputFormat[1] != "csv"):
                    print("Wrong input output file format. They must be .xml and .csv file")
                else:
                    convertXMLtoCSV(inputFile,outputFile)
                    print("XML to CSV convertion is completed!")
            elif(convertType is '3'):
                inputFormat=inputFile.split(".")
                outputFormat=outputFile.split(".")
                if(inputFormat[1] != "xml"):
                    print("Wrong input file format. It must be .xml file")
                elif(outputFormat[1] != "json"):
                    print("Wrong output file format. It must be .json file")
                elif(inputFormat[1] != "xml" and outputFormat[1] != "json"):
                    print("Wrong input output file format. They must be .xml and .json file")
                else:
                    convertXMLtoJSON(inputFile,outputFile)
                    print("XML to JSON convertion is completed!")
            elif(convertType is '4'):
                inputFormat=inputFile.split(".")
                outputFormat=outputFile.split(".")
                if(inputFormat[1] != "json"):
                    print("Wrong input file format. It must be .json file")
                elif(outputFormat[1] != "xml"):
                    print("Wrong output file format. It must be .xml file")
                elif(inputFormat[1] != "json" and outputFormat[1] != "xml"):
                    print("Wrong input output file format. They must be .json and .xml file")
                else:
                    convertJSONtoXML(inputFile,outputFile)
                    print("JSON to XML convertion is completed!")
            elif(convertType is '5'):
                inputFormat=inputFile.split(".")
                outputFormat=outputFile.split(".")
                if(inputFormat[1] != "csv"):
                    print("Wrong input file format. It must be .csv file")
                elif(outputFormat[1] != "json"):
                    print("Wrong output file format. It must be .json file")
                elif(inputFormat[1] != "csv" and outputFormat[1] != "json"):
                    print("Wrong input output file format. They must be .csv and .json file")
                else:
                    convertCSVtoJSON(inputFile,outputFile)
                    print("CSV to JSON convertion is completed!")
            elif(convertType is '6'):
                inputFormat=inputFile.split(".")
                outputFormat=outputFile.split(".")
                if(inputFormat[1] != "json"):
                    print("Wrong input file format. It must be .json file")
                elif(outputFormat[1] != "csv"):
                    print("Wrong output file format. It must be .csv file")
                elif(inputFormat[1] != "json" and outputFormat[1] != "csv"):
                    print("Wrong input output file format. They must be .json and .csv file")
                else:
                    convertJSONtoCSV(inputFile,outputFile)
                    print("JSON to CSV convertion is completed!")
            elif(convertType is '7'):
                inputFormat=inputFile.split(".")
                outputFormat=outputFile.split(".")
                if(inputFormat[1] != "xml"):
                    print("Wrong input file format. It must be .xml file")
                elif(outputFormat[1] != "xsd"):
                    print("Wrong output file format. It must be .xsd file")
                elif(inputFormat[1] != "xml" and outputFormat[1] != "xsd"):
                    print("Wrong input output file format. They must be .xml and .xsd file")
                else:
                    validate(inputFile,outputFile)
                    
            else:
                print("Wrong type. Please enter command line again!")
                continue
        elif(menuInput is '2'):
            help()
        elif(menuInput is '3'):
             flag=False
    print("Goodbye!")
    exit()
#menu method    

def help():
    print("\n\t\t ## HELP PAGE ##\n")
    print("o The tool takes command line arguments according to the formats you want to convert",
             "between them. A typical command line usage is as follows:")
    print("\n\t python <filename> <input file> <output file/xsd file> <type>")
    print("\n type -> 1=CSV to XML,",
          "\n\t 2=XML to CSV,",
          "\n\t 3=XML to JSON,",
          "\n\t 4=JSON to XML,",
          "\n\t 5=CSV to JSON,",
          "\n\t 6=JSON to CSV,",
          "\n\t 7=XML validates with XSD")
    print("\no The sample command line usage converting from XML to JSON as follows:")
    print("\n\tpython student_id.py test.xml test.json 3\n")

menu()


