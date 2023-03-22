from scheme_eval_apply import *
from scheme_utils import *
from scheme_classes import *
from scheme_builtins import *

#################
# Special Forms #
#################

"""
How you implement special forms is up to you. We recommend you encapsulate the
logic for each special form separately somehow, which you can do here.
"""

class SpecialFormBase:

    name = None

    def __init__(self) -> None:
        pass

class SF_Define(SpecialFormBase):

    name = "define"

    def __init__(self) -> None:
        super().__init__()
        self.