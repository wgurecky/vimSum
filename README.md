VimSum
======

VimSum is a collection of scripts that perform basic arithmetic 
on visually selected numbers in vim.

![GIF Demo](https://raw.github.com/wgurecky/vimSum/master/example/example_use.gif)

The scripts can be used on columns of numbers by selecting them in visual mode.
The scripts also can operate on mixed number/word paragraphs (only operating on
numbers).
The format of numbers in text may also be adjusted using the ``VisMult`` or
``VisMath`` script.

Common use cases:

- Multiply many numbers by a constant.  Encountered when changing units.
- Compute sum or mean of column in text file and immediately paste result back into text.
- Perform basic arithmetic on a column of numbers.
- Change format of numbers in text e.g. from scientific notation to decimal format.

Install
=======

Vim must be compiled with ``+python`` support.

If using [vim-plug](https://github.com/junegunn/vim-plug) add the following to
`.vimrc`.

    Plug 'https://github.com/wgurecky/vimSum.git'

USE
===

1. Select text using visual mode.
2. Invoke one of the commands below.  Ex: ``:'<, '>VisMath(2*exp(x), 2f)``

### VisSum ###

Return the sum of all visually selected numbers.
The result is stored in the ``"@0"`` register, so you can paste
the result via ``"0p``

### VisMean ###

Identical to ``VisSum`` but will compute the mean of
all visually selected numbers.

### VisMult ###

Multiply all visually selected number by a constant.  Format
may be specified as an optional second argument.  ex: ``4e`` for 4
digit decimal sci notation.  ``2f`` for two decimal floating str format.
Example use:

    :VisMult(2.0, 2f)

will multiply all selected values by 2.0, format the result to include 2 digits
trailing the decimal and change the current buffer in-place.

### VisMath ###

Evaluate any simple mathematical expression of a single variable
denoted by a character
enclosed in parenthesis: ``(x)``.  Values from the visually selected text will be
injected into the formula and the completed expression will be evaluated.  ex::

    :VisMath(0.5*cos(x)+2.0*exp(x), 4e)

__Note__:
If using whitespace in a formula string make sure to use an escape char before:
ex:  ``VisMath(0.5*cos(x)\ +\ exp(x), 4e)``

TODO
====

Automatically detect max required floating point print precision in ``VisMult`` by
default

In-place buffer change may not be desired.  Perhaps display edited buffer in new
window??

