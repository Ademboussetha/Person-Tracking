""" 
Developed by : Adem Boussetha
Email : ademboussetha@gmail.com
"""
#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
from color_recognition_api import color_histogram_feature_extraction
from color_recognition_api import knn_classifier
import os
import os.path
import sys

global color
def getColor(imageinput):
    source_image=cv2.imread(imageinput)
    prediction = 'n.a.'

    # checking whether the training data is ready
    PATH = './training.data'

    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
        print ('training data is ready, classifier is loading...')
    else:
        print ('training data is being created...')
        open('training.data', 'w')
        color_histogram_feature_extraction.training()
    # get the prediction
    color_histogram_feature_extraction.color_histogram_of_test_image(source_image)
    prediction = knn_classifier.main('training.data', 'test.data')
    print('Detected color is:', prediction)
    return prediction