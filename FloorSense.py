import serial
import re
import numpy as np
from time import sleep
import smtplib
import base64
import datetime
from twilio.rest import TwilioRestClient
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

''' Twilio Creds '''
account_id = 'ACd0cd34fdb40d80a3c63a73e6a3562bbf'
auth_token = '6c289bcada7ddbf16fdb677355ad0bfa'
my_cell = '+14808685672'
my_twilio = '+12402932616' 

def sendmailto(date_time):
    '''
    This function uses Gmail Mailing Protocol to send mail to the emergency contact
    
    '''
    server = smtplib.SMTP('smtp.gmail.com', 587)

    fromaddr = "python.platform.results@gmail.com"
    toaddr = ["kgairola@gmail.com"]

    SUBJECT = "!! EMERGENCY AT JOHN DOE !! "
    TEXT = ["EMERGENCY AT JOHN DOE on ", date_time , "at 1234 First Ave, NY"] 
    TEXT = ''.join(i for i in TEXT)

    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    server.starttls()
    server.login(fromaddr, base64.b64decode("cHl0aG9uQHB5dGhvbg==").decode("utf-8"))
    server.sendmail(fromaddr, toaddr, message)
    server.quit()
    
def sendSMS(account_id, auth_token, my_cell, my_twilio, date_time):
    ''' 
    The function uses twilio application to send sms to the emergency contact
    '''
    client = TwilioRestClient(account_id, auth_token)
    my_msg = ["!! EMERGENCY !! Reach Home. Date - ", date_time]
    my_msg = ''.join(i for i in my_msg)
    message = client.messages.create(to = my_cell, from_ = my_twilio, body = my_msg)
    
def TakeAction(date_time, send_email = "yes", send_sms = "yes"):
    if send_email == "yes":
        sendmailto(date_time)
        
    if send_sms == "yes":
        sendSMS(account_id, auth_token, my_cell, my_twilio, date_time)
        
def plotImage (floor):
    # Make a 2x3 grid...
    nrows, ncols = 2,3
    image = np.zeros((nrows,ncols))
    
    for j in range(floor.shape[0]):
        for k in range(floor.shape[1]):
            image[j][k] = floor[j][k]
            
    row_labels = range(nrows)
    col_labels = ['A', 'B', 'C']
    plt.matshow(image)
    plt.xticks(range(ncols), col_labels)
    plt.yticks(range(nrows), row_labels)
    plt.show()

ser = serial.Serial("COM5", 9600)
set_flag = "No Action"
try:
    number = []
    for i in range(100):
        line = str(ser.readline()).split("'")[1].strip().split('\\')[0] # + ";" +  "0"
        number.append([re.findall(r'\d+', line), datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")])
        for j in range(len(number[i][0])):
            if int(number[i][0][j]) == 0 :
                number[i][0][j] = 0
            else:
                number[i][0][j] = 1
        total = sum(number[i][0])
        #plotImage(np.array(number[i][0][:-1]).reshape(2,3))
        #print(total)
        if total>3:
            wait_period = 5
            for flag in range(wait_period):
                line_flag = str(ser.readline()).split("'")[1].strip().split('\\')[0]
                number_flag = re.findall(r'\d+', line)           
                for k in range(len(number_flag)):
                    if int(number_flag[k])==0:
                        number_flag[k] = 0
                    else:
                        number_flag[k] = 1
                total_flag = sum(number_flag)
                #print(total_flag)
                if total_flag >3:
                    set_flag = "Action"
                else:
                    set_flag = "No Action"
                    break
        if set_flag == "Action":
            #print("Action Taken")
            TakeAction(number[i][1], "yes","yes",)
            break
    ser.flush()    
    ser.close()
except KeyboardInterrupt:
    ser.flush()    
    ser.close()
