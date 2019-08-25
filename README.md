# V5 Upload Utility
This python script provides simple batch uploading of PROS projects to the Vex V5 microcontroller. This was used by team 114T during the 2018-2019 season for autonomous selection and code management.

## Usage
**Optional Arugments:**
* ```auton``` provide a unique project idenitifier (if none is provided all projects will be compiled and uploaded)

``` bash
# Compile and upload all projects
python upload.py

# Compile and upload project id 1
python upload.py 1
```
