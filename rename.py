# encoding: utf-8

import os
import sys
import glob
import shutil
import cv2

# 将jpg文件转换为png
def transform(object_path):
    for root, dirs, files in os.walk(os.path.join(object_path, "JPEGImages")):
        for name in files:
            file = os.path.join(root, name)
            print('transform' + name)
            im = cv2.imread(file)
            cv2.imwrite(file.replace('jpg', 'png'), im)

def rename_dir(object_path):
    os.rename(os.path.join(object_path, "JPEGImages"), os.path.join(object_path, "rgb"))

# rename_img("LINEMOD/timer", "depth", ".png")
# rename_img("LINEMOD/timer", "rgb", ".png")
# rename_img("LINEMOD/timer", "mask", ".png")
def rename_img(object_path, dir, ext):
    dir_path = os.path.join(object_path, dir)
    for file in os.listdir(dir_path):
        name = file.split(".")[0]
        os.rename(os.path.join(dir_path, file), os.path.join(dir_path, '%04d' % int(name) + ext))

# 复制mask文件夹为label
def copy_dir(object_path):
    shutil.copytree(os.path.join(object_path, "mask"), os.path.join(object_path, "label"))

def print_usage():
    
    print("Usage: rename.py <path>")
    print("path: all or name of the folder")
    print("e.g., rename.py all, rename.py LINEMOD/test")

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
        transform(path)
        copy_dir(path)
        rename_dir(path)
        rename_img(path, "depth", ".png")
        rename_img(path, "rgb", ".png")
        # rename_img(path, "JPEGImages", ".png")
        rename_img(path, "mask", ".png")
        rename_img(path, "label", "_label.png")