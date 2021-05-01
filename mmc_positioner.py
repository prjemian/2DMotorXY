"""
Mock MMC support in ophyd/Bluesky
"""

from ophyd import Signal
from ophyd import SoftPositioner
from sim_mmc_controller import SimMMC
import time


class MMC_Positioner(SoftPositioner):
    """Connect MMC controller as ``ophyd.SoftPositioner``."""
    mmc = SimMMC()
    mmc_wait_poll_interval_s = 0.01
    mmc_timeout_s = 10

    def __init__(self, *args, mmc_label="", **kwargs):
        kwargs["source"] = "MMC 2D XY Stage Controller"
        self.mmc_wait_label = mmc_label
        super().__init__(*args, **kwargs)

    def _set_position(self, value, **kwargs):
        self.mmc.setXYPosition(value)
        self._started_moving = True
        self._moving = True

        time_expires = time.time() + self.mmc_timeout_s
        while self.mmc.waitForDevice(self.mmc_wait_label):
            if time.time() > time_expires:
                raise TimeoutError(
                    f"Timeout waiting {timeout:f}s for {self.name}"
                )
            time.sleep(self.mmc_wait_poll_interval_s)

        self._started_moving = False
        self._moving = False

        self._position = self.mmc.getXYPosition()

    def get(self, **kwargs):
        '''The readback value'''
        self._readback = self.mmc.getXYPosition()
        return self._readback


def demonstrate_mmc_positioner(mmc):
    # What's it look like?
    print(f"{mmc = }")

    # Will it set()?
    st = mmc.set((2.1, -.1))
    print(f"{st = }")
    while not st.done:
        time.sleep(0.26)
        print(f"{st = }")
    print(f"{mmc = }")

    # Will it get()?
    try:
        print(f"{mmc.get() = }")
    except Exception as exc:
        print(f"{exc = }")

    # Will it put()?
    try:
        t0 = time.time()
        print(f"{mmc.put((4, .2)) = }")
        print(f"{time.time()-t0:f}s")
        print(f"{mmc = }")
    except Exception as exc:
        print(f"{exc = }")

    # Will it read()?
    print(f"{mmc.read() = }")

    # Will it move()?
    try:
        t0 = time.time()
        print(f"{mmc.move((.6, -.7)) = }")
        print(f"{time.time()-t0:f}s")
        print(f"{mmc = }")
        print(f"{mmc.position = }")
    except Exception as exc:
        print(f"{exc = }")
