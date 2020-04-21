" plugin/visSum.vim
if !has('python3')
    echo 'Error: VimSum requires python3, pynvim and neovim OR vim8'
    finish
endif

" User defined verbosity setting for vimSum
let g:vimSumVerbose = 0

" No need to use yarp if using nvim
if has('nvim')
    finish
endif

" Define VisSum provided commands in vim8
let s:vsplug = yarp#py3('visSum_wrap')

" Wrap python plugin fns
func! FVisSum()
    return s:vsplug.call('vis_sum')
endfunc

func! FVisMean()
    return s:vsplug.call('vis_mean')
endfunc

func! FVisMult(...)
    return s:vsplug.call('vis_mult', a:1, a:2)
endfunc

func! FVisMath(...)
    return s:vsplug.call('vis_math', a:1, a:2)
endfunc

" Create aliases to wrapped vim functions
command! -range -register VisSum call FVisSum()
command! -range -register VisMean call FVisMean()
command! -range -register -nargs=* VisMult call FVisMult(<f-args>)
command! -range -register -nargs=* VisMath call FVisMath(<f-args>)
