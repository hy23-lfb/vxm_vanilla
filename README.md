# Masterarbeit
Master thesis repository of Harsha Yogeshappa, RWTH Aachen University.

## Folder heirarchy
```
├───docs
│   ├───Official_Documents                                # All the official documents (including application and confimration).
│   └───Resource_Documents                                # All files gathered across internet that might be relevant for thesis.
│       ├───Books
│       │   ├───PyTorch
│       │   ├───SciPy_and_NumPy
│       │   └───TensorFlow
│       ├───Documents                                     # Documents found to be useful.
│       │   ├───Keynote                                   # Key points and the references .
│       │   ├───Machine_Learning_Mastery                  # Materials from machinelearningmastery.com
│       │   │   └───Figures
│       │   ├───Miscellaneous                             # Files that cannot be specifically categorized.
│       │   │   ├───Images
│       │   │   ├───Pdfs
│       │   │   ├───Txts
│       │   │   └───Xlsx
│       │   └───TensorFlow                                # Files related to TensorFlow.
│       ├───Google_Colab_Programs
│       ├───Latex_Tutorial                                # Tutorial to write a latex file.
│       ├───Research_Papers                               # Research Papers.
│       │   └───Finished
│       └───Thesis_Reports                                # Thesis reports of friends and acquaintances.
│           ├───Bharath
│           └───Muddasser
├───presentations                                         # slides and resources for md file.
│   ├───13.07.2022
│   ├───resources
│   └───Template
├───src                                                   # utility scripts for windows and linux platforms.
│   ├───linux
│   │   └───utils
│   │       ├───py
│   │       └───sh
│   └───windows
│       └───utils
│           ├───matlab
│           ├───py
│           └───sh
└───voxelmorph                                             # Voxelmorph submodule.
    ├───.github
    │   └───ISSUE_TEMPLATE
    ├───data
    ├───scripts
    │   ├───tf
    │   └───torch
    └───voxelmorph
        ├───py
        ├───tf
        │   └───utils
        └───torch
```

## Get the pipeline running.

### 1. Perform affine registration [mandatory requirement for Voxelmorph network]
- **Step1: Perform affine registration using `larvalign_affine` branch on git.**
    1. Use the `larvalign_affine` branch in the "larvalign" repository to perform an affine registration.
    2. In the root directory of "larvalign" repository, you should find a text file named "affine_list.txt".
        - This file contains a list with the full paths of the images that need to be affine registered in the atlas.
        - The result is stored as a zip file in the RegisteredScans/TIFF/
- **Step2: Unzip the files using matlab script `unzip_larvalign_output.m`**
    1. Contents will be directly extracted to the root directory (a new folder won't be created).

### 2. Perform scaling on all the images to get a uniform size.
- **Step1: Auto scaling to required dimensions using `callAutoScaleImages.m`**
    1. Once the zip files are extracted and tif files are available, use the matlab script `callAutoScaleImages.m` to generate macro for Fiji to output a scaled np channel only of the affine aligned tiff images.
    2. `callAutoScaleImages.m` accepts the path of the tif files only and it will internally read all the files and passes it to 'autoScaleImages.m'

### 3. Perform Registration.
Both the registrations need to happen on the scaled-np-channel images to compare the results.
- #### Voxelmorph registration:
    - **Step1: Voxelmorph need npz files as input: Use the files available in `scaled-np-channel\`.**
        1. Use the python script, `create-npz.py`, available in "masterarbeit" repository ('D:\Harsha\repo\Masterarbeit\src\windows\utils\py') to obtain npz files from the scaled tif files.
        2. **Note:** 
        - The values are scaled down between 0.0 and 1.0 as per voxelmorph's requirement.
    - **Step2: Once all the npz files are available, prepare a list with the full paths of the images.**
        1. Store the list in the following directory as '/home/students/yogeshappa/repo/Masterarbeit/src/linux/list.txt' to run on cluster.
        2. Store the list in the following directory as '/home/students/yogeshappa/repo/Masterarbeit/src/windows/list.txt' to run locally on windows.
    - **Step3: Train the voxelmorph network using the below command.**
        ```py
        /home/students/yogeshappa/miniconda3/bin/python3 /home/students/yogeshappa/repo/Masterarbeit/voxelmorph/scripts/tf/train.py --img-list /home/students/yogeshappa/repo/Masterarbeit/src/linux/list.txt --atlas /home/students/yogeshappa/repo/Masterarbeit/dataset/atlas/np_atlas_scaled.npz --model-dir /work/scratch/yogeshappa/masterarbeit_out/model --epochs 500 --steps-per-epoch 66
        # steps_per_epoch = len(training_data) / batch_size.
        # len(training_data) = 66.
        ```
    - **Step4: Perform nonlinear registration using trained model weights.**
        1. Use the python script, `register_all.py`, available in "masterarbeit" repository ('D:\Harsha\repo\Masterarbeit\src\windows\utils\py') to extract zip files to folders to register all the images.
        2. In the following directory, "I:\masterarbeit_dataset\01.larvalign_data-affine_registered", you must find a text file named "Voxelmorph_list.txt". Use this to tell `register_all.py` to give the list with the full paths of the images that needs to be aligned.
        ```py
        python D:\Harsha\repo\Masterarbeit\src\windows\utils\py\register_all.py --file-list I:\00.masterarbeit_dataset\04.Affine_Registered\01.larvalign_data-Affine_Registered\Voxelmorph_list.txt --gpu 0 --fixed I:\00.masterarbeit_dataset\00.atlas\np-scaled-channel\npz\np_atlas_scaled.npz --model I:\03.masterarbeit_out\experiment\256x512x64\model\0100.h5 --out-path I:\03.masterarbeit_out\experiment\256x512x64\out --warp True
        ```
        3. In any case, if you need to perform single prediction then use the below command.
        ```py
        D:\Harsha\repo\Masterarbeit\voxelmorph\scripts\tf\register.py --moving I:\masterarbeit_dataset\01.larvalign_data-affine_registered\tiff\scaled-np-channel\npz\np_brain3_scaled.npz --fixed I:\masterarbeit_dataset\00.atlas\tif\npz\np_atlas_scaled.npz --moved I:\tensorflow_out\out\moved.npz --model I:\tensorflow_out\model\0223.h5 --gpu 0
        ```
- #### Larvalign registration:
    - **Step1: Use the files available in `scaled-np-channel\` directory to perform nonlinear registration.**
        1. Use the `voxelmorph_nonlinear` branch in the "larvalign" repository to perform an affine + nonlinear registration.
        2. In the following directory, "I:\masterarbeit_dataset\data", you must find a text file named "larvalign_list.txt".
            - This file contains a list with the full paths of the images that need to be nonlinear registered in the atlas.
            - The result is stored as a zip file in the /RegisteredScans/TIFF/
        3. **Note:** Though the input is 1 channel (np channel), output still composes of 3 channels: np-channel, nt-channel(empty), and ge-channel(empty).
    - **Step2: Unzip the files using matlab script `unzip_larvalign_output.m`**
        1. Contents will be directly extracted to the root directory (a new folder won't be created).
            
### 4. Preperation for evaluating the registration results.
- #### Larvalign registration:
    - **Step1: Convert 3 channel tif files to 1 channel tif file using matlab script `call_splitChannels_and_saveNP.m`**
        1. Generates macro for Fiji tool.
            - After running Fiji, the result is stored in the `./np-channel/ directory`, relative to tif files.
    - **Step2: Generate MIP out of these np-channel only tif files.**
        1. Use matlab script, `traverse_and_find_tif.m`, to generate mip files.
            - The result is stored in the `./np-channel/ directory`, relative to the tif files.
    ```
    ───lrv_registered
       └───zip
           │   np_brain0_scaled.tif.zip
           │
           └───tiff
               │   np_brain0_scaled.tif
               │
               └───np-channel
                   │   np_brain0_scaled.tif
                   │
                   └───mip
                           np_brain0_scaled.tif
    ```
- #### Voxelmorph registration:
    - **Step1: Voxelmorph output npz files: Convert npz files to mat files.**
        1. Use the python script, `convert-npz-to-mat-all.py`, available in "masterarbeit" repository ('D:\Harsha\repo\Masterarbeit\src\windows\utils\py') to convert all npz files into mat files.
            - The python script expects the path of the file where all npz files are present not a list like other scripts.
            - The result is stored in the `./mat/ directory`, relative to the npz files.
    - **Step2: Convert matfiles to tiff images.**
        1. Use matlab script, `mat_to_tiff.m`, to convert all .mat variables into a .tif file image.
            - The result is stored in the `./tif/ directory`, relative to the mat files.
    - **Step3: Fix the image properties of these tiff images.**
    These tif files that are created using the matlab script has resolution set in 'pixels' instead of 'mm'. For error measure, it is critical that the physical properties of the images are the same as of atlas's and larvalign_registered images'.
        1. Use matlab script, `callFix_tif_properties.m`, to generate a macro for Fiji tool that sets the right properties.
            - The result is stored in the './np-channel/ directory', relative to the tif files.
    - **Step4: Generate MIP out of these np-channel only tif files.**
        1. Use matlab script, `traverse_and_find_tif.m`, to generate mip files.
            - The result is stored in the `./np-channel/ directory`, relative to the tif files.
    ```
    ───vxm_registered
       └───npz
           │   moved_np_brain0_scaled.npz
           │
           └───mat
               │   moved_np_brain0_scaled.mat
               │
               └───tiff
                   │   np_brain0_scaled.tif
                   │
                   └───np-channel
                       │   np_brain0_scaled.tif
                       │
                       └───mip
                               np_brain0_scaled.tif
    ```
### 4. Evaluate registration results.
Use the function `visuallyEvaluate.m` matlab script to plot and report the mattes mutual information metric.
![MAX_np_brain4_scaled](https://user-images.githubusercontent.com/46209868/179960514-578eb76a-cd86-424d-bc88-475abbfa1141.png)
