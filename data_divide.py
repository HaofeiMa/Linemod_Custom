# encoding: utf-8

import os
import sys
import glob
import random


def data_divide(object_path):
    data_num = len(os.listdir(os.path.join(object_path, "depth")))
    l = [i for i in range(data_num)]
    random.shuffle(l)
    train_list = l[:data_num//10]
    test_list = l[data_num//10:]
    train_list.sort()
    test_list.sort()
    return train_list, test_list

def create_txt(object_path, train_list, test_list):
    train = open(os.path.join(object_path, "train.txt"), "w")
    for i in range(len(train_list)):
        train.write("%4d\n" % train_list[i])
    test = open(os.path.join(object_path, "test.txt"), "w")
    for i in range(len(test_list)):
        train.write("%4d\n" % test_list[i])

def print_usage():
    print("Usage: data_divide.py <path>")
    print("path: all or name of the folder")
    print("e.g., data_divide.py all, data_divide.py LINEMOD/test")

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
        train_list, test_list = data_divide(path)
        train = open(os.path.join(path, "train.txt"), "w")
        for item in train_list:
            train.write("%04d\n" % item)
        test = open(os.path.join(path, "test.txt"), "w")
        for item in test_list:
            test.write("%04d\n" % item)
