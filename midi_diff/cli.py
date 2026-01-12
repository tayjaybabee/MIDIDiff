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
from midi_diff.core import main

DIST_NAME = "midi-diff"
PYPI_JSON_URL = f"https://pypi.org/pypi/{DIST_NAME}/json"

# Update check configuration
UPDATE_CHECK_ENV_VAR = "MIDIFF_CHECK_UPDATES"
UPDATE_CHECK_TRUTHY_VALUES = ("1", "true", "yes")


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
    current_version = _get_version()
    print(f"MIDIDiff {current_version}")
    print(f"Python {platform.python_version()}")
    print(f"Platform {platform.platform()}")
    print(f"mido {_get_dependency_version('mido')}")
    
    # Only check for updates if explicitly enabled via environment variable
    # This avoids potential hangs on slow/unreliable network connections
    if os.getenv(UPDATE_CHECK_ENV_VAR, "").lower() in UPDATE_CHECK_TRUTHY_VALUES:
        print(_check_for_update(current_version))
    else:
        print(f"Update check disabled (set {UPDATE_CHECK_ENV_VAR}=1 to enable).")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare two MIDI files and output their differences.",
    )
    parser.add_argument("file_a", help="Path to the first MIDI file.")
    parser.add_argument("file_b", help="Path to the second MIDI file.")
    parser.add_argument("out_file", help="Path for the diff MIDI output.")
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
    return parser


def cli() -> None:
    """
    Command-line interface for MIDIDiff.

    Usage:
        python -m midi_diff.cli fileA.mid fileB.mid diff.mid

    """
    parser = _build_parser()
    args = parser.parse_args()
    main(args.file_a, args.file_b, args.out_file)


if __name__ == "__main__":
    cli()


__all__ = ["cli"]
