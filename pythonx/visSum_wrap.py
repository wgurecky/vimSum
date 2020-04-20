import os
import sys
sys.path.append("../rplugin/python3/.")
from visSum import VisSumPlug as _Vsp
import vim

_obj = _Vsp

def vis_sum(*args):
    return _obj.vis_sum(args)

def vis_mean(*args):
    return _obj.vis_mean(args)
