import cv2
import numpy as np

size = (3508, 2480) # A4 size
image = cv2.imread("image.jpg")

def click_event(event, x, y, flags, params):

    if event == cv2.EVENT_LBUTTONDOWN:
        pointSrc = params[1]
        if len(pointSrc) <4 : 
            cv2.circle(params[0], (x,y), 8, (0, 0, 255), -1)
            cv2.imshow('image', params[0])
            pointSrc.append([x, y])


pointSrc = list()

cv2.imshow("image", image)
cv2.setMouseCallback('image', click_event, [image, pointSrc])
cv2.waitKey(0)
cv2.destroyAllWindows()

dst = np.array([[0,0],[size[1],0], [0, size[0]], [size[1], size[0]]], dtype=float)
pointSrc = np.array(pointSrc)
M, mask = cv2.findHomography(pointSrc, dst)
result_img = cv2.warpPerspective(image, M, (size[1], size[0]))
cv2.imwrite("result.jpg", result_img)

