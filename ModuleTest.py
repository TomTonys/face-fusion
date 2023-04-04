# -*- coding: utf-8 -*-
# @Time    : 2017/9/2 13:40
# @Author  : 郑梓斌
import os
import shutil
import time

import core
from core.facepointget import face_detect
from core.morpher import zoom_pic

def start(mode_img_path,dst_img_path,put_img_paht):
    # start_time = time.time()
    # mode_img_path = 'images/model.jpg'  # 模板图
    # mode_img_path = 'images/yell2.jpg'  # 模板图
    # dst_img_path = 'images/ym.jpg'  # 换脸图
    # put_img_paht = 'images/output5.jpg'  # 输出地址

    zoom_pic(mode_img_path, dst_img_path)  # 对换脸图进行缩放，不然图比模板图大在install时点会超出模板图导致报错
    point = face_detect(dst_img_path)
    # point = [180,206,307,400]
    # print(point)
    # print(type(point[0]))
    core.face_merge(src_img=mode_img_path,
                    dst_img=dst_img_path,
                    out_img=put_img_paht,
                    face_area=point,
                    alpha=0.78,
                    k_size=(15, 10),
                    mat_multiple=0.9)
    # end_time = time.time()
    # print(end_time-start_time)

def get_image(start_path, stype=['jpg', 'png', 'bmp', 'jpeg', 'pbm']):
    """
    获取满足条件的图片的集合
    :param start_path:
    :return:
    """
    image_list = []
    if os.path.exists(start_path):
        for root, dirs, files in os.walk(start_path):
            for file in files:
                if file.split('.')[-1] in stype:
                    try:
                        decode_str = os.path.join(
                            root, file)
                    except UnicodeDecodeError:
                        decode_str = os.path.join(
                            root, file)
                    image_list.append(decode_str)
    return image_list
def video_face():
    dst_pic_path = 'images/ym.jpg'  # 融合图
    put_img_paht_base = 'video/fuse/'  # 输出路径
    current_file_paht = __file__
    current_file_dir = os.path.dirname(current_file_paht)
    video_pic_path = current_file_dir + "/video/output"
    mode_pic_path_list = get_image(video_pic_path)
    for mode_pic_path in mode_pic_path_list:
        put_img_paht = put_img_paht_base + mode_pic_path.split("\\")[-1]
        point = face_detect(mode_pic_path)
        print(point)
        if len(point) > 0:
            start(mode_pic_path, dst_pic_path, put_img_paht)
        else:
            shutil.copy(mode_pic_path,put_img_paht)


if __name__ == '__main__':
    # start()
    video_face()
