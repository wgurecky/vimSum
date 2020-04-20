#!/bin/bash
##
# Before execution:
# Ensure to clone vimSum repo to ~/.nvim/.
##

# test VisMult
VisMult_inp=VisMult.inp.txt
VisMult_gold=VisMult.gold.txt

nvim -u test_config.vim -c ":UpdateRemotePlugins" -c ":VisualLine" -c ":VisMult(2.0, 5e)" VisMult.inp.txt -c wq VisMult.out.txt
diff VisMult.gold.txt VisMult.out.txt

# test VisMath
VisMath_inp=VisMath.inp.txt
VisMath_gold=VisMath.gold.txt

# test with parens around args
nvim -u test_config.vim -c ":UpdateRemotePlugins" -c ":VisualLine" -c ":VisMath(2.0*(x), 5e)" VisMult.inp.txt -c wq VisMult.out.txt
diff VisMult.gold.txt VisMult.out.txt

# test without parens around args
nvim -u test_config.vim -c ":UpdateRemotePlugins" -c ":VisualLine" -c ":VisMath 2.0*(x) 5e" VisMult.inp.txt -c wq VisMult.out.txt
diff VisMult.gold.txt VisMult.out.txt
