'''If you are running this program, make sure yoou install the names and tabulate       
module and make sure to add your user, password and database name 
'''
#PLEASE READ THE ABOVE COMMENT


import mysql.connector as m
con=m.connect(host='localhost', user='root', passwd='root123',database='root')

if con.is_connected():
    print("connected")
cursor=con.cursor()
import sys
import names
import random
from tabulate import tabulate

###################################################################################################
def hospital(): #creating a table with random values


    cursor.execute('create table hospital(Patient_no int(5) not null primary key,name varchar(30),room_number varchar(10),Diagnosis varchar(25), requirement varchar(25),Days_admitted int(3),contact_number varchar(20), Email varchar(50))')
    print("hospital table created")
    print('please wait inserting values')   

    def patientname():
        name=names.get_full_name()
        return name

    def requirement():
        req=("icu","general bed",  "oxygen bed", "ventilator")
        requirement=random.choice(req)
        return requirement
            
    def diagnosis():
        diag=("covid-19", "heart attack", "pnumonia", "ready for discharge","asthama attack")
        diagnosis=random.choice(diag)
        return diagnosis

    def days():
        days=random.randint(1,15)
        return days

    def contact():
        contact=random.randint(8123456789,9879928364)
        return contact
    roomnumber=1 
    #inserting test values
    for b in range(100):
        pno=b+1
        nam=patientname()
        
        room= 'A' + str(roomnumber)
        roomnumber=int(roomnumber)
        roomnumber=roomnumber+1
        diagn=diagnosis()
        requ=requirement()
        if diagn=='ready for discharge':
            requ="-"
        day=days()
        conta=contact()
        na=nam.replace(" ", "")
        email1=na.lower()+'@gmail.com'
        st="insert into hospital values({}, '{}', '{}', '{}', '{}', {}, '{}', '{}')".format(pno, nam, room, diagn, requ, day, str(conta), email1)
        cursor.execute(st)
        con.commit()


cursor.execute('show tables')
data=cursor.fetchall()
lst=[]
a=('logindetail',)
b=('hospital',)
for i in data:
    lst.append(i)
if b not in lst:
        hospital()
if b in lst:
    print('hospital database found')
if a not in lst:
    cursor.execute('create table logindetail ( EmployeeName varchar(20) , EMPLOYEE_ID int(11), loginpassword varchar(20))')
    print('login table created')
if a in lst:
    print('login database found')

#######################################################################################################################################    

def adddata():  #function to add more patient data
    dou=input('Type "add" if you want to add data or type "del" if you want to delete data: ')
    if dou.upper()=="ADD":
        n=int(input('how many records do you want to add: '))
        for i in range(n):
            
            pname=input('Type the Patient name: ')
            pnumber=int(input('Type Patient number: '))
            roomnum='a'+str(pnumber)
            diagno=input('Enter Patients diagosis: ')
            req=input('Enter Patients requirement: ')
            days=random.randint(1,14)
            contact=input('Enter Patients contact number: ')
            emau=input('Enter the patients email: ')
            cursor.execute("insert into hospital values({}, '{}', '{}', '{}', '{}', {}, '{}', '{}')".format(pnumber, pname, roomnum, diagno, req, days, contact, emau))
            con.commit()
            cursor.execute('select * from hospital where Patient_no =%s' %(pnumber))
            data=cursor.fetchall()
            print('added record:\n', tabulate(data))
    if dou.upper()=="DEL":
        nam=int(input('Please enter the patient number that you want to delete: '))
        cursor.execute('select * from hospital where Patient_no =%s' %(nam))
        data=cursor.fetchall()
        print ('Deleting record:\n', tabulate(data))
        cursor.execute('delete from hospital where Patient_no =%s' %(nam))
        con.commit()
        print('sucess')

        
        
    while True:
        e=input('\nclick enter to continue or type "logout" to logout: ')
        if e=='':
            break
        if e=='logout':
            print('logging out')
            start()
    
########################################################################################################

def retrieve_data():    #function to retrieve one or multiple patients data
    def Name():
        x=input("Enter name: ")
        
        cursor.execute('select * from hospital where name="%s"' %(x))
        data=cursor.fetchall()
        count=cursor.rowcount
        if count==0:
            print('No records found')
        print(tabulate(data))

    def Diagnosis1():
        y=input("Enter diagnosis: ")
        cursor.execute('select * from hospital where diagnosis="%s"' %(y))
        data=cursor.fetchall()
        count=cursor.rowcount
        if count==0:
            print('No records found')
        print(tabulate(data))
        
    def Requirement1():
        z=input("Enter requirement: ")
        cursor.execute('select * from hospital where requirement="%s"' %(z))
        data=cursor.fetchall()
        count=cursor.rowcount
        if count==0:
            print('No records found')
        print(tabulate(data))
    def Patient_no ():
        w=int(input("Enter patient number: "))
        cursor.execute('select * from hospital where Patient_no =%s' %(w))
        data=cursor.fetchall()
        count=cursor.rowcount
        if count==0:
            print('No records found')
        print(tabulate(data))


    print("Search patient(s) by")   #menu for method to search for patient data
    a=int(input("Name(enter 1), Diagnosis (enter 2), Requirement (enter 3), Patient Number (enter 4): "))
    if a==1:
        print("Searching by Name...")
        Name()
    if a==2:
        print("Searching by Diagnosis...")
        Diagnosis1()
    if a==3:
        print("Searching by Requirement...")
        Requirement1()
    if a==4:
        print("Searching by patient number...")
        Patient_no ()
        
    while True:
        e=input('\nclick enter to continue or type "logout" to logout: ')
        if e=='':
            break
        if e=='logout':
            print('logging out')
            start()


###############################################################################################################

import smtplib
def discharge():    #discharge and bill creation
    hospital_mail_id= 'raakeshhospital@gmail.com' #make sure to enter existing gmail id and password otherwise google smtp will throw error
    hospital_password='Root.123'
    
    pNo=int(input("Enter patient number to discharge:"))
    cursor.execute('select diagnosis from hospital where Patient_no=%s'%(pNo))
    diagnosi=cursor.fetchone()
    diagnosis=''
    for item in diagnosi:
        diagnosis = diagnosis + item
    cursor.execute('select email from hospital where Patient_no=%s'%(pNo))
    pgmai=cursor.fetchone()
    pgmail = ''
    for item in pgmai:
        pgmail = pgmail + item
    
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import smtplib

    cursor.execute('select requirement from hospital where Patient_no="%s"' %(pNo))
    data=cursor.fetchone()
    req = ''
    for item in data:
        req = req + item    
    cursor.execute('select Days_admitted from hospital where Patient_no="%s"' %(pNo))
    days=cursor.fetchone()
    day = ''
    for item in days:
        day = day + str(item)
    day=int(day)
    if data=='icu':
        price=day*50000
    if data=='oxygen bed':
        price=day*30000
    if data=='general bed':
        price=day*10000
    if data=='ventilator':
        price=day*4000
    else:
        price=day*4300
    price=str(price)
    # create message object instance
    msg = MIMEMultipart()
    cursor.execute('select * from hospital where Patient_no =%s' %(pNo))
    data=cursor.fetchall()
    data=tabulate(data)
    count=cursor.rowcount
 
    message = """GREETINGS. Please find below attached the reciept and payable amount for your diagnosis.
details:
"""+ data +"""
payable amount:₹"""+ price +"""
Thank you for choosing xyz healthcare.


                                                 This message is auto generated please dont reply to it."""
 
    # setup the parameters of the message
    password =  hospital_password
    msg['From']=hospital_mail_id
    msg['To'] = pgmail
    msg['Subject'] = "Diagnosis Fee"
 
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
 
    #create server
    server = smtplib.SMTP('smtp.gmail.com: 587')
 
    server.starttls()
 
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
 
 
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
 
    server.quit()
 
    print("successfully sent email to %s:" % (msg['To']))
    print('deleting \n'+data)
    cursor.execute('delete from hospital where Patient_no =%s' %(pNo))
    con.commit()

    while True:
        e=input('\nclick enter to continue or type "logout" to logout: ')
        if e=='':
            break
        if e=='logout':
            print('logging out')
            start()

    
###########################################################################################################################    
      

def do():   #main menu that repeats through program
    while True: 
        c=input('Type<1>to add or delete data Type<2>to retrieve data Type<3>to discharge patient:')
        if c=='1':
            adddata()
        if c=='2':
            retrieve_data()
        if c=='3':
            discharge()

#############################################################################################################################       

def login(): #signup/login
    f=True
    i=1
    while f==True:
        user=input('username or employee ID: ')
        passw=cursor.execute('select loginpassword from logindetail where EmployeeName="%s"' %(user))
        passw=cursor.fetchall()
        passw=str(passw)
        passw1=cursor.execute('select loginpassword from logindetail where EMPLOYEE_ID="%s"' %(user))
        passw1=cursor.fetchall()
        passw1=str(passw1)
        password=input('password: ')
        password= "[('"+password+"',)]"
        if password==passw or password==passw1:
            print ('welcome back')
            do()
        else:
            print ('incorrect,', 4-i, 'more tries remaining')
            i=i+1
            if i==4:
                print('too many incorrect entries')
                sys.exit()
                
                
def signup():
    empid=int(input("enter employee id: "))
    name=input("enter name: ")

    password=input("enter password(case sensitive): ")
    sql="insert into logindetail values('{}', {}, '{}')".format(name, empid, password)
    cursor.execute(sql)
    con.commit()
def start():            
    while True:
        a=input('login or signup: ')
        if a=='login':
            login()
        if a=='signup':
            signup()
            print('success')
        if a=='esc':
            quit()



start()
        
    
        

