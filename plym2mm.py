# encoding: utf-8

import os
import sys
import glob
import shutil
import cv2

# ply由m单位转为mm单位
def m2mm(object_path):
    ply_name = object_path.split("/")[1] + "_utf8.ply"
    ply_path = os.path.join(object_path, ply_name)
    vertex = 0
    row = 0
    with open(ply_path, "r") as plyfile,open("%s_mm.ply" % ply_path, "w") as plyfile_new:
        for line in plyfile:
            row += 1
            newline = line
            if row == 4:
                vertex = line.split(" ")[2]
            if row > 17 and row <= int(vertex) + 17:
                line_list = line.split(" ")[:10]
                line_list[0] = str(float(line_list[0]) * 1000)
                line_list[1] = str(float(line_list[1]) * 1000)
                line_list[2] = str(float(line_list[2]) * 1000)
                newline = " ".join(line_list) + " \n"
            plyfile_new.write(newline)
    print("Created %s!", ply_path)
            
        


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
        m2mm(path)