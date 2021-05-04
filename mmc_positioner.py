"""
Mock MMC support in ophyd/Bluesky
"""

from ophyd import Component
from ophyd import Signal
from ophyd.mixins import SignalPositionerMixin
from ophyd.status import MoveStatus
from sim_mmc_controller import SimMMC
import threading
import time
import warnings

class SoftMMCPositioner(SignalPositionerMixin, Signal):

    _move_thread = None

    def __init__(self, *args, mmc=None, mmc_label="", **kwargs):
        self.mmc = mmc
        self.mmc_label = mmc_label

        super().__init__(*args, set_func=self._write_xy, **kwargs)

        # get the position from the controller on startup
        self._readback = self.mmc.getXYPosition()

    def _write_xy(self, value, **kwargs):
        if self._move_thread is not None:
            # The MoveStatus object defends us; this is just an additional safeguard.
            # Do not ever expect to see this warning.
            warnings.warn("Already moving.  Will not start new move.")
        st = MoveStatus(self, target=value)

        def moveXY():
            self.mmc.setXYPosition(value)
            # ALWAYS wait for the device
            self.mmc.waitForDevice(self.mmc_label)

            # update the _readback attribute (which triggers other ophyd actions)
            self._readback = self.mmc.getXYPosition()

            # MUST set to None BEFORE declaring status True
            self._move_thread = None
            st.set_finished()

        self._move_thread = threading.Thread(target=moveXY)
        self._move_thread.start()
        return st


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
