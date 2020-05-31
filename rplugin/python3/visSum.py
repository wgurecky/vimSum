#!/usr/bin/python
##
# Performs basic Arithmetic on visually selected areas in
# vim8 or neovim
##
from __future__ import print_function, division, absolute_import
import re
import math
from math import *
import pynvim


@pynvim.plugin
class VimSumPlug(object):
    def __init__(self, vim):
        self.vim = vim

    @staticmethod
    def op_vis_sel_words_in_buf(buf, callback_word_fn, mod_in_place=False, **kwargs):
        """
        Operates on visually selected lines and
        words in current buffer
        Args:
            buf (pynvim.api.Buffer): buffer
        Returns:
            words in visual selection
        """
        assert hasattr(callback_word_fn, '__call__')
        starty, startx = buf.mark('<')
        endy, endx = buf.mark('>')
        lines = buf[starty - 1:endy]
        for i, line in enumerate(lines):
            # selected portion of current line
            sel_line = line[startx:endx+1]
            sel_line = ''.join(sel_line)
            # split sel_line string into words
            vis_sel_words = re.split(',| ', sel_line)
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
                buf[starty - 1 + i] = new_line_buffer

    @pynvim.command("VisSum", range='', sync=False)
    def vis_sum(self, range):
        """
        Computes sum of all vis sel numbers
        """
        buf = self.vim.current.buffer
        global out_nums
        out_nums = []

        def _append_vis_nums(word, **kwargs):
            try:
                out_nums.append(float(word))
            except:
                pass
            return ''
        try:
            self.op_vis_sel_words_in_buf(buf, _append_vis_nums, mod_in_place=False)
            out_sum = sum(out_nums)
            self.vim.out_write(str(out_sum) + "\n")
            out_string = "'" + str(out_sum) + "'"
            self.vim.command("let @0="+out_string)
        except:
            self.vim.out_write("VisSum: An unexpected error occured." + "\n")


    @pynvim.command("VisMean", range='', sync=False)
    def vis_mean(self, range):
        """
        Computes mean of all vis sel numbers
        """
        buf = self.vim.current.buffer
        global out_nums
        out_nums = []

        def _append_vis_nums(word, **kwargs):
            try:
                out_nums.append(float(word))
            except:
                pass
            return ''
        try:
            self.op_vis_sel_words_in_buf(buf, _append_vis_nums, mod_in_place=False)
            out_mean = sum(out_nums) / len(out_nums)
            self.vim.out_write(str(out_mean) + "\n")
            out_string = "'" + str(out_mean) + "'"
            self.vim.command("let @0="+out_string)
        except:
            self.vim.out_write("VisMean: An unexpected error occured." + "\n")


    @pynvim.command("VisMult", range='', nargs='*', sync=False)
    def vis_mult(self, args, range):
        """
        Multiply all vis selected numbers by a const
        Modifies buffer in-place by default
        Args:
            m (float): multiplier
            a (str): output number format ex: '5f'
        """
        m, a = args[0], args[1]
        buf = self.vim.current.buffer
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
            self.op_vis_sel_words_in_buf(buf, _vis_mult, mod_in_place=True)
        except:
            self.vim.out_write("VisMult: An unexpected error occured." + "\n")


    @pynvim.command("VisMath", range='', nargs='*', sync=False)
    def vis_math(self, args, range):
        """
        Performs Arithmetic on all vis sel numbers
        Modifies buffer in-place by default
        Args:
            m (str): math string to eval ex: '2.0*pi*(x)'
            a (str): output number format ex: '5f'
        """
        m, a = args[0], args[1]
        buf = self.vim.current.buffer
        m = str(m).strip('," ')  # strip commas from fomula str
        m = re.search("\(?(.*)", m).group(1)  # strip leading ( from formula if present
        try:
            # TODO: support fmt = 'auto'
            fmt = str(a).strip('.,()')
        except:
            fmt = '5e'

        def evalFormula(maths, word, depth=0):
            completeForm = re.sub(r"\(\w?\)", "(" + str(word) + ")", maths)
            if self.vim.eval("g:vimSumVerbose") == '1' or self.vim.eval("g:vimSumVerbose") == True:
                self.vim.out_write("Math Expression: " + completeForm + "\n")
            if completeForm == maths:
                self.vim.out_write("Failed to find var in expression: " + maths + "\n")
            else:
                try:
                    evaluatedExpr = eval(completeForm)
                    if self.vim.eval("g:vimSumVerbose") == '1' or self.vim.eval("g:vimSumVerbose") == True:
                        self.vim.out_write("Evaluated Expression: " + maths + " : where x=" + str(word) + "\n")
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
                # self.vim.out_write("no math done on line %d" % (i) + "\n")
                new_word = word
            new_word += ' '
            return new_word

        try:
            self.op_vis_sel_words_in_buf(buf, _vis_math, mod_in_place=True)
        except:
            self.vim.out_write("VisMath: An unexpected error occured." + "\n")


def find_sigfigs(x):
    """
    helper function to automatically determine max sig figs in a number
    from: https://stackoverflow.com/questions/8142676/python-counting-significant-digits
    """
    # change all the 'E' to 'e'
    x = x.lower()
    if ('e' in x):
        myStr = x.split('e')
        # to compenstate for the decimal point
        return len( myStr[0].replace(',', ''))
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

