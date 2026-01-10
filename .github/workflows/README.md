# GitHub Actions Release Workflow

This workflow automatically creates releases and publishes packages when the version in `pyproject.toml` changes.

## Features

- **Automatic Version Detection**: Triggers when version changes in `pyproject.toml`
- **Pre-release Detection**: Automatically detects pre-release versions following PEP 440 (e.g., `dev`, `alpha`, `beta`, `rc`, `a[N]`, `b[N]` with or without separators)
- **GitHub Releases**: Creates GitHub releases with auto-generated release notes
- **Package Publishing**:
  - Publishes to **PyPI** for stable releases
  - Publishes to **Test PyPI** for pre-release versions
- **Build Artifacts**: Attaches built wheel and source distribution to GitHub releases

## Setup Requirements

### Required GitHub Secrets

You need to configure the following secrets in your GitHub repository settings:

1. **PYPI_TOKEN**: Your PyPI API token for publishing stable releases
   - Go to https://pypi.org/manage/account/token/
   - Create a new API token
   - Add it as a repository secret named `PYPI_TOKEN`

2. **TEST_PYPI_TOKEN**: Your Test PyPI API token for publishing pre-releases
   - Go to https://test.pypi.org/manage/account/token/
   - Create a new API token
   - Add it as a repository secret named `TEST_PYPI_TOKEN`

### How to Add Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add `PYPI_TOKEN` and `TEST_PYPI_TOKEN` with their respective values

## Workflow Triggers

The workflow triggers on:
- Push to `main` branch
- When `pyproject.toml` file is modified
- Only if the version number has actually changed

## Release Types

### Stable Release
Version format: `1.0.0`, `2.1.3`, etc.
- Creates a GitHub Release (not marked as pre-release)
- Publishes to **PyPI**

### Pre-release
Version format: `1.0.0.dev1`, `2.0.0a1`, `1.5.0b2`, `1.0.0rc1`, `1.0.0-dev.1`, etc.
- Creates a GitHub Release (marked as pre-release)
- Publishes to **Test PyPI**

## Usage

1. Update the version in `pyproject.toml`:
   ```toml
   [project]
   version = "1.0.0"  # or "1.0.0.dev1" for pre-release
   ```

2. Commit and push to `main` branch:
   ```bash
   git add pyproject.toml
   git commit -m "Bump version to 1.0.0"
   git push origin main
   ```

3. The workflow will automatically:
   - Detect the version change
   - Build the package
   - Create a GitHub release with tag `v1.0.0`
   - Publish to PyPI (stable) or Test PyPI (pre-release)

## Troubleshooting

- **Workflow doesn't trigger**: Ensure you're pushing to the `main` branch and `pyproject.toml` has changed
- **Publishing fails**: Check that the required secrets are configured correctly
- **Version already exists**: PyPI doesn't allow re-uploading the same version. Increment the version number.
