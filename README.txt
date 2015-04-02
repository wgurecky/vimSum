INSTALL
=======

Use pathogen, or place in ~/.vim/plugins/.


USE
===

VisSum will return the sum of all visually selected numbers.
The result is stored in the "@0" register, so you can paste
the result via "0p

VisMean is identical to the above but will comput the mean of
all visually selected numbers.

VisMult will multiply all visually selected number by a constant.
ex:

VisMult(2.0) 

Will multipy all selected values by 2.0, and change the current buffer in-place.

TODO
====

Automatically detect floating point print precission in VisMult

In-place buffer change may not be desired.  Perhaps display edited buffer in new
window??



