from typing import List, Tuple

import cv2
import numpy as np


def getMinMaxLoc(points: np.ndarray) -> Tuple[int, int, int, int]:
    '''Input cv2.findContour(...)[0]. Output (xmin, ymin, xmax, ymax).'''
    return (points[:, 0, 1].min(), points[:, 0, 0].min(), 
            points[:, 0, 1].max(), points[:, 0, 0].max())


img: np.ndarray = cv2.imread('I80.jpg', cv2.IMREAD_UNCHANGED)

roi: Tuple[int, int, int, int] = cv2.selectROI(img)
cv2.destroyAllWindows()
crop: np.ndarray = img[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]

blueCrop: np.ndarray = cv2.split(crop)[0]
thr145blue: np.ndarray = cv2.threshold(blueCrop, 145, 255, 
                                       cv2.THRESH_BINARY)[1]
ctrs: np.ndarray = cv2.findContours(thr145blue,
                                    cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)[0]

rects: List[Tuple[int, int, int, int]] = [getMinMaxLoc(c) for c in ctrs]
for rec in rects:
    cv2.rectangle(crop,
                  pt1=(rec[1] - 15, rec[0] - 15),
                  pt2=(rec[3] + 15, rec[2] + 15),
                  color=(0, 255, 0),
                  thickness=3)

cv2.imshow(None, crop)
stay = True
while stay:
    stay = not cv2.waitKey(90) == ord('q')
cv2.destroyAllWindows()