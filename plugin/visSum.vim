" plugin/visSum.vim

if !has('python3')
    echo 'Error: Requires python3, pynvim and neovim OR vim8 compiled with +python'
    finish
endif

" User defined verbosity setting for vimSum
let g:vimSumVerbose = 0

if has('nvim')
    finish
endif

" Define VisSum provided commands in vim8
let s:vsplug = yarp#py3('visSum_wrap')

func! VisSum(v)
    return s:vsplug.call('vis_sum', a:v)
endfunc

func! VisMean(v)
    return s:vsplug.call('vis_mean', a:v)
endfunc
