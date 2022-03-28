# QuickAR
![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)


## Description

Easy to implement AR-tag library for python based on opencv aruco library.
* locate ar tag in image
* inscribe image over ar tag
* inscribe image between ar tags
* get relitive positional information on ar tag
* calibrate camera for above

## Table of Contents 

- [Usage](#usage)
- [Credits](#credits)
- [License](#license)

## Usage

Example code can be found under examples.

## Credits

[Ian Sodersjerna](https://github.com/plop91)

## Tests

Testing is not currently slated for this project.

## License

GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

## Worklog:

### 3/20/2022 : 

#### Overview
Created package structure, added detector, renderer, generate_marker and aruco_dict all with basic functions.
#### Current State:
Currently, successfully building, generate marker is functional, detector is functional but will occasionally detect 
phantom objects particularly on glass, and renderer will render a saved image of a marker over the existing marker 
however this functionality is not yet working correctly.
#### Files/Functions created:
* aruco_dict.py - used to initialize aruco dict
  * N/A
* detector.py (async)- used tolocate aruco markers 
  * detect - takes a frame and returns found aruco tags
  * draw_markers - draw markers on frame
* generate_marker.py - used to generate aruco markers
  * generate - greate a marker with  the given id
* renderer.py - used to render images onto markers
  * apply_homography - return homography information 
#### Testing:
Test files have been created but no tests have been written.
##### Testing environment:
* Windows 10 Desktop(high-end)
* Python 3.7
* Walfront 2k webcam
* 2 inch markers of type DICT_ARUCO_ORIGINAL id's 1 and 2