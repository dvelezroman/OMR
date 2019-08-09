#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 11:22:20 2019

@author: puesto1
"""

from pyzbar import pyzbar


class BarCodeDetect:
    def __init__(self):
        pass

    def findBarCodes(self, image):
        barcodes = pyzbar.decode(image)
        return barcodes

    def markBarCodes(self, barcodes, image):
        codes = []
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            codes.append((x, y), (x + w, y + h))
