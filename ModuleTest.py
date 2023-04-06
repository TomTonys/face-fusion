# -*- coding: utf-8 -*-
# @Time    : 2017/9/2 13:40
# @Author  : 郑梓斌
import multiprocessing
import os
import shutil
import time

import core
from core.facepointget import face_detect
from core.ffmpeg_lib import ffmpeg_merge_2_mp4, ffmepg_split_2_img
from core.morpher import zoom_pic


def image_face(mode_img_path, dst_img_path, put_img_paht):
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


def get_image(start_path, stype=None):
    """
    获取满足条件的图片的集合
    :param stype:
    :param start_path:
    :return:
    """
    if stype is None:
        stype = ['jpg', 'png', 'bmp', 'jpeg', 'pbm']
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


def video_face(mode_pic_path, dst_pic_path, put_img_paht):
    """
    :param mode_pic_path: 模板图片
    :param dst_pic_path: 融合图片
    :param put_img_paht: 输出图片
    :return:
    """
    point = face_detect(mode_pic_path)
    print(point)
    if len(point) > 0:
        try:
            image_face(mode_pic_path, dst_pic_path, put_img_paht)
        except Exception as e:
            print(e)
            shutil.copy(mode_pic_path, put_img_paht)
    else:
        print('未失败到人脸，直接copy')
        shutil.copy(mode_pic_path, put_img_paht)


def start_video_face():
    dst_pic_path = 'images/ym.jpg'  # 融合图
    put_img_paht_base = 'video/fuse/'  # 输出路径
    mode_video_paht = 'video/720x1080_30fps_11s_2634kbs.mp4'  # 视频
    current_file_paht = __file__
    current_file_dir = os.path.dirname(current_file_paht)
    video_pic_path = current_file_dir + "/video/output"
    if not os.listdir(video_pic_path):  # 判断
        ffmepg_split_2_img(video_path=mode_video_paht, out_put_path=video_pic_path, fps=15)  # 分割视频为图片和音频

    mode_pic_path_list = get_image(video_pic_path)

    pool = multiprocessing.Pool(10)  # 定义进程池的进程数量
    for mode_pic_path in mode_pic_path_list:
        put_img_paht = put_img_paht_base + str(mode_pic_path.split("\\")[-1])
        if not os.path.exists(put_img_paht):
            pool.apply_async(func=video_face, args=(mode_pic_path, dst_pic_path, put_img_paht))
        else:
            print("{}--文件存在".format(put_img_paht))
    pool.close()
    pool.join()
    ffmpeg_status = ffmpeg_merge_2_mp4(put_img_paht_base,
                                       audio_dir=video_pic_path,
                                       out_put_path=put_img_paht_base + "zzz.mp4",
                                       fps=15)  # 合并视频
    if ffmpeg_status:
        print('视频合并成功')
    else:
        print('视频合并失败')


if __name__ == '__main__':
    # start()
    start_video_face()
