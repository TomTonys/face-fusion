#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: v_vxchliu
@file: ffmpeg_lib
@time: 2023/04/06
@contact: v_vxchliu@tencent.com
@desc: ffmpeg相关操作
"""
import os


def ffmepg_split_2_img(video_path, out_put_path, fps=15):
    """
    利用ffmpeg对视频进行切片
    :param out_put_path:视频切片后输出地址
    :param video_path: 需要处理的视频地址
    :param fps: 没一秒取多少帧
    :return:
    """
    cmd = f"ffmpeg -i {video_path} -r {fps} -f image2 {out_put_path}/1_fram_%05d.png"
    code = os.system(cmd)
    if code != 0:
        print('exec ffmpeg failed')
        return False
    else:
        ffmpeg_split_2_audio(video_path, out_put_path)
        return True


def ffmpeg_split_2_audio(video_path, out_dir):
    cmd = f"ffmpeg -i {video_path} -vn -codec copy {out_dir}/out.m4a"
    code = os.system(cmd)
    if code != 0:
        print('exec ffmpeg failed')
        return False
    else:
        return True


def ffmpeg_merge_2_mp4(image_dir, audio_dir, out_put_path, fps=15):
    cmd = f'ffmpeg -f image2 -framerate {fps} ' \
          f'-i "{image_dir}/1_fram_%05d.png" -i {audio_dir}/out.m4a ' \
          f'-b:v 25313k {out_put_path}'
    code = os.system(cmd)
    if code != 0:
        print('exec ffmpeg failed')
        return False
    else:
        return True
