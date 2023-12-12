# encoding: utf-8
import numpy as np
import pandas as pd
import sys
import os
import glob

########################################## 生成gt.yml #################################################
'''
参考格式
0:
- cam_R_m2c: [0.09630630, 0.99404401, 0.05100790, 0.57332098, -0.01350810, -0.81922001, -0.81365103, 0.10814000, -0.57120699]
  cam_t_m2c: [-105.35775150, -117.52119142, 1014.87701320]
  obj_bb: [244, 150, 44, 58]
  obj_id: 1
'''

def create_gt(object_path):
    object_name = object_path.split("/")[1]
    annotations = pd.read_csv("annotations.csv",sep=";")    # 使用pandas读取生成的annotations.csv，获取边界框坐标
    annotations_list = annotations.values[:,:].tolist()
    drop_list = []
    for i in range(len(annotations_list)):
      if object_name not in annotations_list[i][1]:
        drop_list.append(i)
    annotations = annotations.drop(drop_list)
    object_list = annotations.values[:, 2:-1].tolist() # 转换成list
    data_num = len(os.listdir(os.path.join(object_path, "transforms")))
    # 创建gt.yml文件
    gt = open(os.path.join(object_path, "gt.yml"), "w")
    for i in range(data_num):
        npy = np.load(os.path.join(object_path, "transforms") + "/" + str(i) + ".npy")    # 读取生成的npy文件，获取物体位姿
        cam_R_m2c = list(npy[0:3, 0:3].flatten())   # 提取旋转矩阵
        cam_t_m2c = list(npy[0:3, 3].flatten())     # 提取平移矩阵
        gt.write(str(i) + ":")  # 按格式写入gt.yml
        gt.write("\n- cam_R_m2c: " + str(cam_R_m2c))
        # gt.write("\n  cam_t_m2c: " + str(cam_t_m2c))
        gt.write("\n  cam_t_m2c: " + str(list(map(lambda x : x * 1000, cam_t_m2c))))
        gt.write("\n  obj_bb: " + str(object_list[i]))
        gt.write("\n  obj_id: " + "4\n")
        print(object_name + " : " + str(i))
    gt.close()
    print(os.path.join(object_path, "gt.yml ") + "created!")


########################################## 生成info.yml #################################################
'''
参考格式
0:
  cam_K: [572.4114, 0.0, 325.2611, 0.0, 573.57043, 242.04899, 0.0, 0.0, 1.0]
  depth_scale: 1.0
'''

# 查看相机内参
# roslaunch realsense2_camera rs_camera.launch
# rostopic echo /camera/color/camera_info
# cam_K = [907.7092895507812, 0.0, 642.426025390625, 0.0, 907.2830810546875, 356.123046875, 0.0, 0.0, 1.0]

def create_info(object_path):
    # 创建info.yml
    object_name = object_path.split("/")[1]
    annotations = pd.read_csv("annotations.csv",sep=";")    # 使用pandas读取生成的annotations.csv，获取边界框坐标
    annotations_list = annotations.values[:,:].tolist()
    drop_list = []
    for i in range(len(annotations_list)):
      if object_name not in annotations_list[i][1]:
        drop_list.append(i)
    annotations = annotations.drop(drop_list)
    object_list = annotations.values[:, 2:-1].tolist() # 转换成list
    data_num = len(object_list)
    info = open(os.path.join(object_path, "info.yml"), "w")
    for j in range(data_num):
        info.write(str(j) + ":")  # 按格式写入info.yml
        info.write("\n  cam_K: [605.1395263671875, 0.0, 321.6173095703125, 0.0, 604.8554077148438, 237.4153594970703, 0.0, 0.0, 1.0]")
        # info.write("\n  depth_scale: 0.0010000000474974513\n")
        info.write("\n  depth_scale: 1.0\n")
        print(object_name + " : " + str(j))
    info.close()
    print(os.path.join(object_path, "info.yml ") + "created!")

def print_usage():
    
    print("Usage: generate_yml.py <path>")
    print("path: all or name of the folder")
    print("e.g., generate_yml.py all, generate_yml.py LINEMOD/test")

if __name__ == "__main__":
  
    try:
        if sys.argv[1] == "all":
            folders = glob.glob("LINEMOD/*/")
        elif sys.argv[1]+"/" in glob.glob("LINEMOD/*/"):
            folders = [sys.argv[1]+"/"]
        else:
            print_usage()
            exit()
    except:
        print_usage()
        exit()

    for path in folders:
        # print(path)
        create_gt(path)
        create_info(path)
