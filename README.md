# PyShift
##### A Kinect-based Doppler shift demonstration
Seth Stubbs and Morgan Rehnberg

### Effect
Place a Kinect sensor around waist-height, with a display above. As users walk towards the display, the image will appear to be blue-shifted. As the user backs away, the image will appear red-shifted.

### Dependencies
- `freenect` (OpenKinect)
- `python_libfreenect` (freenect Python wrapper)
- `OpenCv2` & `python_opencv2`
- Python 3.7

### How to use
```
python3 pyshift.py <inputimage>
```
You can specify which image to display with the command line. If no input image is given, `input.jpg` in the current directory will be used.
    
### Configuration
There are a number of options that can be tweaked in pyshift.py
    
#### Scale
`X_SCALE` and `Y_SCALE` can both be used to stretch or downscale the image. 
    
For example, if you have an image that is 1400x1200 you can scale it down by setting 

```python
X_SCALE = 0.5
Y_SCALE = 0.5
```
        
so that the image is being rendered at 700x600, which should increase performance.
        
#### Flash Fix
On less powerful systems (such as the Raspberry Pi) enabling the flash fix will result in a less-stuttery output.

```python
FLASH_FIX = True
```

This should make a better effect when framerates are low.

#### Debug Mode
This prints out some debug-related log information.

```python
DEBUG = True
```
