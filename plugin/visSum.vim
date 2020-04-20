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

" TODO:
" Define VisSum provided commands in vim8
