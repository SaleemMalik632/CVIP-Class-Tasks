import cv2
import numpy as np

# Reading images
image1 = cv2.imread("P1.png")
image2 = cv2.imread("P4.png")
image3 = cv2.imread("P3.png")


image1 = cv2.imread("P1.png")
if image1 is None:
    print("Error loading P1.png")

 
# Resize images to a common size
common_size = (250, 250)
# image1 = cv2.resize(image1, common_size)
image2 = cv2.resize(image2, common_size)
image3 = cv2.resize(image3, common_size)



print(image1)

# Create a black canvas for the collage
collage = np.zeros((common_size[1]*2, common_size[0]*2, 3) , dtype="uint8")

print(collage.shape)
print(image1.shape) 

# Place images on the canvas
collage[:200, :300] = cv2.resize(image1,(300,200))
collage[:200, 300:] = cv2.resize(image2,(200,200))
collage[200:500, :500] = cv2.resize(image3,(500,300))


collage2 = np.zeros((common_size[1]*2, common_size[0]*2, 3) , dtype="uint8")


collage2[:500, :300] = cv2.resize(image3,(300,500))
collage2[:250, 300:] = cv2.resize(image2,(200,250))
collage2[250:500, 300:] = cv2.resize(image1,(200,250)) 

# Display the collage
cv2.imshow("Collage", collage)
cv2.imshow("Collage2", collage2)
cv2.waitKey(0)
cv2.destroyAllWindows()
