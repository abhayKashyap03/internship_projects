# Split Dataset, Draw Bounding Boxes, Image Information

## Packages 
- `os, shutil, random, argparse, glob, time`
- `ast, pandas, numpy, cv2`

- If not installed : `pip install ast pandas numpy opencv-python`

## Split Dataset

```shell
python split_script.py --image_folder /path/to/folder/containing/images --csv_path /path/to/csv --separate_folders [True,False] --class_folders [True,False] --dest_folder /path/to/separate/folders --train_size float --test_size float --val_size float --shuffle [True,False]
```
Ex : ```python split_script.py --image_folder /home/my_folder/images --csv_path /home/my_folder/data.csv --separate_folders True --class_folders True --dest_folder /home/my_folder/images/split_images/ --train_size 0.6 --test_size 0.3 --val_size 0.1, --shuffle True```

Arguments :

- image_folder - Path to directory where images are stored
- csv_path - CSV file location
- separate_folders (optional) - True or False - Create new folders for training, testing and validation images after split or not (default = True)
- class_folders (optional, required if `separate_folders` is given as `True`) - True or False - Create new folders for each class of images under train, test, and val folders (default = False)
- dest_folder (optional, required if `separate_folders` is given as `True`) - Path to where new folders should be created. If nothing is given, the new folders are created in image_folder - Path for train, test, and val folders
- train_size - Fraction of number of training images. Example - 0.6 or 0.5 or 0.7
- test_size - Fraction of number of testing images. Example - 0.3 or 0.4 or 0.2
- val_size - Fraction of number of validation images. Example - 0.1 or 0.2 or 0.3
- shuffle (optional) - True or False - Shuffle dataset before splitting or not (default = True)

## Drawing Bounding Boxes

```shell
python draw_bb.py --csv /path/to/csv --image_folder /path/to/folder/containing/images --save_images [True,False] --dest_folder /path/to/save/annotated/images --wait int
```
Ex : ```python draw_bb.py --csv /home/my_folder/data.csv --image_folder /home/my_folder/images --save_images True --dest_folder /path/to/save/annotated/images --wait 2000``` 

Arguments :
- image_folder - Path to directory where images are stored
- csv - CSV file location
- save_images (optional) - True or False - Save annotated images or not
- dest_folder (optional, required if `save_images` is given as `True`) - Path to where new folders should be created. If nothing is given, the new folders are created in `image_folder`
- wait (optional) - Number of milliseconds to display the image (default = 0 - image is displayed till a key is pressed)

## Image Information

```shell
python img_info_new.py --image_folder /path/to/folder/containing/images --save_as /path/to/save/csv --decimal_places int
```
Ex : ```python img_info_new.py --image_folder /home/my_folder/images --save_as /home/my_folder/info.csv --decimal_places 3```

Arguments :
- image_folder - Path to directory where images are stored
- save_as - Path where CSV file with image information should be stored 
- decimal_places (optional) - Number of places to round off to (default = 2)

