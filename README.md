
# Linemod Custom

[中文文档](https://www.mahaofei.com/post/82de970.html)

A tool for making your own Linemod dataset for pose estimation algorithms. (The code is not perfect and was written for demo testing, for reference only)

The process in this document refers to the project: [https://github.com/F2Wang/ObjectDatasetTools](https://github.com/F2Wang/ObjectDatasetTools)


### Intro

This tool is a pure python script that is used to create object masks, bounding box labels, 3D object mesh files from RGBD cameras.

The tool prepares training and testing data for a variety of deep learning projects, such as 6D pose estimation, object detection, instance segmentation, and more.

### Preparation

Color print the aruco markers in the arucomarkers folder, ID1-13, a total of 4 pages of A<> paper.

Cut out the markers one by one and stick them around the object.

![](https://img.mahaofei.com/img/20220918100104.png)

Use conda to create a new virtual environment

```bash
conda create -n objectdatasettools python=2.7
conda activate objectdatasettools
```

Install dependencies

```bash
sudo apt-get install build-essential cmake git pkg-config libssl-dev libgl1-mesa-glx
```

```bash
pip install numpy Cython==0.19 pypng==0.0.18 scipy scikit-learn open3d==0.9.0 scikit-image tqdm pykdtree opencv-python==3.3.0.10 opencv-contrib-python==3.3.0.10  trimesh==2.38.24
```

```bash
pip install pyrealsense2
```

### Record a video

**(1) If there is a Realsense camera**

Record a video of an object with the Realsense camera, `record.py` for older models, `recordf2.py` for librealsense SDK 0.2.

```python
python record2.py LINEMOD/OBJECTNAME
```

By default, the script is recorded after 5 countdowns to 40 seconds, and the recording duration can be modified on line 20 in the record.py. You can exit the recording by pressing "Q".

Please move the camera steadily to get a different view of the object while always keeping 2-3 markers within the camera's field of view.

Note that this project assumes that all sequences are saved under a folder named "LINEMOD", using a different folder name will cause the error to occur.

If you create a sequence using record.py, the color image, depth map, and camera parameters are automatically saved in the sequence directory.

![](https://img.mahaofei.com/img/20220918154609.png)

**(2) If there is existing images**

If you already have a color image or a depth image, you should place the color image (.jpg) in a folder named "JPEGImages" and the depth image of it in the "depth" folder.

Note: The algorithm assumes that the depth map is aligned with the color map. Name the color map from 0.jpg, 1.jpg、...、600.jpg and the corresponding depth map to 0.png,...,600.png at the same time, create a file named `intrinsics.json` in the sequence directory, and manually enter the camera parameters as follows

```json
{"fx": 614.4744262695312, "fy": 614.4745483398438, "height": 480, "width": 640, "ppy": 233.29214477539062, "ppx": 308.8282470703125, "ID": "620201000292"}
```

### Gets transformations between frames

Calculate the transformation of the first frame to the specified interval (the interval can be modified in config/registrationParameters), save the transformation (4x4 matrix) as a numpy array. The results of the calculations are saved in `LINEMOD/OBJECTNAME/transforms.npy`

```python
python compute_gt_poses.py LINEMOD/OBJECTNAME
```

or

```python
python compute_gt_poses.py all
```

### 3D reconstruction of the target object

```python
python register_scene.py LINEMOD/OBJECTNAME
```

The above code will save the original registeredScene.ply in the specified directory (e.g., LINEMOD/OBJECTNAME/registeredScene.ply). registerScene.ply is a point cloud of the entire scene, including desktops, marker paper, objects, and other objects in the camera.

![](https://img.mahaofei.com/img/20220918154806.png)


```python
python register_segmented.py LINEMOD/OBJECTNAME
```

Use the code above to skip the manual work, remove unwanted backgrounds, and reconstruct objects in 3D

register_segmented.py converts the object point cloud into a mesh network. FILLBOTTOM is set to true, and the algorithm automatically fills the bottom of the object with a flat surface.

However, register_segmented.py may fail, and some parameters need to be adjusted to make the algorithm work. The most important parameter is MAX_RADIUS, and if the object is large, this value needs to be increased to ensure that the object is not truncated.

**Adjust MAX_RADIUS parameters to make the model as accurate as possible. Use MeshLAB to manually delete orphaned points and areas after generation and then manually save them once.**

### Manually process point clouds

If you are satisfied with the results of the `register_segmented.py` above, you can skip this step.

RegisteredScene.ply opens the generated point cloud data using meshlab:

1. Remove the background
2. Perform a surface reconstruction to complete the missing bottom
3. Handle the rebuilt network
4. Make sure that the processed mesh is free of isolated noise

The final mesh file is generated.

### Generate image masks and label files

When you have finished generating the mesh file of the object, use the following procedure to create image masks and labels

```python
python create_label_files.py all
```

or

```python
python create_label_files.py LINEMOD/OBJECTNAME
```

This step will generate a file named `OBJECTNAME.ply`, open it with meshlab, save it as mesh and uncheck binary, and save the file as the **model file** of the dataset. The AABB is centered on the origin and has the same size as the OBB, and at the same time, the mask folder will generate the mask of the image, the transform matrix of the new mesh will be saved in the transforms folder, and the label file will be saved in the labels folder.

Copy the printed min_xyz and size_xyz to the `models_info.yml` file at the same time.

Use the following command to check the correctness of the bounding box and mask you created:

```python
python inspectMasks.py LINEMOD/OBJECTNAME
```

### Obtain the object scale

```python
python getmeshscale.py
```

Copy the object diameter into a `models_info.yml` file.

### Create a bounding box labels

Once you have the mask of the object, use the following code:

```python
python get_BBs.py
```

An `annotations.csv` file is created at the root directory that contains labels and bounding box information for the object categories of all images.

### Match the dataset format

The following 4 programs are written to process the generated linemod dataset and organize it into a format for linemod_processed dataset.

Generating `gt.yml` and `info.yml` from `annotations.csv` using the following code. It is necessary to modify the `obj_id` correspondence for each object.

```python
python generate_yml.py LINEMOD/timer
```

Rename the image to such a format `0000.png`.

```python
python rename.py all
```

Divide the dataset according to the number of pictures of each object, generate the `train.txt` and `test.txt`.

```python
python data_divide.py all
```

(Change the coordinate unit in the ply file from `m` to `mm`), open the `objectname.ply` file with meshlab, delete the invalid points and save it as `objectname_aligned.ply`, check the `normal` and `color`, and uncheck the `binary encoding`.

Then run the following command to convert the unit of the point cloud file from m to mm:

```python
python plym2mm.py all
```


