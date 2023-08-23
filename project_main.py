import streamlit as st
import pandas as pd
import numpy as np
import os
import cv2
import pytesseract                         
from pytesseract import Output
import re
import csv
import mysql.connector
import matplotlib.pyplot as plt 
from PIL import Image



code = conn=mysql.connector.connect(host='localhost',user="root",password="Password@123",database="dlproject") 
mycursor=conn.cursor()

mycursor.execute("SELECT Pic FROM task")

data=mycursor.fetchall()

print(data)
conn.close() 


lst=[]
for i in data:
    lst.append(list(i))

lst1=[]
for i in lst:
    for j in i:
     lst1.append(j)
print(lst1)

conn=mysql.connector.connect(host='localhost',user="root",password="Password@123",database="dlproject")  
mycursor=conn.cursor()

mycursor.execute("SELECT Name FROM task")
data1=mycursor.fetchall()
print(data1)
conn.close()

lst=[]
for i in data1:
    lst.append(list(i))

class_name=[]
for i in lst:
    for j in i:
     class_name.append(j)
print(class_name)



st.title("Aadhaar Detection")
text_input = st.text_input(
        "Enter your name 👇")
if text_input:
        st.write("You entered: ", text_input)
     
# class_name=['Vishnupriya S','Vishal V','Aleesha Thomas']
# name_of_aadar=input("enter your name:")


        if text_input not in class_name:
            st.write("No Match")
            
            option = st.selectbox('Do you need to add your aadar?',
                ('select','YES','NO'))

            
            if option == 'YES':
              st.title("Upload Your Aadhaar Here")
              uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
              if uploaded_file is not None:
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Uploaded Image", use_column_width=True)
                    st.write("Image dimensions: {} x {}".format(image.width, image.height))

                    file_path = os.path.join(os.getcwd(), uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.read())
                    st.success("Image saved successfully!")

                    conn=mysql.connector.connect(host='localhost',user="root",password="Password@123",database="dlproject")  
                    mycursor=conn.cursor()

                    sql = "INSERT INTO task(id,Name,Pic) VALUES(%s,%s,%s)"
                    values=(11,text_input,file_path)

                    mycursor.execute(sql,values)
                    conn.commit()
                    conn.close()

            if option == 'NO':
                    st.write("Thank You !")
            




        if text_input in class_name:
            ind=class_name.index(text_input)
            img=cv2.imread(f'{lst1[ind]}') 
            image_data = pytesseract.image_to_data(img,output_type=Output.DICT)
            n_boxes = len(image_data['text'])

                
                        
        #  print(image_data['conf'])
        #  print(image_data['text'])

            aadar_pattern1="^\d{12}$"
            aadar_pattern="^\d{4}$"
            date_pattern = '^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/(19|20)\d\d$'
            date_pattern1= '^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$'
            # date_pattern2='^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'
            a=""
            for k in range(n_boxes):
                    if re.match(aadar_pattern,image_data['text'][k]) or re.match(aadar_pattern1,image_data['text'][k]):
                            
                        if image_data['conf'][k]>50:

                            x,y,w,h = image_data['left'][k],image_data['top'][k],image_data['width'][k],image_data['height'][k]
                                    
                            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),thickness=3)

                        aadar_num=image_data['text'][k]
                        b=str(aadar_num)
                        a=' '.join([a,b])

            for k in range(n_boxes):
                    if re.match(date_pattern,image_data['text'][k]) or re.match(date_pattern1,image_data['text'][k]):

                        if image_data['conf'][k]>50:

                            x,y,w,h = image_data['left'][k],image_data['top'][k],image_data['width'][k],image_data['height'][k]
                                    
                            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),thickness=3)


                        dob=image_data['text'][k]           

            for k in range(n_boxes):
                    if image_data['text'][k] == 'Female' or image_data['text'][k] == 'Male' or image_data['text'][k]=='MALE' or image_data['text'][k]=='FEMALE' :
                        if image_data['conf'][k]>50:

                            x,y,w,h = image_data['left'][k],image_data['top'][k],image_data['width'][k],image_data['height'][k]
                                    
                            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),thickness=3)

                        sex=image_data['text'][k]  

                    

            print(dob)
            print(sex)
            # print(aadar_num)
            print(a)

            col1, col2 ,col3= st.columns(3)
            with col1:
                st.write('dob is:',dob)
            with col2:
                st.write('gender is:',sex)
            with col3:
                st.write('aadar_num is:',a)

            conn=mysql.connector.connect(host='localhost',user="root",password="Password@123",database="dlproject")  
            mycursor=conn.cursor()

            sql = "INSERT INTO aadhar_details(name,dob,sex,aadhar_no) VALUES(%s,%s,%s,%s)"
            values=(text_input,dob,sex,a)

            mycursor.execute(sql,values)
            conn.commit()
            conn.close()



            cv2.imshow('img',img)
            cv2.waitKey()
            cv2.destroyAllWindows()
                

