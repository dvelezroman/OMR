#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 16:19:07 2019

@author: puesto1
"""

import cv2


class ShapeDetector:
    def __init__(self):
        pass

    @staticmethod
    def detect(c):
        # initialize the shape name and approximate the contour
        shape = "unindentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        if len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)

            if 0.95 <= ar <= 1.05:
                shape = "square"
            else:
                shape = "rectangle"

        return shape
