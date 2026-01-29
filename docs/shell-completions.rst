Shell Completions
=================

MIDIDiff provides tab-completion support for multiple shells, making it easier
to use the command-line interface.

Supported Shells
---------------

* **Bash** - The Bourne Again SHell (Linux, macOS, Windows Git Bash)
* **Zsh** - Z Shell (macOS default since Catalina, Linux)
* **Fish** - Friendly Interactive SHell (cross-platform)
* **PowerShell** - Windows PowerShell and PowerShell Core (cross-platform)
* **CMD** - Windows Command Prompt (basic doskey helper)

Generating Completion Scripts
-----------------------------

To generate a completion script for your shell, use the ``completion`` subcommand:

.. code-block:: bash

   midi-diff completion <shell>

Replace ``<shell>`` with one of: ``bash``, ``zsh``, ``fish``, ``powershell``, or ``cmd``.

The script will be printed to standard output. You can then install it according
to your shell's conventions.

Automatic Installation
----------------------

To install completions for the shell you are currently using, run:

.. code-block:: bash

   midi-diff install-completions

The tool will attempt to detect your shell and install the completion script to a
standard per-user location. To override detection, pass ``--shell``:

.. code-block:: bash

   midi-diff install-completions --shell zsh

You can also override the base directory used for installation by setting
``MIDI_DIFF_COMPLETIONS_DIR``. This is useful if your shell loads completions
from a nonstandard location. On non-Windows systems, PowerShell defaults to
``~/.config/powershell/Scripts``, while on Windows it uses
``~/Documents/PowerShell/Scripts``. CMD writes to ``%USERPROFILE%`` by default.

Installation Instructions
-------------------------

Bash
~~~~

**Option 1: User-specific installation (recommended)**

.. code-block:: bash

   # Create completion directory if it doesn't exist
   mkdir -p ~/.local/share/bash-completion/completions
   
   # Generate and save the completion script
   midi-diff completion bash > ~/.local/share/bash-completion/completions/midi-diff
   
   # Source it in your current session (or restart your shell)
   source ~/.local/share/bash-completion/completions/midi-diff

**Option 2: Session-specific (temporary)**

.. code-block:: bash

   # Source the completion script in your current session
   source <(midi-diff completion bash)
   
   # To make it permanent, add this line to your ~/.bashrc:
   echo 'source <(midi-diff completion bash)' >> ~/.bashrc

**Option 3: System-wide installation (requires sudo)**

.. code-block:: bash

   # Install for all users (requires root)
   sudo midi-diff completion bash > /etc/bash_completion.d/midi-diff

Zsh
~~~

**Option 1: User-specific installation (recommended)**

.. code-block:: bash

   # Create completion directory if it doesn't exist
   mkdir -p ~/.zsh/completions
   
   # Generate and save the completion script
   midi-diff completion zsh > ~/.zsh/completions/_midi-diff
   
   # Add this to your ~/.zshrc if not already present:
   echo 'fpath=(~/.zsh/completions $fpath)' >> ~/.zshrc
   echo 'autoload -Uz compinit && compinit' >> ~/.zshrc
   
   # Reload your shell configuration
   source ~/.zshrc

**Option 2: Using Oh My Zsh**

.. code-block:: bash

   # Generate completion script in Oh My Zsh's custom completions directory
   midi-diff completion zsh > ~/.oh-my-zsh/custom/completions/_midi-diff
   
   # Reload your shell configuration
   source ~/.zshrc

**Option 3: System-wide installation (requires sudo)**

.. code-block:: bash

   # Install for all users (location may vary by system)
   sudo midi-diff completion zsh > /usr/local/share/zsh/site-functions/_midi-diff

Fish
~~~~

**User-specific installation**

.. code-block:: bash

   # Create completion directory if it doesn't exist
   mkdir -p ~/.config/fish/completions
   
   # Generate and save the completion script
   midi-diff completion fish > ~/.config/fish/completions/midi-diff.fish
   
   # Completions are loaded automatically in new sessions

**System-wide installation (requires sudo)**

.. code-block:: bash

   # Install for all users
   sudo midi-diff completion fish > /usr/share/fish/vendor_completions.d/midi-diff.fish

PowerShell
~~~~~~~~~~

**Current user installation (recommended)**

.. code-block:: powershell

   # Create profile directory if it doesn't exist
   if (!(Test-Path -Path (Split-Path -Parent $PROFILE))) {
       New-Item -ItemType Directory -Path (Split-Path -Parent $PROFILE) -Force
   }
   
   # Generate and save the completion script
   midi-diff completion powershell | Out-File -FilePath "$HOME\Documents\PowerShell\Scripts\midi-diff-completion.ps1" -Encoding UTF8
   
   # Add this line to your PowerShell profile to load it:
   # Open profile with: notepad $PROFILE
   Add-Content -Path $PROFILE -Value "`n. `"$HOME\Documents\PowerShell\Scripts\midi-diff-completion.ps1`""

**Session-specific (temporary)**

.. code-block:: powershell

   # Load completion in current session
   midi-diff completion powershell | Invoke-Expression

**All users installation (requires admin)**

.. code-block:: powershell

   # Run PowerShell as Administrator and execute:
   midi-diff completion powershell | Out-File -FilePath "$PSHOME\Modules\midi-diff\midi-diff-completion.ps1" -Encoding UTF8

CMD (Command Prompt)
~~~~~~~~~~~~~~~~~~~

Windows Command Prompt has limited completion support. The completion command
generates a simple doskey macro helper:

.. code-block:: batch

   REM Generate and execute the completion helper
   midi-diff completion cmd > %TEMP%\midi-diff-completion.cmd
   call %TEMP%\midi-diff-completion.cmd

Note: This provides basic command aliasing but not true tab-completion like
other shells. For better completion support on Windows, use PowerShell instead.

Testing Completions
-------------------

After installing completions, test them by typing:

.. code-block:: bash

   midi-diff <TAB>

You should see available subcommands:

* ``diff`` - Compare two MIDI files
* ``debug-info`` - Show diagnostic information
* ``check-updates`` - Check for updates
* ``upgrade`` - Upgrade to the latest version
* ``docs`` - Open documentation
* ``completion`` - Generate shell completions

For the ``diff`` subcommand, tab completion will suggest file paths.
For the ``completion`` subcommand, tab completion will suggest shell names.

Troubleshooting
---------------

Completions not working
~~~~~~~~~~~~~~~~~~~~~~~

1. **Verify installation path**: Make sure the completion script was saved to
   the correct directory for your shell.

2. **Check shell configuration**: Ensure your shell is configured to load
   completions from the directory where you saved the script.

3. **Restart your shell**: Completions are typically loaded when the shell
   starts. Try opening a new terminal window.

4. **Verify the script**: Check that the completion script was generated
   without errors:

   .. code-block:: bash

      midi-diff completion bash | head -20

5. **Check file permissions**: Ensure the completion script is readable:

   .. code-block:: bash

      # For Bash/Zsh/Fish
      chmod 644 ~/.local/share/bash-completion/completions/midi-diff

Bash: "command not found" errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you see errors when sourcing the completion script, ensure ``bash-completion``
is installed:

.. code-block:: bash

   # Ubuntu/Debian
   sudo apt install bash-completion
   
   # Fedora/RHEL
   sudo dnf install bash-completion
   
   # macOS (with Homebrew)
   brew install bash-completion@2

Zsh: completions not loading
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ensure ``compinit`` is called after adding the completions directory to ``fpath``:

.. code-block:: bash

   # In ~/.zshrc, this order is important:
   fpath=(~/.zsh/completions $fpath)
   autoload -Uz compinit && compinit

You may also need to rebuild the completion cache:

.. code-block:: bash

   rm ~/.zcompdump
   compinit

PowerShell: execution policy errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If PowerShell won't execute the completion script, you may need to adjust
the execution policy:

.. code-block:: powershell

   # Check current policy
   Get-ExecutionPolicy
   
   # Set policy to allow local scripts (as Administrator)
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

Updating Completions
--------------------

When MIDIDiff is updated and new commands or options are added, you should
regenerate and reinstall the completion scripts:

.. code-block:: bash

   # Example for Bash
   midi-diff completion bash > ~/.local/share/bash-completion/completions/midi-diff
   source ~/.local/share/bash-completion/completions/midi-diff

Advanced Usage
--------------

Custom completion locations
~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can save completion scripts to any location you prefer, as long as your
shell is configured to load them from that location.

For example, to use a custom directory for Bash completions:

.. code-block:: bash

   # In ~/.bashrc:
   export BASH_COMPLETION_USER_DIR="$HOME/.my-completions"
   
   # Then save completions there:
   mkdir -p ~/.my-completions
   midi-diff completion bash > ~/.my-completions/midi-diff

Combining with other tools
~~~~~~~~~~~~~~~~~~~~~~~~~~

If you use a shell framework like Oh My Zsh, Prezto, or Fisher (for Fish),
follow their specific conventions for loading custom completions.

For Oh My Zsh, the custom completions directory is:

.. code-block:: bash

   ~/.oh-my-zsh/custom/completions/

For Prezto, add completion directories to your ``.zpreztorc``.

For Fish and Fisher/Oh My Fish, place completions in:

.. code-block:: bash

   ~/.config/fish/completions/

Contributing
------------

If you encounter issues with shell completions or would like to suggest
improvements, please open an issue on the `GitHub repository
<https://github.com/Inspyre-Softworks/MIDIDiff/issues>`_.

Completion scripts are generated programmatically by
``midi_diff.cli.completions.emit_completion_script()``. To add support for
a new shell or improve existing completions, see the
`CONTRIBUTING.md <https://github.com/Inspyre-Softworks/MIDIDiff/blob/main/CONTRIBUTING.md>`_
guide.
