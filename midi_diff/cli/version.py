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
import urllib.error
import urllib.request
from importlib import metadata

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    _RICH_AVAILABLE = True
except ImportError:
    _RICH_AVAILABLE = False


DIST_NAME = "midi-diff"
PYPI_JSON_URL = f"https://pypi.org/pypi/{DIST_NAME}/json"

# Update check configuration
UPDATE_CHECK_ENV_VAR = "MIDIFF_CHECK_UPDATES"
UPDATE_CHECK_TRUTHY_VALUES = ("1", "true", "yes")


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
        return
    
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


__all__ = ["print_version_info", "print_debug_info"]
