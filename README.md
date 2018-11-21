# PyShift
##### A Kinect-based Doppler shift demonstration
Seth Stubbs and Morgan Rehnberg

### Dependencies
- freenect (OpenKinect)
- python_libfreenect (freenect python wrapper)
- OpenCv2 & python_opencv2
- Python 3.7

### How to use
```
python3 pyshift.py <inputimage>
```
You can specify which image by the command-line. If no input image is given, input.jpg in the current directory will be used.
    
### Configuration
There are a number of options that can be tweaked in pyshift.py
    
### Scale
X_SCALE and Y_SCALE can both be used to stretch or downscale the image. 
    
For example, if you have an image that is 1400x1200 you can scale it down by setting 

```
X_SCALE = 0.5
Y_SCALE = 0.5
```
        
so that the image is being rendered at 700x600, which should increase performance.
        
# Flash Fix
On low-power systems (such as the raspberry pi) it is advised you enable the flash fix to smooth your frames.

```
FLASH_FIX = True
```

This should make a better effect when framerates are low.

### Debug Mode
This prints out some debug-related log information.

```
DEBUG = True
```
