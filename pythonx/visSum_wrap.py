from visSum import VimSumPlug as _Vsp
import vim

_obj = _Vsp(vim)

def vis_sum(*args):
    return _obj.vis_sum(args)

def vis_mean(*args):
    return _obj.vis_mean(args)
