import cv2

from PIL import Image
import pytesseract
import os

def getFrame(account:str) -> dict:
    vid = cv2.VideoCapture("../../Downloads/AT-cm_336663010.mp4")
    _,image = vid.read()
    image = image[0:170, 0:1280]

    # create sections
    red_score = image[65:115, 500:630]
    blue_score = image[65:115, 670:780]

    match = image[130:170, 180:580]

    match_time = image[15:40, 600:680]

    # Debug. Show all sections
    # cv2.imshow("frame", image)
    # cv2.imshow("rscore", red_score)
    # cv2.imshow("bscore", blue_score)
    # cv2.imshow("match", match)
    # cv2.imshow("match time", match_time)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return {"blue_score": blue_score, "red_score": red_score, "match": match, "match_time": match_time}

def parseFrame(frame:dict):

    # Get text
    blue_score_text = pytesseract.image_to_string(frame["blue_score"], lang='eng', 
           config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
    red_score_text = pytesseract.image_to_string(frame["red_score"], lang='eng', 
           config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
    match_text = pytesseract.image_to_string(frame["match"], lang='eng', 
           config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
    match_time_text = pytesseract.image_to_string(frame["match_time"], lang='eng', 
           config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
    
    # parse match text
    match_text_fmt = match_text.replace("Quarterfinal ", "qf")
    match_text_fmt = match_text_fmt.replace("Final ", "f")
    match_text_fmt = match_text_fmt.replace("Qualification ", "qm")

    match_text_fmt = match_text_fmt.split("of")[0][:-1]

    return {"blue_score": blue_score_text, "red_score": red_score_text, "match": match_text, "match_fmt": match_text_fmt, "match_time": match_time_text}