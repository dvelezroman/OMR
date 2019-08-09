import argparse
import imutils as im
import cv2
import json
from OMR_detect_barCode import BarCodeDetect
from serveForm  import ServeForm
import os

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
ap.add_argument("-o", "--output", help="path to the output CSV results of forms")
ap.add_argument("-d", "--directory", required=True, help="Folder where are stored the JSON Forms")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
resized = im.resize(image, width=600)
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

ratio = image.shape[0] / float(resized.shape[0])
ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

bcd = BarCodeDetect()
sf = ServeForm(args["directory"])

barcode = bcd.findBarCodes(image)[0]
barcode = barcode.data.decode("utf-8")

formName = barcode.split("U")[1]
form = sf.give_me_form(int(formName))

form["barcode"] = barcode

quest_count = 0
threshold = 50
if form["type"] == "answers_sheet":
    threshold = 30


for question in form["questions"]:
    option_count = 0
    if question["selection"] == "simple":
        for option in question["options"]:
            x1 = round(option["coords"][0][0] / ratio)
            y1 = round(option["coords"][0][1] / ratio)
            x2 = round(option["coords"][1][0] / ratio)
            y2 = round(option["coords"][1][1] / ratio)
            pt1 = (x1, y1)
            pt2 = (x2, y2)
            cv2.rectangle(resized, pt1, pt2, (255, 0, 0), 1)
            areaToCalc = thresh[y1:y2, x1:x2]
            result = cv2.countNonZero(areaToCalc)
            #print(f"Result of {question['number']} - {option['text']} = {result}")
            if result > threshold:
                form["questions"][quest_count]["options"][option_count]["selected"] = True
                cv2.rectangle(resized, pt1, pt2, (0, 255, 0), 1)
            option_count += 1
    if question["selection"] == "matrix":
        main_option_count = 0
        for main_option in question["options"]:
            nested_option_count = 0
            for nested_option in main_option["options"]:
                x1 = round(nested_option["coords"][0][0] / ratio)
                y1 = round(nested_option["coords"][0][1] / ratio)
                x2 = round(nested_option["coords"][1][0] / ratio)
                y2 = round(nested_option["coords"][1][1] / ratio)
                pt1 = (x1, y1)
                pt2 = (x2, y2)
                cv2.rectangle(resized, pt1, pt2, (255, 0, 0), 1)
                areaToCalc = thresh[y1:y2, x1:x2]
                result = cv2.countNonZero(areaToCalc)
                if result > threshold:
                    form["questions"][quest_count]["options"][main_option_count]["options"][nested_option_count]["selected"] = True
                    cv2.rectangle(resized, pt1, pt2, (0, 255, 0), 1)
                nested_option_count += 1
            main_option_count += 1

    quest_count += 1

form["processed"] = True
cv2.imshow("Marks", resized)
cv2.waitKey(0)

folder = args["output"]

if not os.path.exists(folder):
    os.makedirs(folder)

nested_folder = os.path.join(folder, barcode.split("U")[0])

if not os.path.exists(nested_folder):
    os.makedirs(nested_folder)

path = os.path.join(nested_folder, barcode.split("U")[1] + ".json")
with open(path, "w", encoding="utf-8") as file:
    json.dump(form, file, ensure_ascii=False, indent=4)
