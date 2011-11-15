#!/bin/bash

# Filters given arguments list and produces an array containing "no-options"
# (argument prefixed with -) and options.
# Input: COMP_WORDS global array must be defined
# Output:
#   __no_opts global array, __no_opts[0] is the name of the application
#   __opts global array
_filter_options()
{
    local index_no_opts=0
    local index_opts=0
    for w in ${COMP_WORDS[@]}
    do
        if [[ ${w} != -* ]]
        then
            __no_opts[${index_no_opts}]=${w}
            ((index_no_opts++))
        else
            __opts[${index_opts}]=${w}
            ((index_opts++))
        fi
    done
}

_setup()
{
    declare -a __no_opts
    declare -a __opts
}

_clean()
{
    unset __no_opts
    unset __opts
}

_cortex_client()
{
    local cur opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"

    #
    #  Cortex-client's options.
    #
    opts=`${COMP_WORDS[0]} --options`
    if [[ ${cur} == -* ]] ; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi

    _setup
    _filter_options

    #
    #  Cortex-client's resources and services.
    #
    local resources=`${__no_opts[0]} --resources`

    local resource=${__no_opts[1]}
    local action=${__no_opts[2]}

    #  Complete resources if no action is yet given
    if [[ ${resource} == ${cur} ]]
    then
        COMPREPLY=( $(compgen -W "${resources}" -- ${cur}) )
        _clean
        return 0
    fi

    #  Complete action if no argument is yet given
    if [[ ${action} == ${cur} ]]
    then
        local actions
        actions=`${__no_opts[0]} ${resource} __available_actions`
        if [[ $? == 0 ]]
        then
            COMPREPLY=( $(compgen -W "${actions}" -- ${cur}) )
        fi
        _clean
        return 0
    fi

    #  Complete parameters
    if [[ (${cur} != ${resource}) && (${cur} != ${action}) ]]
    then
        local params
        params=`${__no_opts[@]} --completions`
        if [[ $? == 0 ]]
        then
            COMPREPLY=( $(compgen -W "${params}" -- ${cur}) )
        fi
        _clean
        return 0
    fi

   _clean
   return 0
}

complete -F _cortex_client cortex-client