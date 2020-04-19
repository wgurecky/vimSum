#!/usr/bin/python
##
# Performs basic Arithmetic on visually selected areas in
# vim8 or neovim
##
from __future__ import print_function, division, absolute_import
import re
import math
from math import *
try:
    import vim
except:
    import pynvim as vim


def op_vis_sel_words_in_buf(b, callback_word_fn, mod_in_place=False, **kwargs):
    """
    Operates on visually selected lines and
    words in current buffer
    Args:
        b (pynvim.api.Buffer): python buffer
    Returns:
        words in visual selection
    """
    assert hasattr(callback_word_fn, '__call__')
    starty, startx = vim.current.buffer.mark('<')
    endy, endx = vim.current.buffer.mark('>')
    lines = b[starty - 1:endy]
    for i, line in enumerate(lines):
        # selected portion of current line
        sel_line = line[startx:endx+1]
        sel_line = ''.join(sel_line)
        # split sel_line string into words
        vis_sel_words = sel_line.split()
        new_line_buffer = ''
        for word in vis_sel_words:
            cleanWord = word.strip('.,')
            callback_result = callback_word_fn(cleanWord, **kwargs)
            try:
                new_line_buffer += callback_result
            except:
                pass
        if mod_in_place:
            # for modification in-place
            endline = line[endx+1:]
            begline = line[:startx]
            new_line_buffer += endline
            new_line_buffer = begline + new_line_buffer
            b[starty - 1 + i] = new_line_buffer


def vis_sum():
    """
    Computes sum of all vis sel numbers
    """
    buf = vim.current.buffer
    global out_nums
    out_nums = []

    def _append_vis_nums(word, **kwargs):
        try:
            out_nums.append(float(word))
        except:
            pass
        return ''
    try:
        op_vis_sel_words_in_buf(buf, _append_vis_nums, mod_in_place=False)
        out_sum = sum(out_nums)
        print(out_sum)
        out_string = "'" + str(out_sum) + "'"
        vim.command("let @0="+out_string)
    except:
        print("An unexpected error occured.")


def vis_mean():
    """
    Computes mean of all vis sel numbers
    """
    buf = vim.current.buffer
    global out_nums
    out_nums = []

    def _append_vis_nums(word, **kwargs):
        try:
            out_nums.append(float(word))
        except:
            pass
        return ''
    try:
        op_vis_sel_words_in_buf(buf, _append_vis_nums, mod_in_place=False)
        out_mean = sum(out_nums) / len(out_nums)
        print(out_mean)
        out_string = "'" + str(out_mean) + "'"
        vim.command("let @0="+out_string)
    except:
        print("An unexpected error occured.")


def vis_mult(m, a):
    """
    Multiply all vis selected numbers by a const
    Modifies buffer in-place by default
    Args:
        m (float): multiplier
        a (str): output number format ex: '5f'
    """
    buf = vim.current.buffer
    m = float(str(m).strip(',()'))
    fmt = '5e'
    try:
        # allow user specified number format
        # TODO: support fmt = 'auto'
        fmt = str(a).strip('.,()')
    except:
        pass

    def _vis_mult(word, **kwargs):
        try:
            new_word = str('{:.' + fmt + '}').format(float(word) * m)
        except:
            new_word = word
        new_word += ' '
        return new_word

    try:
        op_vis_sel_words_in_buf(buf, _vis_mult, mod_in_place=True)
    except:
        print("An unexpected error occured.")


def vis_math(m, a):
    """
    Performs Arithmetic on all vis sel numbers
    Modifies buffer in-place by default
    Args:
        m (str): math string to eval ex: '2.0*pi*(x)'
        a (str): output number format ex: '5f'
    """
    m = str(m).strip('," ')  # strip commas from fomula str
    m = re.search("\(?(.*)", m).group(1)  # strip leading ( from formula if present
    try:
        # TODO: support fmt = 'auto'
        fmt = str(a).strip('.,()')
    except:
        fmt = '5e'

    def evalFormula(maths, word, depth=0):
        completeForm = re.sub(r"\(\w?\)", "(" + str(word) + ")", maths)
        print("CompleteForm: " + completeForm)
        if completeForm == maths:
            print("Failed to find var in expression: " + maths)
        else:
            try:
                evaluatedExpr = eval(completeForm)
                if vim.eval("g:vimSumVerbose") == '1' or vim.eval("g:vimSumVerbose") == True:
                    print("Evaluated Expression: " + maths + " : where x=" + str(word))
                else:
                    pass
                return float(evaluatedExpr)
            except:
                if depth == 0:
                    evalFormula(maths + ')', word, depth=1)
                else:
                    pass

    def _vis_math(word, **kwargs):
        try:
            new_word = str('{:.' + fmt + '}').format(evalFormula(m, word))
        except:
            # print("no math done on line %d" % (i))
            new_word = word
        new_word += ' '
        return new_word

    try:
        op_vis_sel_words_in_buf(buf, _vis_math, mod_in_place=True)
    except:
        print("An unexpected error occured.")


def find_sigfigs(x):
    """
    helper function to automatically determine max sig figs in a number
    from: https://stackoverflow.com/questions/8142676/python-counting-significant-digits
    """
    # change all the 'E' to 'e'
    x = x.lower()
    if ('e' in x):
        # return the length of the numbers before the 'e'
        myStr = x.split('e')
        return len( myStr[0] ) - 1 # to compenstate for the decimal point
    else:
        # put it in e format and return the result of that
        ### NOTE: because of the 8 below, it may do crazy things when it parses 9 sigfigs
        n = ('%.*e' %(8, float(x))).split('e')
        # remove and count the number of removed user added zeroes. (these are sig figs)
        if '.' in x:
            s = x.replace('.', '')
            #number of zeroes to add back in
            l = len(s) - len(s.rstrip('0'))
            #strip off the python added zeroes and add back in the ones the user added
            n[0] = n[0].rstrip('0') + ''.join(['0' for num in range(l)])
        else:
            #the user had no trailing zeroes so just strip them all
            n[0] = n[0].rstrip('0')
        #pass it back to the beginning to be parsed
    return find_sigfigs('e'.join(n))

