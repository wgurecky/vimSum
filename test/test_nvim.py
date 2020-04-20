import pynvim
from pynvim import attach
import sys
import os
sys.path.append("../rplugin/python3/.")
from visSum import VimSumPlug

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
