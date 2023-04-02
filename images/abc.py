import cv2
import sys

path = r'D:\Myprojects\djangoProj\Edumate\images\aclassroom-image.jpg'
img = cv2.imread(path)
print(img)
# create a bounding box around the coordinated
x = 789 
y = 300 
a = 884
b = 408
img=cv2.rectangle(img, (x, y), (a, b), (0, 255, 0), 2)
cv2.imshow('image', img)
cv2.waitKey(0)