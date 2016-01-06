if !has('python')
    finish
endif

fun! SumNumbers_Float()
python << EOF

import vim

try:
    b = vim.current.buffer
    starty, startx = vim.current.buffer.mark('<')
    endy, endx = vim.current.buffer.mark('>')
    lines = b[starty - 1:endy]
    outNums = []
    for line in lines:
        line = line[startx:endx+1]
        # concatenate all characters in a line into a line string
        line = ''.join(line)
        # split line string into words
        words = line.split()
        for word in words:
            # if the word is a number, add to the sum
            try:
                outNums.append(float(word.strip('.,')))
            except:
                pass
    print(sum(outNums))
    outstring = "'" + str(sum(outNums)) + "'"
    vim.command("let @0="+outstring)
except:
    print("An unexpected error occured.")
EOF

endfun

fun! MeanNumbers_Float()
python << EOF

import vim

try:
    b = vim.current.buffer
    starty, startx = vim.current.buffer.mark('<')
    endy, endx = vim.current.buffer.mark('>')
    lines = b[starty - 1:endy]
    outNums = []
    for line in lines:
        line = line[startx:endx+1]
        # concatenate all characters in a line into a line string
        line = ''.join(line)
        # split line string into words
        words = line.split()
        for word in words:
            # if the word is a number, add to the sum
            try:
                outNums.append(float(word.strip('.,')))
            except:
                pass
    print(sum(outNums) / len(outNums))
    outstring = "'" + str(sum(outNums) / len(outNums)) + "'"
    vim.command("let @0="+outstring)
except:
    print("An unexpected error occured.")
EOF

endfun


fun! MultNumbers_Float_v2(m, ...)
python << EOF

import vim
import math

def precision_and_scale(x):
    max_digits = 14
    int_part = int(abs(x))
    magnitude = 1 if int_part == 0 else int(math.log10(int_part)) + 1
    if magnitude >= max_digits:
        return (magnitude, 0)
    frac_part = abs(x) - int_part
    multiplier = 10 ** (max_digits - magnitude)
    frac_digits = multiplier + int(multiplier * frac_part + 0.5)
    while frac_digits % 10 == 0:
        frac_digits /= 10
    scale = int(math.log10(frac_digits))
    return (magnitude + scale, scale)

# get argument from vim
m = float(vim.eval("a:m").strip(',()'))
fmt = '5e'
try:
    # allow user specified number format
    fmt = str(vim.eval("a:1").strip('.,()'))
except:
    pass

try:
    b = vim.current.buffer
    starty, startx = vim.current.buffer.mark('<')
    endy, endx = vim.current.buffer.mark('>')
    lines = b[starty - 1:endy]
    for i, line in enumerate(lines):
        modline = line[startx:endx+1]
        endline = line[endx+1:]
        begline = line[:startx]
        # concatenate all characters in a line into a line string
        modline = ''.join(modline)
        # split line string into words
        words = modline.split()
        newbuffer = ''
        for word in words:
            cleanWord = word.strip('.,')
            try:
                if word == cleanWord:
                    newbuffer += str('{:.' + fmt + '}').format(float(cleanWord) * m)
                else:
                    newbuffer += str('{:.' + fmt + '}').format(float(cleanWord) * m) + '.'
            except:
                newbuffer += word 
            newbuffer += ' '
        newbuffer += endline
        newbuffer = begline + newbuffer
        vim.current.buffer[starty - 1 + i] = newbuffer
except:
    print("An unexpected error occured.")
EOF

endfun


fun! Restruct_Cols(colWidth)
python << EOF

import vim

# get argument from vim
colWidth = vim.eval("a:colWidth").strip('()')

try:
    b = vim.current.buffer
    starty, startx = vim.current.buffer.mark('<')
    endy, endx = vim.current.buffer.mark('>')
    lines = b[starty - 1:endy]
    outList = []
    # collect words into flat array
    for line in lines:
        try:
            outList += line.split()
        except:
            pass
    # restructure array into n number of cols
    restructTable, newRowString = [], ""
    for i, word in enumerate(outList):
        newRowString += word + "  "
        if (i + 1) % int(colWidth) == 0:
            restructTable.append(newRowString)
            newRowString = ""
    restructTable.append(newRowString)
    vim.command("split ResCol")
    b = vim.buffers[-1]
    b.append(restructTable)
    vim.command("set buftype=nofile")
except:
    print("Ensure valid block")
EOF

endfun

fun! MathNumbers_Float(m, ...)
python << EOF

import vim
import re
from math import *

m = str(vim.eval("a:m").strip(','))  # strip commas from fomula str
m = re.search("\(?(.*)\)", m).group(1)  # strip leading ( from formula if present
fmt = '5e'
try:
    fmt = str(vim.eval("a:1").strip('.,()'))
except:
    pass

def evalFormula(maths, word):
    # might be missing a closing ) at the end of function string... maybe not?
    try:
        return float(eval(re.sub(r"\(\w?\)", "(" + str(word) + ")", maths + ')')))
    except:
        return float(eval(re.sub(r"\(\w?\)", "(" + str(word) + ")", maths)))

try:
    b = vim.current.buffer
    starty, startx = vim.current.buffer.mark('<')
    endy, endx = vim.current.buffer.mark('>')
    lines = b[starty - 1:endy]
    for i, line in enumerate(lines):
        modline = line[startx:endx+1]
        endline = line[endx+1:]
        begline = line[:startx]
        # concatenate all characters in a line into a line string
        modline = ''.join(modline)
        # split line string into words
        words = modline.split()
        newbuffer = ''
        for word in words:
            cleanWord = word.strip('.,')
            try:
                if word == cleanWord:
                    newbuffer += str('{:.' + fmt + '}').format(evalFormula(m, cleanWord))
                else:
                    newbuffer += str('{:.' + fmt + '}').format(evalFormula(m, cleanWord)) + '.'
            except:
                newbuffer += word 
            newbuffer += ' '
        newbuffer += endline
        newbuffer = begline + newbuffer
        vim.current.buffer[starty - 1 + i] = newbuffer
except:
    print("An unexpected error occured.")
EOF

endfun

command! -range -register -nargs=1 ResCol call Restruct_Cols(<f-args>)
command! -range -register -nargs=* VisMath call MathNumbers_Float(<f-args>)
command! -range -register -nargs=* VisMult call MultNumbers_Float_v2(<f-args>)
command! -range -register VisSum call SumNumbers_Float()
command! -range -register VisMean call MeanNumbers_Float()
