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
import webbrowser
from typing import Final, Sequence
from midi_diff.core import main as core_main
from midi_diff.cli.version import (
    print_version_info,
    print_debug_info,
    check_for_updates_command,
    upgrade_package,
    UPDATE_CHECK_ENV_VAR,
)


# Subcommand names - single source of truth for CLI commands
# These are referenced by both build_parser() and backward compatibility logic
COMMAND_DIFF: Final[str] = 'diff'
COMMAND_DEBUG_INFO: Final[str] = 'debug-info'
COMMAND_CHECK_UPDATES: Final[str] = 'check-updates'
COMMAND_UPGRADE: Final[str] = 'upgrade'
COMMAND_DOCS: Final[str] = 'docs'

# Flag definitions - single source of truth for CLI flags
# These are referenced by both build_parser() and backward compatibility logic
FLAG_VERSION_SHORT: Final[str] = '-V'
FLAG_VERSION_LONG: Final[str] = '--version'
FLAG_HELP_SHORT: Final[str] = '-h'
FLAG_HELP_LONG: Final[str] = '--help'

# Known subcommands and flags for backward compatibility.
# These sets are derived from the constants above to ensure they stay
# synchronized with the parser configuration in build_parser().
KNOWN_COMMANDS: Final[frozenset[str]] = frozenset({COMMAND_DIFF, COMMAND_DEBUG_INFO, COMMAND_CHECK_UPDATES, COMMAND_UPGRADE, COMMAND_DOCS})
KNOWN_FLAGS: Final[frozenset[str]] = frozenset({FLAG_VERSION_SHORT, FLAG_VERSION_LONG, FLAG_HELP_SHORT, FLAG_HELP_LONG})


class VersionAction(argparse.Action):
    """Custom argparse action to print version info and exit."""
    
    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str | Sequence[str] | None,
        option_string: str | None = None,
    ) -> None:
        print_version_info()
        parser.exit()


def open_documentation() -> None:
    """
    Open MIDIDiff documentation in the user's default web browser.
    
    Opens http://mididiff.readthedocs.io/en/latest/ in the system's
    default web browser.
    """
    url = "http://mididiff.readthedocs.io/en/latest/"
    print(f"Opening documentation at {url}")
    webbrowser.open(url)


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
        FLAG_VERSION_SHORT,
        FLAG_VERSION_LONG,
        action=VersionAction,
        nargs=0,
        help=(
            f"Show version and environment info "
            f"(set {UPDATE_CHECK_ENV_VAR} to a truthy value like '1', 'true', or 'yes' to check for updates)."
        ),
    )
    
    # Create subparsers for subcommands
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands',
    )
    
    # diff subcommand (main functionality)
    diff_parser = subparsers.add_parser(
        COMMAND_DIFF,
        help='Compare two MIDI files and output their differences'
    )
    diff_parser.add_argument("file_a", help="Path to the first MIDI file.")
    diff_parser.add_argument("file_b", help="Path to the second MIDI file.")
    diff_parser.add_argument("out_file", help="Path for the diff MIDI output.")
    
    # debug-info subcommand (no additional arguments needed)
    subparsers.add_parser(
        COMMAND_DEBUG_INFO,
        help='Display diagnostic and environment information'
    )
    
    # check-updates subcommand (explicitly check for updates)
    subparsers.add_parser(
        COMMAND_CHECK_UPDATES,
        help='Check for available updates from PyPI'
    )
    
    # upgrade subcommand (upgrade the package)
    upgrade_parser = subparsers.add_parser(
        COMMAND_UPGRADE,
        help='Upgrade midi-diff to the latest version from PyPI'
    )
    upgrade_parser.add_argument(
        '--pre',
        action='store_true',
        help='Include pre-release versions in the upgrade'
    )
    
    # docs subcommand (open documentation in browser)
    subparsers.add_parser(
        COMMAND_DOCS,
        help='Open MIDIDiff documentation in your default web browser'
    )
    
    return parser


def run_cli(argv: Sequence[str] | None = None) -> None:
    """
    Main CLI entry point for MIDIDiff.

    Parameters:
        argv: Command-line arguments to parse. If None, defaults to sys.argv[1:].
              Accepts any sequence of strings (e.g., list, tuple) for testability.

    Usage:
        midi-diff fileA.mid fileB.mid output.mid  (assumes 'diff' subcommand)
        midi-diff diff fileA.mid fileB.mid output.mid
        midi-diff debug-info
        midi-diff --version

    """
    parser = build_parser()
    
    # Default to sys.argv[1:] if no argv provided
    if argv is None:
        argv = sys.argv[1:]
    
    # Combine known commands and flags for backward compatibility check
    known_subcommands_and_flags = KNOWN_COMMANDS | KNOWN_FLAGS
    
    # Backward compatibility: If first arg isn't a known subcommand/flag,
    # assume it's a file path and prepend 'diff' to make it work with the new structure.
    # Argparse will handle validation of the actual arguments.
    if len(argv) > 0 and argv[0] not in known_subcommands_and_flags:
        argv = [COMMAND_DIFF] + list(argv)
    
    args = parser.parse_args(argv)
    
    # Handle subcommands
    if args.command == COMMAND_DIFF:
        core_main(args.file_a, args.file_b, args.out_file)
    elif args.command == COMMAND_DEBUG_INFO:
        print_debug_info()
    elif args.command == COMMAND_CHECK_UPDATES:
        check_for_updates_command()
    elif args.command == COMMAND_UPGRADE:
        upgrade_package(include_pre=args.pre)
    elif args.command == COMMAND_DOCS:
        open_documentation()
    else:
        # No subcommand provided - show help
        parser.print_help()
        sys.exit(1)


__all__ = ["run_cli", "build_parser"]
