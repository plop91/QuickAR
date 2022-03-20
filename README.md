# QuickAR
## Author 
Ian Sodersjerna
## GOAL
Create an easy to implement AR-tag library for python

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