'''

Created by: Saaras Pakanati (Github Id: randochat)
Data: 22nd May 2022

Credits:
Anand Jagadeesan (https://www.geeksforgeeks.org/text-detection-and-extraction-using-opencv-and-ocr/) 
    - For detection of information of data in the image section of the code.
    - Additions made by me inslcude thresholding the images to comply with the 
        the LEGO instruction sheets in a more efficient and accurate manner.

'''

# Import required packages
import cv2
import pytesseract
import numpy as np
import mysql.connector
from mysql.connector import Error

def LEGO_SET_DB(imagename):

    # Mention the installed location of Tesseract-OCR in your system
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\tesseract.exe"

    # Read image from which text needs to be extracted
    img = cv2.imread(imagename)

    ####cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
    lower = np.array([230, 230, 0])
    upper = np.array([255, 255, 255])

    gray = cv2.inRange(img, lower, upper)
    #gray = cv2.bitwise_not(gray)

    # Preprocessing the image starts

    # Convert the image to gray scale
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # Specify structure shape and kernel size.
    # Kernel size increases or decreases the area
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect
    # each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                    cv2.CHAIN_APPROX_NONE)

    # Creating a copy of image
    im2 = img.copy()

    # A text file is created and flushed
    file = open("recognized.txt", "w+")
    file.write("")
    file.close()

    # Looping through the identified contours
    # Then rectangular part is cropped and passed on
    # to pytesseract for extracting text from it
    # Extracted text is then written into the text file
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        
        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]
        
        # Open the file in append mode
        file = open("recognized.txt", "a")
        
        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)
        
        # Appending the text into file
        file.write(text)
        file.write("\n")
        
        # Close the file
        file.close

    # Opening temporary dump file in read mode to delete any previous data.
    LEGOFile = open('recognized.txt' , 'r')

    # Initializing required variables.
    LEGOSetDataPiecesSQLPush = []
    EmptyStringPlaceHolder = ''

    # Gathering data in the temporary dump file.
    LEGOSetDataPieces = LEGOFile.readlines()

    # Itteration through the data in the temporary dump file.
    for i in range(len(LEGOSetDataPieces)):
        for j in range(len(LEGOSetDataPieces[i])):

            # Validating data with a 'x' or 'k' sign to read number of pieces.
            if LEGOSetDataPieces[i][j] == 'x' or LEGOSetDataPieces[i][j] == 'k':

                # Calculating all the values before the 'x' to mitigate any unwanted data values creeping into the 
                # SQL Push List that may cause issues downstream.
                for k in range(j-1, -1, -1):
                    if LEGOSetDataPieces[i][k].isdigit() == True:
                        EmptyStringPlaceHolder = LEGOSetDataPieces[i][k] + EmptyStringPlaceHolder
                PieceNumber = LEGOSetDataPieces[i+1].replace('\n' , '')

                # Upon inspection, it was observed that pytesseract in its current implementation was unable to
                # detect ones with great accuracy and often read them as whitespaces. In order to make the data
                # more comprehensive, if the program reads no predecessor digit to the 'x' symbol, we add one to
                # it.
                if EmptyStringPlaceHolder == '':
                    EmptyStringPlaceHolder = '1'

                LEGOSetDataPiecesSQLPush.append((PieceNumber , EmptyStringPlaceHolder))
                EmptyStringPlaceHolder = ''

    # Displaying the pushed data to run analysis if required.
    print(LEGOSetDataPiecesSQLPush)

    # Establishing connection with the database present in the MySQL 
    # local environment.
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='LEGOSETDATA',
                                            user='root',
                                            password='Saaras1234')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

    # Displaying error incase of an error in establishing a connection 
    # with the database in the MySQL local environment.
    except Error as e:
        print("Error while connecting to MySQL", e)

    # Creating a cursor object to itterate through the database.
    mycursor = connection.cursor()

    # Pushing data into a table in the database.
    sql = "INSERT INTO SETSDATAALPHA (PieceNumber, NumberOfPieces) VALUES (%s, %s)"
    mycursor.executemany(sql, LEGOSetDataPiecesSQLPush)
    connection.commit()
    print(mycursor.rowcount, "was inserted.")

#Test condition
'''
imagenameinitial = "TessSample3.png"

LEGO_SET_DB(imagenameinitial)
'''

# End of code

########################################################################################