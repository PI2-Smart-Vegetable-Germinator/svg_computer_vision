import numpy as np
import cv2

class ImageProcessing:
    def green_percentage(self, img):
        green = [120, 128, 85]
        threshold = 30
        boundaries = [([green[2] - threshold, green[1] - threshold, green[0] - threshold],
                [green[2] + threshold, green[1] + threshold, green[0] + threshold])]

        for (lower, upper) in boundaries:
            lower = np.array(lower, dtype=np.uint8)
            upper = np.array(upper, dtype=np.uint8)

            mask = cv2.inRange(img, lower, upper)
            output = cv2.bitwise_and(img, img, mask=mask)

            ratio_green = cv2.countNonZero(mask)/(img.size/3)

            return np.round(ratio_green*100, 2)

    def image_treatment(self, img):
        img.seek(0)
        img_array = np.asarray(bytearray(img.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, 1)
        Z = img.reshape((-1,3))

        img = img[89:345, 93:570]

        # convert to np.float32
        Z = np.float32(Z)

        # define criteria, number of clusters(K) and apply kmeans()
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 3
        ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

        # Now convert back into uint8, and make original image
        center = np.uint8(center)
        res = center[label.flatten()]
        img = res.reshape((img.shape))

        return img
        
    def count_sprouted_seedlings(self, img):
        if(self.green_percentage(img)):
            y_step = 15
            x_step = 40
            sprouted_seedlings = 0

            for y in range(0, 300, y_step):
                for x in range(0, 400, x_step):
                    a = img[y:y+y_step, x:x+x_step]

                    try:
                        if(self.green_percentage(a)):
                            sprouted_seedlings+=1
                    except Exception as e:
                        print(e)
            
            return sprouted_seedlings
        else:
            return 0