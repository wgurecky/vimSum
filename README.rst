VimSum
======

VimSum is collection of simple scripts that provide the ability to perform basic calculations in vim.
The scripts can be used on columns of numbers by selecting them in visual mode.
The scripts also can operate on mixed number/word paragraphs (only operating on
numbers).
The format of numbers in text may also be adjusted using the ``VisMult`` or
``VisMath`` script.

Common use cases:

    - Multiply many numbers by a constant.  Encountered when changing units.
    - Compute sum or mean of column in text file and immediately paste result back into text.
    - Change format of numbers in text e.g. from scientific notation to decimal format.

Install
=======

Vim must be compiled with ``+python`` support.

USE
===

1) Select text using visual mode.
2) Envoke one of the below scripts.  Ex: ``:'<, '>VisMath(2*exp(x), 2f)``

``VisSum`` will return the sum of all visually selected numbers.
The result is stored in the ``"@0"`` register, so you can paste
the result via ``"0p``

``VisMean`` is identical to ``VisSum`` but will comput the mean of
all visually selected numbers.

``VisMult`` will multiply all visually selected number by a constant.  Format
may be specified as an optional second argument.  ex: ``4e`` for 4
digit decimal sci notation.  ``2f`` for two decimal floating str format.
ex::

    VisMult(2.0, 2f) 

will multipy all selected values by 2.0, and change the current buffer in-place.

``VisMath`` will take any simple mathmatical expression of a single variable
denoted by a character
enclosed in parenthesis: ``(x)``.  Values from the visually selected text will be
injected into the formula and the completed expression will be evaluated.  ex::

    VisMath(0.5*cos(x) + 2.0*exp(x), 4e)

TODO
====

Automatically detect max required floating point print precission in VisMult by
default

In-place buffer change may not be desired.  Perhaps display edited buffer in new
window??

