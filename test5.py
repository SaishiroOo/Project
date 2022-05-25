# importing cv2,imutils,numpy,pytesseract,re
import cv2 
import imutils
import numpy as np
import pytesseract
import re 

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\snir\AppData\Local\Tesseract-OCR\tesseract.exe'

# path 
webcam = cv2.VideoCapture("rtsp://admin:passsnir92@192.168.5.161:554") 

# Reading an image in default mode
while(True):

    # reading from frame
    _, imageFrame = webcam.read() 
    # Window name in which image is displayed
    window_name = 'Reconnaissance'
  
    # Using cv2.cvtColor() method
    # Using cv2.COLOR_BGR2GRAY color space
    # conversion code
    gray = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2GRAY) 
    edged = cv2.Canny(gray, 10, 400)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:4]

    # # loop over our contours
    # for c in cnts:
    #     # approximate the contour
    #     peri = cv2.arcLength(c, True)
    #     approx = cv2.approxPolyDP(c, 0.018 * peri, True)
    #     # if our approximated contour has four points, then
    #     # we can assume that we have found our screen
    #     if len(approx) == 4:
    #         cnts = approx
    #         break
               
    #     else:
    #         detected = 1

    #     if detected == 1:
    #         cv2.drawContours(imageFrame, cnts, -1, (0, 255, 0), 2)

    # # Masking the part other than the number plate
    # mask = np.zeros(gray.shape,np.uint8)
    # new_image = cv2.drawContours(mask,cnts,0,255,-1,)
    # new_image = cv2.bitwise_and(imageFrame,imageFrame,mask=mask)

    # # Now crop
    # (x, y) = np.where(mask == 255)
    # (topx, topy) = (np.min(x), np.min(y))
    # (bottomx, bottomy) = (np.max(x), np.max(y))
    # Cropped = gray[topx:bottomx+1, topy:bottomy+1]

    # #Read the number plate
    # text = pytesseract.image_to_string(imageFrame, config='--psm 11')
    # x = re.findall("[A-Z]{2}-[0-9]{3}-[A-Z]{2}",text)
    # if len(x) == 0:
    #     print("Aucune plaque detecté")
    # else:
    #     x_str = "".join(x[0])
    #     print("Plaque detecté:",x_str)

    # Displaying the image 
    cv2.imshow(window_name, edged)

    if cv2.waitKey(10) & 0xFF == ord('q'): 
        cv2.destroyAllWindows() 
        break