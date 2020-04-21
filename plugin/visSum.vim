" plugin/visSum.vim
if !has('python3')
    echo 'Error: Requires python3, pynvim and neovim OR vim8 compiled with +python'
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

" Create aliases to wrapped vim functions
command! -range -register VisSum call FVisSum()
command! -range -register VisMean call FVisMean()
