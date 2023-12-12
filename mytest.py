# encoding: utf-8

import sys
import glob

# 将jpg文件转换为png
def m2mm(ply_path):
    vertex = 0
    row = 0
    with open(ply_path, "r") as plyfile,open("%s.bak" % ply_path, "w") as plyfile_new:
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
        plyfile.close()
        plyfile_new.close()

def print_usage():
    
    print("Usage: compute_gt_poses.py <path>")
    print("path: all or name of the folder")
    print("e.g., compute_gt_poses.py all, compute_gt_poses.py.py LINEMOD/Cheezit")

if __name__ == "__main__":
  
    # try:
    #     if sys.argv[1] == "all":
    #         folders = glob.glob("LINEMOD/*/")
    #     elif sys.argv[1]+"/" in glob.glob("LINEMOD/*/"):
    #         folders = [sys.argv[1]+"/"]
    #     else:
    #         print_usage()
    #         exit()
    # except:
    #     print_usage()
    #     exit()

    # for path in folders:
    #     print(path)
    m2mm("/home/huffie/Documents/PoseEstimation/ObjectDatasetTools/LINEMOD_5obj/batterybox/registeredScene copy.ply")