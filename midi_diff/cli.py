"""
Author: 
    Inspyre Softworks

Project:
    MIDIDiff

File: 
    midi_diff/cli.py
 

Description:
    Command-line interface for MIDIDiff to compare two MIDI files and output their differences.

"""
import argparse
import json
import os
import platform
import sys
import urllib.error
import urllib.request
from importlib import metadata
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from midi_diff.core import main

DIST_NAME = "midi-diff"
PYPI_JSON_URL = f"https://pypi.org/pypi/{DIST_NAME}/json"

# Update check configuration
UPDATE_CHECK_ENV_VAR = "MIDIFF_CHECK_UPDATES"
UPDATE_CHECK_TRUTHY_VALUES = ("1", "true", "yes")

# Known subcommands and flags for backward compatibility check
KNOWN_SUBCOMMANDS_AND_FLAGS = frozenset(['diff', 'debug-info', '-V', '--version', '-h', '--help'])


class VersionAction(argparse.Action):
    """Custom argparse action to print version info and exit."""
    
    def __call__(self, parser, namespace, values, option_string=None):
        _print_version_info()
        parser.exit()


def _get_version() -> str:
    return _get_metadata_version(DIST_NAME, "unknown")


def _get_dependency_version(name: str) -> str:
    return _get_metadata_version(name, "not installed")


def _get_metadata_version(name: str, fallback: str) -> str:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return fallback


def _check_for_update(current_version: str) -> str:
    try:
        with urllib.request.urlopen(PYPI_JSON_URL, timeout=5) as response:
            payload = json.load(response)
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, json.JSONDecodeError) as exc:
        return f"Update check failed: {exc}"

    latest = payload.get("info", {}).get("version")
    if not latest:
        return "Update check failed: missing version metadata."
    if latest == current_version:
        return "Up to date."
    return f"Update available: {latest} (installed {current_version})."


def _print_version_info() -> None:
    console = Console()
    current_version = _get_version()

    markdown_text = f"""
# Version Information

**MIDIDiff:** {current_version}

----

**Python:** {platform.python_version()}  
**Platform:** {platform.platform()}  

----

**mido:** {_get_dependency_version('mido')}  
**rich:** {_get_dependency_version('rich')}
""".strip()

    md = Markdown(markdown_text)

    panel = Panel(
        md,
        border_style='blue',
        padding=(1, 2),
    )

    console.print(panel)

    # Only check for updates if explicitly enabled via environment variable
    if os.getenv(UPDATE_CHECK_ENV_VAR, '').lower() in UPDATE_CHECK_TRUTHY_VALUES:
        update_msg = _check_for_update(current_version)

        if 'Update available' in update_msg:
            console.print(f'[yellow]⚠ {update_msg}[/yellow]')
        elif 'Up to date' in update_msg:
            console.print(f'[green]✓ {update_msg}[/green]')
        else:
            console.print(f'[red]{update_msg}[/red]')
    else:
        console.print(
            f'[dim]Update check disabled '
            f'(set {UPDATE_CHECK_ENV_VAR}=1 to enable).[/dim]'
        )


def _print_debug_info() -> None:
    """Print comprehensive debug information in Rich Markdown format."""
    console = Console()
    
    # Get all version information
    mididiff_version = _get_version()
    python_version = platform.python_version()
    platform_info = platform.platform()
    mido_version = _get_dependency_version('mido')
    rich_version = _get_dependency_version('rich')
    
    # Get environment information
    cwd = os.getcwd()
    
    # Collect relevant environment variables
    path_env = os.getenv('PATH', 'not set')
    truncated_path = path_env[:100] + '...' if path_env != 'not set' and len(path_env) > 100 else path_env
    
    env_vars = {
        UPDATE_CHECK_ENV_VAR: os.getenv(UPDATE_CHECK_ENV_VAR, 'not set'),
        'PATH': truncated_path,
        'PYTHONPATH': os.getenv('PYTHONPATH', 'not set'),
    }
    
    # Build markdown content
    markdown_text = f"""
# MIDIDiff Debug Information

## Version Information

| Component | Version |
|-----------|---------|
| **MIDIDiff** | `{mididiff_version}` |
| **Python** | `{python_version}` |
| **mido** | `{mido_version}` |
| **rich** | `{rich_version}` |

## Platform Information

| Property | Value |
|----------|-------|
| **Platform** | `{platform_info}` |
| **System** | `{platform.system()}` |
| **Release** | `{platform.release()}` |
| **Machine** | `{platform.machine()}` |
| **Processor** | `{platform.processor() or 'unknown'}` |

## Environment

| Variable | Value |
|----------|-------|
| **Working Directory** | `{cwd}` |
| **{UPDATE_CHECK_ENV_VAR}** | `{env_vars[UPDATE_CHECK_ENV_VAR]}` |
| **PYTHONPATH** | `{env_vars['PYTHONPATH']}` |

**PATH** (truncated):
```
{env_vars['PATH']}
```

---

*Copy this information when reporting issues or requesting support.*
""".strip()
    
    md = Markdown(markdown_text)
    
    panel = Panel(
        md,
        border_style='cyan',
        padding=(1, 2),
        title='[bold cyan]Debug Information[/bold cyan]',
    )
    
    console.print(panel)


def _build_parser() -> argparse.ArgumentParser:
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


def cli() -> None:
    """
    Command-line interface for MIDIDiff.

    Usage:
        midi-diff fileA.mid fileB.mid output.mid  (assumes 'diff' subcommand)
        midi-diff diff fileA.mid fileB.mid output.mid
        midi-diff debug-info
        midi-diff --version

    """
    parser = _build_parser()
    
    # Backward compatibility: If first arg isn't a known subcommand/flag,
    # try to parse as 'diff' subcommand by prepending it to argv
    # This approach is more robust than checking argv length directly
    if len(sys.argv) > 1 and sys.argv[1] not in KNOWN_SUBCOMMANDS_AND_FLAGS:
        # Try parsing to see if we get valid diff arguments
        # This handles edge cases better than just checking length
        sys.argv.insert(1, 'diff')
    
    args = parser.parse_args()
    
    # Handle subcommands
    if args.command == 'diff':
        main(args.file_a, args.file_b, args.out_file)
    elif args.command == 'debug-info':
        _print_debug_info()
    else:
        # No subcommand provided - show help
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    cli()


__all__ = ["cli"]
