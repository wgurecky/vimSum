[![Build Status](https://travis-ci.org/wgurecky/vimSum.svg?branch=master)](https://travis-ci.org/wgurecky/vimSum)

VimSum
======

VimSum provides a collection of vim commands that perform basic arithmetic
on visually selected numbers in neovim or vim.

![GIF Demo](https://raw.github.com/wgurecky/vimSum/master/example/example_use.gif)

The arithmetic operations can be used on columns of numbers by selecting them in visual mode.
The routines also can operate on mixed number/word paragraphs (only operating on numbers).
The format of numbers in text may also be adjusted using this plugin, which allows easily
switching between scientific notation and decimal representations. See the ``VisMult`` example.

Common use cases:

- Multiply numbers in text by a constant.  Encountered when changing units.
- Compute sum or mean of column in text file and immediately paste result back into text.
- Perform basic arithmetic on a column of numbers.
- Change format of numbers in text e.g. from scientific notation to decimal format.

Install
=======

### Neovim ###

Requirements:

- python3
- pynvim

Ensure the [pynvim](https://github.com/neovim/pynvim) python package is installed:

    pip install pynvim

If using [vim-plug](https://github.com/junegunn/vim-plug) add the following to
`.vimrc`.

    Plug 'https://github.com/wgurecky/vimSum.git', { 'do' : 'vim +UpdateRemotePlugins +qall' }


### Vim8 ###

Using vimSum with vim8 requires a remote plugin compatibility shim provided by
the nvim-yarp plugin:

    Plug 'https://github.com/wgurecky/vimSum.git'
    Plug 'roxma/nvim-yarp'

USE
===

1. Select text using visual mode.
2. Invoke one of the commands below.

    Ex: ``:'<, '>VisMath(2*exp(x), 2f)``

### :VisSum ###

Return the sum of all visually selected numbers.
The result is stored in the ``"@0"`` register, so you can paste
the result via ``"0p``

### :VisMean ###

Identical to ``VisSum`` but will compute the mean of
all visually selected numbers.

### :VisMult ###

Multiply all visually selected number by a constant.  Format
may be specified as an optional second argument.  ex: ``4e`` for 4
digit decimal sci notation.  ``2f`` for two decimal floating str format.
Example use:

    :VisMult(2.0, 2f)

will multiply all selected values by 2.0, format the result to include 2 digits
trailing the decimal and change the current buffer in-place.

For just changing the format from decimal representation to scientific; select
a block of text in visual mode and then run:

    :VisMult(1.0, 5e)

### :VisMath ###

Evaluate any simple mathematical expression of a single variable
denoted by a character
enclosed in parenthesis: ``(x)``.  Values from the visually selected text will be
injected into the formula and the completed expression will be evaluated.  ex::

    :VisMath(0.5*cos(x)+2.0*exp(x), 4e)

__Note__:
If using whitespace in a formula string make sure to use an escape char before:
ex:  ``VisMath(0.5*cos(x)\ +\ exp(x), 4e)``

Example Config
=====

It might be useful to create the following, or similar, aliases to the above
functions in the vimrc:

    " aliases
    xnoremap <leader>s :VisSum
    xnoremap <leader>a :VisMean
    cnoreabbrev vm VisMult
    cnoreabbrev ve VisMath

    " set verbosity
    let g:vimSumVerbose = 1
