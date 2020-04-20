import pynvim
from pynvim import attach
import sys
import os
sys.path.append("../rplugin/python3/.")
from visSum import VimSumPlug

def vis_mult_test():
    # create nvim instance
    nvim = attach('child', argv=["env", "nvim", "--embed", "--headless"])

    # load the input file
    nvim.command("edit VisMult.inp.txt")

    # Initilize vimsum plugin
    vsp = VimSumPlug(nvim)

    # set visual mode marks
    nvim.feedkeys("m<")
    nvim.feedkeys("$")
    nvim.feedkeys("m>")

    # Execute VisMult
    args = ['2.0', '5e']
    range = [1, 1]
    vsp.vis_mult(args, range)

    # Write resulting file out
    nvim.command("wq! VisMult.out.txt")
    nvim.close()

def vis_math_test():
    # create nvim instance
    nvim = attach('child', argv=["env", "nvim", "--embed", "--headless"])

    # load the input file
    nvim.command("edit VisMult.inp.txt")

    # Initilize vimsum plugin
    vsp = VimSumPlug(nvim)

    # set visual mode marks
    nvim.feedkeys("m<")
    nvim.feedkeys("$")
    nvim.feedkeys("m>")

    # Execute VisMult
    args = ['2.0*(x)', '5e']
    range = [1, 1]
    vsp.vis_math(args, range)

    # Write resulting file out
    nvim.command("wq! VisMath.out.txt")
    nvim.close()

if __name__ == "__main__":
    vis_mult_test()
    vis_math_test()
