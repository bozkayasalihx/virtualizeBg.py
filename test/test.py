import cv2
  
img = cv2.imread("/home/malware/test/background/back.jpg")
  
print("Shape of the image", img.shape)
  
crop = img[50:180, 100:300]  
  
cv2.imshow('original', img)
cv2.imshow('cropped', crop)
cv2.waitKey(0)
cv2.destroyAllWindows()