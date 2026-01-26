"""
Author: 
    Inspyre Softworks

Project:
    MIDIDiff

File: 
    midi_diff/cli/completions.py
 

Description:
    Shell completion script generation for the MIDIDiff CLI.

"""
from __future__ import annotations

from typing import Final, Iterable

SUPPORTED_SHELLS: Final[frozenset[str]] = frozenset({"bash", "zsh", "fish"})


def emit_completion_script(
    shell: str,
    commands: Iterable[str],
    flags: Iterable[str],
) -> str:
    """
    Generate a shell completion script for the given shell.

    Parameters
    ----------
    shell:
        Target shell name (bash, zsh, fish).
    commands:
        Iterable of supported subcommands.
    flags:
        Iterable of supported top-level flags.

    Returns
    -------
    str
        The completion script content.
    """
    if shell not in SUPPORTED_SHELLS:
        supported = ", ".join(sorted(SUPPORTED_SHELLS))
        raise ValueError(f"Unsupported shell '{shell}'. Supported shells: {supported}")

    commands_list = " ".join(sorted(commands))
    flags_list = " ".join(sorted(flags))

    if shell == "bash":
        return f"""# Bash completion for midi-diff
_midi_diff_completions() {{
    local cur prev
    COMPREPLY=()
    cur="{{COMP_WORDS[COMP_CWORD]}}"
    prev="{{COMP_WORDS[COMP_CWORD-1]}}"

    if [[ $COMP_CWORD -eq 1 ]]; then
        COMPREPLY=($(compgen -W "{commands_list}" -- "$cur"))
        return 0
    fi

    case "{{COMP_WORDS[1]}}" in
        diff)
            if [[ $COMP_CWORD -le 4 ]]; then
                COMPREPLY=($(compgen -f -- "$cur"))
            fi
            ;;
        upgrade)
            COMPREPLY=($(compgen -W "--pre" -- "$cur"))
            ;;
        completion)
            COMPREPLY=($(compgen -W "bash zsh fish" -- "$cur"))
            ;;
        *)
            COMPREPLY=($(compgen -W "{flags_list}" -- "$cur"))
            ;;
    esac
}}
complete -F _midi_diff_completions midi-diff
"""

    if shell == "zsh":
        return f"""#compdef midi-diff

_midi_diff() {{
    local -a commands
    commands=({commands_list})

    _arguments \\
        "1: :->command" \\
        "*::arg:->args"

    case $state in
        command)
            _values 'midi-diff commands' $commands
            ;;
        args)
            case $words[2] in
                diff)
                    _arguments "2:First MIDI file:_files" "3:Second MIDI file:_files" "4:Output MIDI file:_files"
                    ;;
                upgrade)
                    _values 'upgrade options' --pre
                    ;;
                completion)
                    _values 'shell' bash zsh fish
                    ;;
                *)
                    _values 'flags' {flags_list}
                    ;;
            esac
            ;;
    esac
}}

_midi_diff "$@"
"""

    # fish
    return f"""# Fish completion for midi-diff
complete -c midi-diff -n "not __fish_seen_subcommand_from {commands_list}" -s V -l version -d "Show version and environment info"
complete -c midi-diff -n "not __fish_seen_subcommand_from {commands_list}" -s h -l help -d "Show help"

complete -c midi-diff -n "__fish_use_subcommand" -a "{commands_list}" -d "midi-diff commands"

complete -c midi-diff -n "__fish_seen_subcommand_from diff" -a "(__fish_complete_path)" -d "MIDI file path"
complete -c midi-diff -n "__fish_seen_subcommand_from upgrade" -l pre -d "Include pre-release versions"
complete -c midi-diff -n "__fish_seen_subcommand_from completion" -a "bash zsh fish" -d "Target shell"
"""


__all__ = ["emit_completion_script", "SUPPORTED_SHELLS"]
