"""
Created on Sunday June 13 2021
@author: Neeraj

"""
from tkinter import*
try:
    import Tkinter as tk
except:
    import tkinter as tk
import tkinter as tk

from PIL import Image, ImageTk
from datetime import datetime
from time import sleep

from email.mime.multipart import MIMEMultipart  
from email.mime.base import MIMEBase  
from email.mime.text import MIMEText  
from email.utils import formatdate  
from email import encoders
import smtplib,ssl

import face_recognition
import numpy as np
import sqlite3
import pickle
import ctypes
import time
import cv2
import os
 
ctypes.windll.shcore.SetProcessDpiAwareness(1) # it increase the window clearity
root = Tk()
photo = PhotoImage(file = "icon/icon.png")
root.iconphoto(False, photo) # set the icon to the window
root.title('Smart Attendance System(author : Neeraj)')
#root.attributes('-fullscreen', True) # it turn screen in full mode

root.bind("<Escape>", exit) #press escape to exit window

root.geometry("1920x1080+-8+-8")
root['bg'] = 'light blue'

lbl=Label(root,text ="SMART ATTENDANCE SYSTEM",fg ='red2' , font =("times new roman", 70),bg='light blue')
lbl.place(x=100,y=10)

lbl1=Label(root,text ="Choose the options",fg ='dark green' , font =("times new roman", 40),bg='light blue')
lbl1.place(x=50,y=170)

lbl2=Label(root,text ="Enroll the faces and encode the faces",fg ='dark violet' , font =("times new roman", 30),bg='light blue')
lbl2.place(x=145,y=270)

lbl3=Label(root,text ="Start attendance",fg ='dark violet' , font =("times new roman", 30),bg='light blue')
lbl3.place(x=145,y=340)

lbl16=Label(root,text ="Reset all the things",fg ='dark violet' , font =("times new roman", 30),bg='light blue')
lbl16.place(x=145,y=410)


########################### mail ###########################################################
def send_an_email():
            me = '##write your mail id##'     # enter your email id
            toaddr = mail_id                  # email id of person to send the mail      
            subject = "college authority"     # write Subject
                      
            msg = MIMEMultipart()  
            msg['Subject'] = subject  
            msg['From'] = me  
            msg['To'] = toaddr  
            msg.preamble = "test "   
            msg.attach(MIMEText("Attendance"))
                      
            part = MIMEBase('application', "octet-stream")  
            part.set_payload(open("attendance_database.db", "rb").read())  
            encoders.encode_base64(part)  
            part.add_header('Content-Disposition', 'attachment; filename="attendance_database.db"')   # File name and format name
            msg.attach(part)  
                      
            try:  
                s = smtplib.SMTP('smtp.gmail.com', 587)  # Protocol
                s.ehlo()  
                s.starttls()  
                s.ehlo()  
                s.login(user = '#write your mail id#', password = '#write your mail id password#')  # User id & password
                s.send_message(msg)  
                s.sendmail(me, toaddr, msg.as_string())  
                s.quit()
                lbl14.destroy()
                btn9.destroy()
                
                         
            except smtplib.SMTPException: 
                    print ("Error")
 
###############################################################################################
                    

def setTextInput1():
    global mail_id,lbl4,btn9,lbl14
        
    if (mailid.get() == ""):
            print()
            
    else:    
        mail_id=mailid.get()
        mailid.delete(0, END)

        lbl14=Label(root,text ="Send the mail",fg ='red3' , font =("times new roman", 30),bg='light blue')
        lbl14.place(x=1265,y=880)

        btn9 = Button(root, text = 'Send',bg='yellow', bd = '10',command = send_an_email) # it create the send button to send the mail
        btn9.place(x=1200, y=880)
        
        

lbl11=Label(root,text ="Send database via mail",fg ='dark green' , font =("times new roman", 40),bg='light blue')
lbl11.place(x=1200,y=690)

lbl14=Label(root,text ="Enter email id",fg ='dark violet' , font =("times new roman", 30),bg='light blue')
lbl14.place(x=1200,y=760)

large_font=('Verdana',20)
mailid=Entry(root,width=15,font=large_font,fg = 'DarkOrange3') # this create entry box to write sender mail     
mailid.grid(row=0, column=1)
mailid.place(x=1500,y=762)
#mailid.focus()
    
btn3 = Button(root, text = 'Save',bg='yellow', bd = '10',command = setTextInput1) # this create submit button of entry box, it submit the mail
btn3.place(x=1500, y=810)



##################################### enroll the student using face capture ##################
def Start():
        face_encoding='face_encoding/'

        known_face_encodings = []
        known_face_names = []

        video_capture = cv2.VideoCapture(0)

        for filename in os.listdir(face_encoding): 
                        known_face_names.append(filename[:-4])
                        with open (face_encoding+filename, 'rb') as fp: # call the face encoding of the student inside face_encoding folder
                                known_face_encodings.append(pickle.load(fp)[0])
                    

        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        try:
                while True:
                    # Grab a single frame of video
                    ret, frame = video_capture.read()

                    # Resize frame of video to 1/4 size for faster face recognition processing
                    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                    rgb_small_frame = small_frame[:, :, ::-1]

                    # Only process every other frame of video to save time
                    if process_this_frame:
                        # Find all the faces and face encodings in the current frame of video
                        face_locations = face_recognition.face_locations(rgb_small_frame)
                        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                        face_names = []
                        
                        for face_encoding in face_encodings:
                            # See if the face is a match for the known face(s)
                            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                            name = "Unknown"
                              
                            # Or instead, use the known face with the smallest distance to the new face
                            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                            best_match_index = np.argmin(face_distances)
                            if matches[best_match_index]:
                                name = known_face_names[best_match_index]

                                conn = sqlite3.connect('attendance_database.db')
                                curs=conn.cursor()
                                curs.execute("SELECT college_id FROM student_table WHERE name ='%s' "%name)
                                records3 = curs.fetchall()
                                x=["Empty","Empty","Empty"]
                                for x in records3:
                                    print(x[0])

                                conn.commit()
                                curs.close()

                                curs=conn.cursor()
                                curs.execute("SELECT name FROM present_student_table WHERE name ='%s' "%name)
                                records3 = curs.fetchone()
                        
                                if records3:
                                    print()
                                else:                               
                                    now1=datetime.now()
                                    current_time=now1.strftime("%d-%m-%Y %I:%M%p")
                                    conn = sqlite3.connect('attendance_database.db')
                                    curs = conn.cursor()
                                    curs.execute('INSERT INTO present_student_table(college_id, name,present_date_time) values(? ,?, ? )',( x[0],name,current_time)) # insert the present student in the database
                                    conn.commit()
                                    curs.close()                               
                                            
                                    face_names.append(name)

                    process_this_frame = not process_this_frame

                    # Display the results
                    for (top, right, bottom, left), name in zip(face_locations, face_names):
                        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                        top *= 4
                        right *= 4
                        bottom *= 4
                        left *= 4

                        # Draw a box around the face
                        cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 4)

                        # Draw a label with a name below the face
                        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                        font = cv2.FONT_HERSHEY_DUPLEX
                        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                    # Display the resulting image
                    #cv2.resizeWindow("camera", 500, 500)
                    cv2.imshow('Video', frame)
                    cv2.moveWindow('Video', 1200, 160)

                    # Hit 'q' on the keyboard to quit!
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                    #if n == 'p':
                     break

        # Release handle to the webcam
        except KeyboardInterrupt:
          video_capture.release()
          cv2.destroyAllWindows()
###############################################################################################


          
def Capture():
    global lbl4,lbl5,lbl6,lbl7,lbl8,lbl9
    lbl4=Label(root,text ="Enter name of person",fg ='black' , font =("times new roman", 25),bg='light blue')
    lbl4.place(x=50,y=500)

    lbl5=Label(root,text ="Enter college id",fg ='black' , font =("times new roman", 25),bg='light blue')
    lbl5.place(x=50,y=550)

    lbl6=Label(root,text ="Enter batch ",fg ='black' , font =("times new roman", 25),bg='light blue')
    lbl6.place(x=50,y=600)

    lbl7=Label(root,text ="Enter department",fg ='black' , font =("times new roman", 25),bg='light blue')
    lbl7.place(x=50,y=650)

    lbl8=Label(root,text ="Capture the image for enroll",fg ='dark violet' , font =("times new roman", 30),bg='light blue')
    lbl8.place(x=145,y=765)
            

    
    def setTextInput():
        global name_id,c,d,j,lbl9,lbl10
        
        if (name.get() == "" and college_id.get() == "" and batch.get() == "" and department.get() == ""):
            print()
        
        else:    
            name_id=name.get()
            c=college_id.get()
            d=batch.get()
            j=department.get()
            
            name.delete(0, END)
            college_id.delete(0, END)
            batch.delete(0, END)
            department.delete(0, END)


    global name
    large_font=('Verdana',20)
    name=Entry(root,width=15,font=large_font,fg = 'DarkOrange3') # this create entry box to write name     
    name.grid(row=0, column=1)
    name.place(x=430,y=500)
    name.focus_set()
    
    global college_id
    college_id=Entry(root,width=15,font=large_font,fg = 'DarkOrange3')# this create entry box to write college id    
    college_id .grid(row=1, column=0)
    college_id .place(x=430,y=550)

    global batch
    batch=Entry(root,width=15,font=large_font,fg = 'DarkOrange3')# this create entry box to write batch      
    batch.grid(row=2, column=0)
    batch.place(x=430,y=600)
   
    global department
    department=Entry(root,width=15,font=large_font,fg = 'DarkOrange3')# this create entry box to write department     
    department.grid(row=3, column=0)
    department.place(x=430,y=650)
    
    global btn2
    btn2 = Button(root, text = 'save!',bg='yellow', bd = '12',command = setTextInput)# this button save student information 
    btn2.place(x=430,y=700)
    
    def Run():
        timer = int(5) # timer
        cap = cv2.VideoCapture(0) 
        while True: 
                            ret, img = cap.read() 
                            cv2.imshow('a', img)  
                            prev = time.time() 

                            while timer >= 0: 
                                            ret, img = cap.read() 
                                            font = cv2.FONT_HERSHEY_SIMPLEX 
                                            cv2.putText(img, str(timer), (200, 250), font, 7, (0, 255, 255), 4, cv2.LINE_AA) 
                                            cv2.imshow('a', img)
                                            cv2.moveWindow('Video', 1200, 160)
                                            cv2.waitKey(125) 
                                            cur = time.time()
                                            
                                            if cur-prev >= 1: 
                                                    prev = cur 
                                                    timer = timer-1

                            else: 
                                            ret, img = cap.read() 
                                            cv2.imshow('a', img)
                                            cv2.moveWindow('Video', 1200, 160)
                                            cv2.waitKey(1000) 
                                            cv2.imwrite('clicked_photo/'+ name_id +'.jpg', img)
                                            
                                            enroll_encoding=[]
                                            img_ = face_recognition.load_image_file('clicked_photo/'+ name_id +'.jpg')
                                            try:
                                               img_encoding = face_recognition.face_encodings(img_)[0]
                                               enroll_encoding.append(img_encoding)
                                            
                                               f=open('face_encoding/'+name_id+'.txt','w+')
                                            
                                               with open('face_encoding/'+name_id+'.txt','wb') as fp:
                                                    pickle.dump(enroll_encoding,fp)
                                               f.close

                                            
                                            except IndexError as e:
                                               print("dlib face detector couldn't detect a face in the image you passed in")
                                               print(e)
                                            conn = sqlite3.connect('attendance_database.db')   
                                            curs = conn.cursor()
                                            curs.execute('INSERT INTO student_table(college_id, name,batch,department) values(? ,?, ? ,?)',( c,name_id,d,j)) # this query insert student information to the student_table
                                            conn.commit()
                                            cap.release()

                                            ###################### this destroy the labels and buttons ########
                                            department.destroy()
                                            batch.destroy()
                                            college_id.destroy()
                                            name.destroy()
                                            btn2.destroy()
                                            btn5.destroy()
                                            
                                            lbl4.destroy()
                                            lbl5.destroy()
                                            lbl6.destroy()
                                            lbl7.destroy()
                                            lbl8.destroy()
                                            ##################################################################
                                            
                                            
                                            cv2.destroyAllWindows()
    global btn5                                      
    btn5 = Button(root, text = 'capture !',bg='yellow', bd = '10',command = Run) # this button help to enroll the face of the student
    btn5.place(x=50,y=765)

btn = Button(root, text = 'Click me !',bg='yellow', bd = '10',command = Capture) # this button enroll the student information to database 
btn.place(x=50, y=270)

btn1 = Button(root, text = 'Click me !',bg='yellow', bd = '10',command = Start)  # this button start face recognition to take attendance 
btn1.place(x=50, y=340)


############################## generate database ###################
def setTextInput2():
    global lbl18
    lbl18=Label(root,text ="Enter password",fg ='red3' , font =("times new roman", 30),bg='light blue')
    lbl18.place(x=148,y=910)
    
    global pass_word
    password=Entry(root,width=15,font=large_font,fg = 'DarkOrange3') #this create the entry box to enter the password,so i create the database   
    password.grid(row=2, column=0)
    password.place(x=480,y=910)
    password.focus()
 
    def setTextInput3():
        pass_word = password.get()
        if pass_word == "neeraj123": # from here you can change your password
            conn = sqlite3.connect('attendance_database.db')
            curs = conn.cursor()
            curs.execute("CREATE TABLE student_table(college_id int(20) not null,name text not null, batch text not null,department text not null,primary key(college_id),unique(college_id))")
            curs.execute("CREATE TABLE present_student_table(college_id int(20) not null,name TEXT not null,present_date_time datetime default CURRENT_TIMESTAMP)")
            password.destroy()
            lbl18.destroy()
            btn8.destroy()
        
        
    global btn8    
    btn8 = Button(root, text = 'Enter PSW',bg='yellow', bd = '10',command = setTextInput3)#press button causes password insert
    btn8.place(x=50, y=910)
######################################################################
                        
                   
lbl17=Label(root,text ="Generate database",fg ='dark violet' , font =("times new roman", 30),bg='light blue')
lbl17.place(x=165,y=840)
btn7 = Button(root, text = 'Generate DB',bg='yellow', bd = '10',command = setTextInput2)
btn7.place(x=50, y=840)


############################ destroy buttons and labels ######
def reset():
    department.destroy()
    batch.destroy()
    college_id.destroy()
    name.destroy()
    btn2.destroy()
    btn5.destroy()
                   
    lbl4.destroy()
    lbl5.destroy()
    lbl6.destroy()
    lbl7.destroy()
    lbl8.destroy()
    
    
btn6 = Button(root, text = 'reset all !',bg='yellow', bd = '10',command = reset) # this button destroy buttons and labels
btn6.place(x=50, y=410)
##########################################################


########################## it focus the entry box when i press the arrow button #### 
def previous_widget(event):
        event.widget.tk_focusPrev().focus()
        return "break"
root.bind_class("Entry", "<Up>",previous_widget)

def next_widget(event):
        event.widget.tk_focusNext().focus()
        return "break"
root.bind_class("Entry", "<Down>",next_widget)
###################################################################################

root.mainloop()
