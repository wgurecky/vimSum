#!/bin/bash

# test VisMult
python test_nvim.py
diff VisMult.gold.txt VisMult.out.txt
