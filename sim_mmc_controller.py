"""
Simulate MMC controller with random image data.

Only implement the xy axes and produce a random image.
"""

import numpy as np
import time

class SimMMC:
    """This is a simulated microscope that returns a 512x512 image."""
    pixels = (512, 512)

    def __init__(self):
        self.pos = 0
        self.xy = [0, 0]
        self.exposure_time = 0.1
        # self.data = io.imread("sim_data/DAPI.tif")
        self.data = np.random.rand(*self.pixels)

    def getCameraDevice(self):
        return "SimCamera"

    def getFocusDevice(self):
        return "SimFocus"

    def snapImage(self):
        time.sleep(self.exposure_time)
        return

    def setPosition(self, value):
        self.pos = value
        return

    def getPosition(self):
        return self.pos

    def setXYPosition(self, value):
        self.xy = value
        return

    def getXYPosition(self):
        return self.xy

    def waitForDevice(self, label):
        time.sleep(1)
        return

    def getImage(self):
        # return frame_crop(self.data)
        return self.data


def demonstrate_mmc(mmc):
    """Put this class through its paces."""
    print(f"{mmc.getPosition() = }")
    print(f"{mmc.getXYPosition() = }")
    # print(f"{ = }")

    print(f"{mmc.setXYPosition((5,4)) = }")
    print(f"{mmc.getPosition() = }")
    print(f"{mmc.getXYPosition() = }")
    
    print(f"{mmc.getCameraDevice() = }")
    
    t0 = time.time()
    mmc.waitForDevice("ignore this label")
    print(f"waitForDevice() completed in {time.time()-t0}s")
