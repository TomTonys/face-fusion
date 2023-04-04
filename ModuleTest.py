# -*- coding: utf-8 -*-
# @Time    : 2017/9/2 13:40
# @Author  : 郑梓斌
import time

import core
from core.facepointget import face_detect
from core.morpher import zoom_pic

def start():
    start_time = time.time()
    # mode_img_path = 'images/model.jpg'  # 模板图
    mode_img_path = 'images/yell2.jpg'  # 模板图
    dst_img_path = 'images/ym.jpg'  # 换脸图
    put_img_paht = 'images/output4.jpg'  # 输出地址

    zoom_pic(mode_img_path, dst_img_path)  # 对换脸图进行缩放，不然图比模板图大在install时点会超出模板图导致报错
    point = face_detect(dst_img_path)
    # point = [180,206,307,400]
    # print(point)
    # print(type(point[0]))
    core.face_merge(src_img=mode_img_path,
                    dst_img=dst_img_path,
                    out_img=put_img_paht,
                    face_area=point,
                    alpha=0.75,
                    k_size=(15, 10),
                    mat_multiple=0.95)
    end_time = time.time()
    print(end_time-start_time)

if __name__ == '__main__':
    start()
