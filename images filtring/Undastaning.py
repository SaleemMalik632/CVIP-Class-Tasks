import cv2
import numpy as np



image = cv2.imread('P1.jpg')

"""
Apply identity kernel
"""
kernel1 = np.array([[0, 0, 0],
                    [0, 1, 0],
                    [0, 0, 0]])

identity = cv2.filter2D(src=image, ddepth=-1, kernel=kernel1)
kernel2 = np.ones((5, 5), np.float32) / 25 # Create a 5x5 kernel with all elements equal to 1
identity = cv2.filter2D(src=image, ddepth=-1, kernel=kernel2) # Apply kernel to the input image

# cv2.imshow('Original', image)
# cv2.imshow('Identity', identity)

"""
Apply Gaussian blur
"""
# sigmaX is Gaussian Kernel standard deviation 
# ksize is kernel size
imagesGaussian = cv2.GaussianBlur(src=image, ksize=(5,5), sigmaX=0, sigmaY=0)
# cv2.imshow('Apply Gaussian blur', imagesGaussian)

"""
Apply sharpening using kernel
"""

kernel3 = np.array([[0, -1,  0],
                   [-1,  5, -1],
                    [0, -1,  0]] )

sharp_img = cv2.filter2D(src=image, ddepth=-1, kernel=kernel3)
# cv2.imshow('Original', image)
# cv2.imshow('Sharpened', sharp_img) 


"""
Apply edge detection using kernel

"""
kernel4 = np.array([[-1, -1, -1],   # Edge detection kernel
                   [-1,  8, -1],
                   [-1, -1, -1]])
edge_img = cv2.filter2D(src=image, ddepth=-1, kernel=kernel4) # Apply kernel to the input image

cv2.imshow('Original', image)
cv2.imshow('Edge detection', edge_img)


# Convert to graycsale
img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Blur the image for better edge detection
img_blur = cv2.GaussianBlur(img_gray, (3,3), 0) 
 
# Sobel Edge Detection
sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5) # Sobel Edge Detection on the X axis
sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5) # Sobel Edge Detection on the Y axis
sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) # Combined X and Y Sobel Edge Detection
# Display Sobel Edge Detection Images
cv2.imshow('Sobel X', sobelx)
cv2.waitKey(0)
cv2.imshow('Sobel Y', sobely)
cv2.waitKey(0)
cv2.imshow('Sobel X Y using Sobel() function', sobelxy)
cv2.waitKey(0)
 
# Canny Edge Detection
edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200) # Canny Edge Detection
# Display Canny Edge Detection Image
cv2.imshow('Canny Edge Detection', edges)
cv2.waitKey(0)




cv2.waitKey()
cv2.imwrite('identity.jpg', identity)
cv2.destroyAllWindows() 