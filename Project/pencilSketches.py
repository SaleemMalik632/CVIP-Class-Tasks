import numpy as np
import cv2
import typing

class PencilSketch:
    """Apply pencil sketch effect to an image
    """
    def __init__(
        self,
        blur_sigma: int = 5,
        ksize: typing.Tuple[int, int] = (0, 0),
        sharpen_value: int = None,
        kernel: np.ndarray = None,
        ) -> None:
        """
        Args:
            blur_sigma: (int) - sigma ratio to apply for cv2.GaussianBlur
            ksize: (float) - ratio to apply for cv2.GaussianBlur
            sharpen_value: (int) - sharpen value to apply in predefined kernel array
            kernel: (np.ndarray) - custom kernel to apply in sharpen function
        """
        self.blur_sigma = blur_sigma
        self.ksize = ksize
        self.sharpen_value = sharpen_value
        self.kernel = np.array([[0, -1, 0], [-1, sharpen_value, -1], [0, -1, 0]]) if kernel is None else kernel

    def dodge(self, front: np.ndarray, back: np.ndarray) -> np.ndarray:
        """The formula comes from https://en.wikipedia.org/wiki/Blend_modes
        Args:
            front: (np.ndarray) - front image to be applied to dodge algorithm
            back: (np.ndarray) - back image to be applied to dodge algorithm

        Returns:
            image: (np.ndarray) - dodged image
        """
        result = front * 255.0 / (255.0 - back + 1e-5)
        result[result > 255] = 255
        result[back == 255] = 255
        return result.astype('uint8')

    def sharpen(self, image: np.ndarray) -> np.ndarray:
        """Sharpen image by defined kernel size
        Args:
            image: (np.ndarray) - image to be sharpened

        Returns:
            image: (np.ndarray) - sharpened image
        """
        if self.sharpen_value is not None and isinstance(self.sharpen_value, int):
            inverted = 255 - image
            return 255 - cv2.filter2D(src=inverted, ddepth=-1, kernel=self.kernel)

        return image

    def __call__(self, image: np.ndarray) -> np.ndarray:
        """Main function to do pencil sketch
        Args:
            image: (np.ndarray) - image to execute pencil sketch on

        Returns:
            image: (np.ndarray) - processed image that is a pencil sketch
        """
        if len(image.shape) == 2:
            grayscale = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        else:
            grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            grayscale = cv2.cvtColor(grayscale, cv2.COLOR_GRAY2BGR)

        inverted_img = 255 - grayscale

        blur_img = cv2.GaussianBlur(inverted_img, ksize=self.ksize, sigmaX=self.blur_sigma)

        final_img = self.dodge(blur_img, grayscale)

        sharpened_image = self.sharpen(final_img)

        return sharpened_image

if __name__ == '__main__': 
    pencilSketch = PencilSketch(blur_sigma=5)
    image = cv2.imread('P2.jpg')
    sketch_image = pencilSketch(image)
    cv2.imshow('Original Image', image)
    cv2.imshow('Pencil Sketch', sketch_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
