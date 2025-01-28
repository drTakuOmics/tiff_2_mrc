tiff_2_mrc
================
Short pipeline to convert .tiff files produced by WVU EM scope to mrc so they can be uploaded and processed by  CryoSPARC

## Converting EM.tiff to mrc for CryoSPARC:

What: You received warnings or errors from CryoSPARC during upload of your images or during the conversion of TIFF files to MRC format in IMOD due to null bytes in the ImageDescription metadata collected from the WVU-EM scope.
Why: Null bytes can lead to data truncation and incorrect reading of metadata, which can affect subsequent processing.

### check_tiff_metadata to identify problematic files:
By using the Pillow library (PIL) we created a script to scan the TIFF files in a specific directory.
The script was designed to systematically check each file for null bytes the common problem from ou EM in WVU.

### Detecting Null Bytes:

The script check_tiff_metadata opens each TIFF file, access the ImageDescription metadata, and checks for null bytes.
This step targets which files are problematic, ensuring only those files needed further action.

### Cleaning the Metadata:

Upon finding null bytes, the script removes them from the ImageDescription and saved a new version of the file.
Cleaning the metadata is necessary to prevent conversion errors with IMOD and maintain the integrity of the image's information for correct upload to CryoSparc.

### Verifying Results:

After processing, the script provided a summary of cleaned files.
This confirmation helped ensure that all problematic files were addressed, making it clear which files were successfully cleaned.

### Summary:
By automating the detection and cleaning of null bytes in TIFF file metadata, you effectively resolve the warnings encountered during file conversion with IMOD and other tools. This method not only corrected the immediate issue but also established a reliable process for handling similar problems in the future.

## Requirements

- Python and the library PIL 
- IMOD version compatible with CUDA installed

## Installation

If you have python and IMOD you can run this script by downloading the file check_tiff_metadata located in this folder.

## Conversion after cleaning.
After the files are cleaned run one of the following commands in your folder to perform the conversion to .mrc, you will need IMOD installed

1. for %f in (*.tif) do tif2mrc "%f" "%~nf.mrc"  

2. foreach ($a in Get-ChildItem *.tif) { & "C:\\YourPath\\IMOD\bin\tif2mrc.exe" -B 0 $a.FullName ".\$($a.BaseName).mrc"

## License

The code is freely available to download and run, but it’s protected and
licensed under a [Creative Commons Attribution-ShareAlike 4.0
International License](https://creativecommons.org/licenses/by-nc/4.0/),
meaning you can use it but citing it’s source.

[![License: CC BY-NC
4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
