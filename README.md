# How to encode a 2D motor (XY stage) with ophyd?

The 2D motor operates with an `(x, y)` tuple rather than separate
controls for each axis.  The controller supports these methods for the
XY stage (in addition to methods supporting other features):

* `getXYPosition())`
* `setXYPosition((x,y))`
* `waitForDevice(label)`

## Strategy

class | subclass | purpose | notebook
:--- | :--- | :--- | :---
`SimMMC` | | simulate MMC controller | [demonstrate_SimMMC_controller](https://nbviewer.jupyter.org/github/prjemian/2DMotorXY/blob/main/demonstrate_SimMMC_controller.ipynb)
`MMC_Positioner` | `ophyd.SoftPositioner` | connect `SimMMC` with ophyd | [demonstrate_MMC_Positioner](https://nbviewer.jupyter.org/github/prjemian/2DMotorXY/blob/main/demonstrate_MMC_Positioner.ipynb)
`TwoD_XY_StagePositioner` | `ophyd.PseudoPositioner` | (NOT WORKING YET) add separate x & y axis controls for scans | [demonstrate_TwoD_XY_StagePositioner](https://nbviewer.jupyter.org/github/prjemian/2DMotorXY/blob/main/demonstrate_TwoD_XY_StagePositioner.ipynb)

## Additional

**Python motor simulator** : 
    [SimAxis](https://nbviewer.jupyter.org/github/prjemian/2DMotorXY/blob/main/reference/SimAxis.ipynb): simulate a positioning motor in pure Python
