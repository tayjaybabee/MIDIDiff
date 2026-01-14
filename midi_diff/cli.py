"""
Author: 
    Inspyre Softworks

Project:
    MIDIDiff

File: 
    midi_diff/cli.py
 

Description:
    Backward compatibility shim for the CLI module.
    
    This module preserves backward compatibility for code that imports from 
    `midi_diff.cli` or runs `python -m midi_diff.cli`. The actual CLI 
    implementation has been moved to the `midi_diff.cli` sub-package.
    
    This shim will be maintained through the 1.x release series.

"""
# Import from the new CLI sub-package
from midi_diff.cli import cli


# Support for `python -m midi_diff.cli` (backward compatibility)
if __name__ == "__main__":
    cli()


__all__ = ["cli"]
