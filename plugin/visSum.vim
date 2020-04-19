if !has('python3')
    echo 'Error: Requires pynvim and neovim OR vim8 compiled with +python'
    finish
    if !has('nvim')
        let s:visSum = yarp#py3('visSum')
        " check for remote plugin compat
        echo 'Requires remote plugin shim for vim8. Install nvim-yarp.'
    endif
endif

" User defined verbosity setting for vimSum
let g:vimSumVerbose = 1

" Define VisSum provided commands
" command! -range -register VisSm call VisSum(1)
" command! -range -register VisAvg call VisMean()
" command! -range -register -nargs=* VisEval call VisMath(<f-args>)
" command! -range -register -nargs=* VisMlt call VisMult(<f-args>)
