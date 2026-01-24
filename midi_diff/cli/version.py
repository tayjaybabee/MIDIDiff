"""
Author: 
    Inspyre Softworks

Project:
    MIDIDiff

File: 
    midi_diff/cli/version.py
 

Description:
    Version and debug information utilities for the MIDIDiff CLI.

"""
import json
import os
import platform
import subprocess
import sys
import urllib.error
import urllib.request
from importlib import metadata

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    _RICH_AVAILABLE: bool = True
except ImportError:
    _RICH_AVAILABLE = False


DIST_NAME: str = "midi-diff"
PYPI_JSON_URL: str = f"https://pypi.org/pypi/{DIST_NAME}/json"

# Update check configuration
UPDATE_CHECK_ENV_VAR: str = "MIDIFF_CHECK_UPDATES"
UPDATE_CHECK_TRUTHY_VALUES: tuple[str, ...] = ("1", "true", "yes")

# Path truncation for debug output
PATH_TRUNCATE_LENGTH: int = 100


def _get_version() -> str:
    """Get the installed version of MIDIDiff."""
    return _get_metadata_version(DIST_NAME, "unknown")


def _get_dependency_version(name: str) -> str:
    """Get the installed version of a dependency."""
    return _get_metadata_version(name, "not installed")


def _get_metadata_version(name: str, fallback: str) -> str:
    """
    Get version from package metadata.
    
    Parameters:
        name: Package name to lookup
        fallback: Default value if package not found
        
    Returns:
        Version string or fallback value
    """
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return fallback


def _check_for_update(current_version: str) -> str:
    """
    Check PyPI for newer version.
    
    NOTE: This function makes a network request to PyPI (https://pypi.org/pypi/midi-diff/json)
    to check for updates. It is called when the user explicitly enables update checking
    via the MIDIFF_CHECK_UPDATES environment variable, or when using the check-updates
    or upgrade CLI subcommands.
    
    Parameters:
        current_version: Currently installed version
        
    Returns:
        Update status message
    """
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


def print_version_info() -> None:
    """Print formatted version information to the console."""
    if not _RICH_AVAILABLE:
        # Fallback to plain text if rich is not available
        current_version = _get_version()
        print(f"MIDIDiff version: {current_version}")
        print(f"Python: {platform.python_version()}")
        print(f"Platform: {platform.platform()}")
        print(f"mido: {_get_dependency_version('mido')}")
        print(f"rich: {_get_dependency_version('rich')}")
        
        # Check for updates if explicitly enabled via environment variable
        if os.getenv(UPDATE_CHECK_ENV_VAR, '').lower() in UPDATE_CHECK_TRUTHY_VALUES:
            update_msg = _check_for_update(current_version)
            print(update_msg)
        else:
            print(f"Update check disabled (set {UPDATE_CHECK_ENV_VAR}=1 to enable).")
        
        return
    
    console = Console()
    current_version = _get_version()

    markdown_text: str = f"""
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


def print_debug_info() -> None:
    """Print comprehensive debug information in Rich Markdown format."""
    if not _RICH_AVAILABLE:
        # Fallback to plain text if rich is not available
        print("MIDIDiff Debug Information")
        print("=" * 40)
        print(f"MIDIDiff: {_get_version()}")
        print(f"Python: {platform.python_version()}")
        print(f"Platform: {platform.platform()}")
        print(f"mido: {_get_dependency_version('mido')}")
        print(f"rich: {_get_dependency_version('rich')}")
        print(f"Working Directory: {os.getcwd()}")
        return
        
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
    truncated_path = path_env[:PATH_TRUNCATE_LENGTH] + '...' if path_env != 'not set' and len(path_env) > PATH_TRUNCATE_LENGTH else path_env
    
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


def check_for_updates_command() -> None:
    """
    Explicitly check for updates and display the result.
    
    This is called by the 'check-updates' subcommand.
    """
    current_version = _get_version()
    
    if not _RICH_AVAILABLE:
        print(f"MIDIDiff version: {current_version}")
        print("Checking for updates...")
        update_msg = _check_for_update(current_version)
        print(update_msg)
        
        if "Update available" in update_msg:
            print("\nTo upgrade, run: midi-diff upgrade")
        return
    
    console = Console()
    console.print(f"[bold]MIDIDiff version:[/bold] {current_version}")
    console.print("[dim]Checking for updates...[/dim]")
    
    update_msg = _check_for_update(current_version)
    
    if 'Update available' in update_msg:
        console.print(f'[yellow]⚠ {update_msg}[/yellow]')
        console.print("\n[dim]To upgrade, run:[/dim] [cyan]midi-diff upgrade[/cyan]")
    elif 'Up to date' in update_msg:
        console.print(f'[green]✓ {update_msg}[/green]')
    else:
        console.print(f'[red]{update_msg}[/red]')


def upgrade_package(include_pre: bool = False) -> None:
    """
    Upgrade the midi-diff package using pip.
    
    Parameters:
        include_pre: Whether to include pre-release versions
    """
    current_version = _get_version()
    
    if not _RICH_AVAILABLE:
        print(f"Current version: {current_version}")
        print("Checking for updates...")
        update_msg = _check_for_update(current_version)
        print(update_msg)
        
        if "Up to date" in update_msg:
            print("No upgrade needed.")
            return
        
        if "Update check failed" in update_msg:
            print("Cannot proceed with upgrade due to update check failure.")
            return
        
        print("\nUpgrading midi-diff...")
    else:
        console = Console()
        console.print(f"[bold]Current version:[/bold] {current_version}")
        console.print("[dim]Checking for updates...[/dim]")
        
        update_msg = _check_for_update(current_version)
        
        if "Up to date" in update_msg:
            console.print(f'[green]✓ {update_msg}[/green]')
            console.print("[dim]No upgrade needed.[/dim]")
            return
        
        if "Update check failed" in update_msg:
            console.print(f'[red]{update_msg}[/red]')
            console.print("[red]Cannot proceed with upgrade due to update check failure.[/red]")
            return
        
        console.print(f'[yellow]⚠ {update_msg}[/yellow]')
        console.print("\n[dim]Upgrading midi-diff...[/dim]")
    
    # Build pip command
    pip_cmd = [sys.executable, "-m", "pip", "install", "--upgrade"]
    if include_pre:
        pip_cmd.append("--pre")
    pip_cmd.append(DIST_NAME)
    
    try:
        # Run pip upgrade
        result = subprocess.run(
            pip_cmd,
            capture_output=True,
            text=True,
            check=True,
        )
        
        # Handle edge case where pip reports the requirement is already satisfied
        already_satisfied = "Requirement already satisfied" in (result.stdout or "")
        
        if not _RICH_AVAILABLE:
            if already_satisfied:
                print("\nPackage is already at the latest version. No changes were made.")
                if result.stdout.strip():
                    print(f"Output: {result.stdout.strip()}")
            else:
                print("\nUpgrade successful!")
                if result.stdout.strip():
                    print(f"Output: {result.stdout.strip()}")
        else:
            if already_satisfied:
                console.print("[green]✓ Package is already at the latest version. No changes were made.[/green]")
                if result.stdout.strip():
                    console.print(f"[dim]{result.stdout.strip()}[/dim]")
            else:
                console.print("[green]✓ Upgrade successful![/green]")
                if result.stdout.strip():
                    console.print(f"[dim]{result.stdout.strip()}[/dim]")
        
    except subprocess.CalledProcessError as e:
        # Parse stderr for more helpful error messages
        error_msg = e.stderr or str(e)
        if "Permission denied" in error_msg or "PermissionError" in error_msg:
            helpful_msg = "Permission denied. Try running with appropriate permissions or use a virtual environment."
        elif "Network" in error_msg or "ConnectionError" in error_msg or "URLError" in error_msg:
            helpful_msg = "Network error. Please check your internet connection and try again."
        else:
            helpful_msg = f"Upgrade failed: {e}"
        
        if not _RICH_AVAILABLE:
            print(f"\n{helpful_msg}")
            if e.stderr:
                print(f"Error details: {e.stderr}")
        else:
            console.print(f"[red]✗ {helpful_msg}[/red]")
            if e.stderr:
                console.print(f"[red]{e.stderr}[/red]")
        sys.exit(1)
    except Exception as e:
        if not _RICH_AVAILABLE:
            print(f"\nUnexpected error during upgrade: {e}")
        else:
            console.print(f"[red]✗ Unexpected error during upgrade: {e}[/red]")
        sys.exit(1)


__all__ = ["print_version_info", "print_debug_info", "check_for_updates_command", "upgrade_package"]
