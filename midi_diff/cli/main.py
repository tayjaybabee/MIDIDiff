"""
Author: 
    Inspyre Softworks

Project:
    MIDIDiff

File: 
    midi_diff/cli/main.py
 

Description:
    Main CLI logic and argument parsing for MIDIDiff.

"""
import argparse
import sys
from midi_diff.core import main as core_main
from midi_diff.cli.version import print_version_info, print_debug_info, UPDATE_CHECK_ENV_VAR


class VersionAction(argparse.Action):
    """Custom argparse action to print version info and exit."""
    
    def __call__(self, parser, namespace, values, option_string=None):
        print_version_info()
        parser.exit()


def build_parser() -> argparse.ArgumentParser:
    """
    Build and return the argument parser for MIDIDiff CLI.
    
    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        prog='midi-diff',
        description="MIDIDiff - Compare MIDI files and output their differences.",
    )
    parser.add_argument(
        "-V",
        "--version",
        action=VersionAction,
        nargs=0,
        help=(
            f"Show version and environment info "
            f"(set {UPDATE_CHECK_ENV_VAR} to a truthy value like '1', 'true', or 'yes' to check for updates)."
        ),
    )
    
    # Create subparsers for subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # diff subcommand (main functionality)
    diff_parser = subparsers.add_parser(
        'diff',
        help='Compare two MIDI files and output their differences'
    )
    diff_parser.add_argument("file_a", help="Path to the first MIDI file.")
    diff_parser.add_argument("file_b", help="Path to the second MIDI file.")
    diff_parser.add_argument("out_file", help="Path for the diff MIDI output.")
    
    # debug-info subcommand (no additional arguments needed)
    subparsers.add_parser(
        'debug-info',
        help='Display diagnostic and environment information'
    )
    
    return parser


def _get_known_subcommands_and_flags(parser: argparse.ArgumentParser) -> frozenset:
    """
    Extract known subcommands and flags from parser configuration.
    
    This dynamically generates the set of known commands and flags to avoid
    hardcoding and keep it synchronized with the actual parser configuration.
    
    Parameters:
        parser: Configured ArgumentParser instance
        
    Returns:
        Frozenset of known subcommands and flag strings
    """
    known = set()
    
    # Add top-level optional flags
    for action in parser._actions:
        if action.option_strings:
            known.update(action.option_strings)
    
    # Add subcommand names
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            known.update(action.choices.keys())
    
    return frozenset(known)


def run_cli() -> None:
    """
    Main CLI entry point for MIDIDiff.

    Usage:
        midi-diff fileA.mid fileB.mid output.mid  (assumes 'diff' subcommand)
        midi-diff diff fileA.mid fileB.mid output.mid
        midi-diff debug-info
        midi-diff --version

    """
    parser = build_parser()
    
    # Get known subcommands and flags dynamically from parser
    known_subcommands_and_flags = _get_known_subcommands_and_flags(parser)
    
    # Backward compatibility: If first arg isn't a known subcommand/flag,
    # assume it's a file path and prepend 'diff' to make it work with the new structure.
    # Argparse will handle validation of the actual arguments.
    if len(sys.argv) > 1 and sys.argv[1] not in known_subcommands_and_flags:
        sys.argv.insert(1, 'diff')
    
    args = parser.parse_args()
    
    # Handle subcommands
    if args.command == 'diff':
        core_main(args.file_a, args.file_b, args.out_file)
    elif args.command == 'debug-info':
        print_debug_info()
    else:
        # No subcommand provided - show help
        parser.print_help()
        sys.exit(1)


__all__ = ["run_cli", "build_parser"]
