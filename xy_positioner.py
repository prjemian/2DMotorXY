from ophyd import Component
from ophyd import PseudoPositioner
from ophyd import PseudoSingle
from ophyd import SoftPositioner
from ophyd.pseudopos import pseudo_position_argument
from ophyd.pseudopos import real_position_argument

class TwoD_XY_StagePositioner(PseudoPositioner):

    # The pseudo positioner axes:
    x = Component(PseudoSingle, target_initial_position=True)
    y = Component(PseudoSingle, target_initial_position=True)

    # The real (or physical) positioners:
    # pair = Component(SoftPositioner)
    pair = Component(SoftMMCPositioner, mmc=mmc)

    @pseudo_position_argument
    def forward(self, pseudo_pos):
        """Run a forward (pseudo -> real) calculation (return pair)."""
        return self.RealPosition(pseudo_pos)

    # @real_position_argument
    def inverse(self, real_pos):
        """Run an inverse (real -> pseudo) calculation (return x & y)."""
        if len(real_pos) == 1:
            if real_pos.pair is None:
                x, y = self.pair.mmc.xy
            else:
                x, y = tuple(real_pos.pair)
        elif len(real_pos) == 2:
            x, y = real_pos
        else:
            raise ValueError(
                f"Incorrect argument: {self.name}.inverse({real_pos})"
            )
        return self.PseudoPosition(x=x, y=y)
