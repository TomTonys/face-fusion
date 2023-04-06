#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: v_vxchliu
@file: facepointget
@time: 2023/04/04
@contact: v_vxchliu@tencent.com
@desc: 通过dlib提取关键的
"""

import dlib
import cv2

def get_point_2_dlib(png_path):
    predictor_path = "face_mode_file/shape_predictor_81_face_landmarks.dat"  # 权重文件路径
    # png_path = "../images/20171030175254.jpg"

    detector = dlib.get_frontal_face_detector()
    #相撞
    predicator = dlib.shape_predictor(predictor_path)
    # win = dlib.image_window()
    img1 = cv2.imread(png_path)

    dets = detector(img1,1)
    if len(dets) == 0:
        return []
    else:
        # print("Number of faces detected : {}".format(len(dets)))
        for k, d in enumerate(dets):
            lanmarks = [[p.x,p.y] for p in predicator(img1,d).parts()]
            break
        return lanmarks

def face_detect(image):

    img1 = cv2.imread(image)

    gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

    face_detector = cv2.CascadeClassifier("face_mode_file/haarcascade_frontalface_default.xml")

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,)

    if len(faces) > 0:
        for (x, y, w, h) in faces:
            face_frame = [int(x),int(y),int(w),int(h)]
            break
    else:
        face_frame = ()
    return face_frame
#
