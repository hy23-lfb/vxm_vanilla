# Useful commands.[^format]


## Command to find a specific string in files and directories.
### **grep -Rw ./ -e 'def load_volfile'**
1. -R: tells **grep** to read all files in all the directories recursively.[^1]
2. -w: instructs **grep** to select only those lines containing matches that form whole words.[^1]
3. -e: is used to specify the string (pattern) to be searched.[^1]

## Command to find number of files in a directory.
### **ls -1 | wc -l**
1. -1 (The numeric digit "one".) Force output to be one entry per line. This is the default when output is not to a terminal.
2. wc stands for word count; -l stands for new line count.

## Commands to register all images and generate mip files.
python commands
```py
python Y:\repo\Masterarbeit\src\windows\utils\py\register_all.py --file-list I:\00.masterarbeit_dataset\04.Affine_Registered\01.larvalign_data-Affine_Registered\Voxelmorph_list.txt --gpu 0 --fixed I:\00.masterarbeit_dataset\00.atlas\np-scaled-channel\npz\np_atlas_scaled.npz --model I:\03.masterarbeit_out\experiment\256x512x64_config_V2_noNorm\model\0029.h5 --out-path I:\03.masterarbeit_out\experiment\256x512x64_config_V2_noNorm\out

python Y:\repo\Masterarbeit\src\windows\utils\py\convert-npz-to-mat-all.py --file-path I:\03.masterarbeit_out\experiment\256x512x64_config_V2_noNorm\out
```
matlab commands
```Matlab
mat_filepath = 'I:\03.masterarbeit_out\experiment\256x512x64\out\mat';
tif_filepath = [mat_filepath '\tiff'];
mat_to_tiff(mat_filepath);
traverse_and_find_tif(tif_filepath);
```

--------
[^1]: https://www.tecmint.com/find-a-specific-string-or-word-in-files-and-directories/
[^format]: https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax
