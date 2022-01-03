import cv2
import numpy as np
import glob 
import img2pdf
import os
import time

instructions = """
Instructions:
Select the points in the following order Top left, top right, bottom left, bottom right.
Once the points are selected press esc key to move to the next image.
"""
print(instructions)
time.sleep(2)
size = (3508, 2480) # A4 size
dst = np.array([[0,0],[size[1],0], [0, size[0]], [size[1], size[0]]], dtype=float)

def click_event(event, x, y, flags, params):

    if event == cv2.EVENT_LBUTTONDOWN:
        pointSrc = params[1]
        if len(pointSrc) <4 : 
            cv2.circle(params[0], (x,y), 8, (0, 0, 255), -1)
            cv2.imshow('image', params[0])
            pointSrc.append([x, y])

        if len(pointSrc) == 4:
            return


def main_func(image, file):
    pointSrc = list()

    i = image.copy()
    cv2.imshow("image", image)
    cv2.setMouseCallback('image', click_event, [image, pointSrc])
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    pointSrc = np.array(pointSrc)
    M, mask = cv2.findHomography(pointSrc, dst)
    result_img = cv2.warpPerspective(i, M, (size[1], size[0]))
    fname = "result_" + file[:-4] + ".png"
    cv2.imwrite(fname, result_img)


for file in glob.glob("*.jpg"):
    image = cv2.imread(file)
    main_func(image, file)

with open("result.pdf","wb") as f:
    f.write(img2pdf.convert(sorted(glob.glob("*.png"))))

for file in glob.glob("*.png"):
    os.remove(file)
