# LEGO PIECES TO DATABASE

## Introduction
The code was created to conform to other codes that required the lego pieces present in a LEGO set to be brought to a DBMS by simply using an image of the parts list provided in the end of every booklet.

## Software and languages used
The base code has been coded on Python along with the use of the following libraries and services:

1. OpenCV (cv2)
  https://pypi.org/project/opencv-python/
  
2. Google Tesseract (pytesseract)
  https://pypi.org/project/pytesseract/
  In additon to the package, the following link goes through the additional downloads required to execute the code.
  https://github.com/tesseract-ocr/tesseract
  
3. Numpy (numpy)
  https://numpy.org/

4. MySQL (mysql.connector and Error from mysql.connector)
  https://dev.mysql.com/doc/connector-python/en/
  The below link provides instructions on downloading the application.
  https://www.mysql.com/

## References
1. Anand Jagadeesan (https://www.geeksforgeeks.org/text-detection-and-extraction-using-opencv-and-ocr/) 
  - For detection of information of data in the image section of the code.
  - Additions made by me inslcude thresholding the images to comply with the 
        the LEGO instruction sheets in a more efficient and accurate manner.
        
2. https://pypi.org/project/opencv-python/

3. https://pypi.org/project/pytesseract/
 
4. https://github.com/tesseract-ocr/tesseract

5. https://numpy.org/

6. https://dev.mysql.com/doc/connector-python/en/

7. https://www.mysql.com/

## Conclusion
This code has been optimized for reading the LEGO parts list. For any wider application, play around with the thresholding of the image. 

Hope this code helps!




