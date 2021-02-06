
#Stages of this lib is as follow:
# 1. Create random tracking numbers
#        a. numbers range (start, stop)
#        b. Total codes needed (totalsample)
#        c. startstring to put at the begining of the tracking codes such as contract numner
#
# 2. Save these random number
#       a. data which comes from step one (data)
#       b. address for saving the files, better to be a different address from QR code generator destination.
#       c. Contract number to add to the file name (Contract), should be a string
#
# 3. Generate all QRCodes and save them
#       a. data, which created earlier
#       b. The message we want to have with the WhatsApp link (message)
#       c. Destination address is better be an empty folder, should end with "/" or "\"

import qrcode
import numpy as np
import pandas as pd


#String is the code for the contract and manufacturer company's name.
#strat and stop is the range of numbers we want to have codes.
#TotalSample is the number of QR code we want to create.
def CreateRandomTrackingNumber(start, stop, totalsample, startstring):
    data = []
    rnd = np.random.choice(range(start, stop), totalsample, replace=False)
    for i in rnd:
        data.append(startstring+str(i))
    return data


#Data is the array of all tracking codes.
#Address is the location we want to save the Excel file, must ends with / or \.
#Contract number as a string to add it in the file name.
def SaveTrackingAsExcel(data, address, contract):
    writer = pd.ExcelWriter(address+contract+'tracking_codes.xlsx', engine='xlsxwriter')
    # Change the Numpy format to Pandas format to save in Excel file
    panda_dic = pd.DataFrame(data)
    # Data is the Excel's Sheet name to save the data in.
    panda_dic.to_excel(writer, 'Tracking')
    writer.save()
    return


def AdvancedCreateQRCodes(data, message, destination_address):
    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4)

    for i in data:
        message2 = ""
        message2 = message + i
        qr.add_data(message2)
        qr.make(fit=True)
        QRCode = qr.make_image(fill_color="black", back_color="white")
        QRCode.save(destination_address + i + ".png")

    return

def SimpleCreateQRCodes(data, message, destination_address):

    for i in data:
        message2 = ""
        message2 = message + i
        QRCode = qrcode.make(message2)
        QRCode.save(destination_address + i + ".png")

    return




def CreateVQRCode(data, destination_address):
    # Using the below format of data will helps us to create Vcard in QR Code.
    data = '''BEGIN:VCARD

    VERSION:3.0

    N:Lastname;Surname

    FN:TAHER

    ORG:EVenX

    URL:URL HERE

    EMAIL:SOME@EMAIL.COM

    TEL;TYPE=voice,work,pref:+49 1234 56788

    ADR;TYPE=intl,work,postal,parcel:;;Wallstr. 1;Tehran;;12345;Iran

    END:VCARD '''

    data1 = qrcode.make(data)
    data1.save("newqr.png")
    return





start = 1000
stop = 2000
totalsample = 500
startstring = "TAHER21-C0382C01-AAA"

data = CreateRandomTrackingNumber(start, stop, totalsample, startstring)


address = 'G:\Google\Electronic Design\python_projects\Product Authentification\Excel\AAA/'
contract = 'C0382C01'

SaveTrackingAsExcel(data, address, contract)

message = '''
https://wa.me/989033335009

Important Instruction:

Please copy code below in the given whatsapp link for authentification of your product from Taher Agroindustrial Group. 

Code: '''

destination_address = "G:\Google\Electronic Design\python_projects\Product Authentification\QRCodes\AAA/"
SimpleCreateQRCodes(data, message, destination_address)

print('All {} QRCodes are created..'.format(totalsample))