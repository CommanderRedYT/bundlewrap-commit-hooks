from __future__ import annotations

import argparse
import subprocess
from collections.abc import Sequence
from pathlib import Path


def get_staged_files() -> list[str]: # pragma: no cover
    """Get list of staged files from git."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except subprocess.CalledProcessError:
        return []


def find_common_directory(files: list[str]) -> str | None:
    """
    Find the deepest common directory path for all files.
    Ignores directories starting with a dot (., .., .git, etc).

    Examples:
        - 'bundles/web/items.py', 'bundles/web/config.py' -> 'bundles/web'
        - 'bundles/web/items.py', 'bundles/api/config.py' -> 'bundles'
        - 'src/main.py' -> 'src'
        - 'README.md' -> None (no directory)
        - 'bundles/web/items.py', '.github/workflows/test.yml' -> None (dot-prefixed file)
    """
    valid_files = []

    # Filter out files in dot-prefixed directories
    for file in files:
        if not file:
            continue
        parts = Path(file).parts
        if parts and not parts[0].startswith('.'):
            valid_files.append(parts)

    # If no valid files, return None
    if not valid_files:
        return None

    # If only one file, return its directory (excluding the filename)
    if len(valid_files) == 1:
        parts = valid_files[0]
        # If it's just a root-level file, return None
        if len(parts) <= 1:
            return None
        return str(Path(*parts[:-1]))

    # Find common prefix across all file paths (excluding filename)
    all_dirs = [parts[:-1] for parts in valid_files]  # Remove filename from each

    # Find the common prefix of all directory paths
    common_prefix = []
    for i in range(min(len(d) for d in all_dirs)):
        if all(d[i] == all_dirs[0][i] for d in all_dirs):
            common_prefix.append(all_dirs[0][i])
        else:
            break

    # Return None if no common directory, or the common path
    if not common_prefix:
        return None

    return str(Path(*common_prefix))


def generate_prefix(directory: str | None) -> str | None:
    """
    Generate commit message prefix based on directory.

    Returns:
        'directory: ' if a directory exists, None otherwise
    """
    if directory:
        return f'{directory}: '
    return 'bw: '


def get_prefix_from_files(staged_files: list[str]) -> str | None:
    common_dir = find_common_directory(staged_files)

    # Generate prefix
    prefix = generate_prefix(common_dir)

    return prefix


def main(argv: Sequence[str] | None = None) -> int: # pragma: no cover
    parser = argparse.ArgumentParser(
        description='Prefix commit message based on staged file paths'
    )
    parser.add_argument(
        'commit_msg_source',
        help='Path to the commit message file (passed by git hook)',
    )
    parser.add_argument('source', nargs='?', help='Source of the commit (optional)')
    parser.add_argument(
        'sha', nargs='?', help='SHA-1 of the commit being amended (optional)'
    )
    args = parser.parse_args(argv)

    commit_msg_file = Path(args.commit_msg_source)

    # Read the current commit message
    try:
        commit_msg = commit_msg_file.read_text()
    except FileNotFoundError:
        return 0

    # Skip if message is empty or already has a prefix
    if not commit_msg.strip() or commit_msg.strip().startswith('['):
        return 0

    # Get staged files and find common directory
    staged_files = get_staged_files()

    prefix = get_prefix_from_files(staged_files)

    # If we have a prefix, prepend it to the commit message
    if prefix:
        new_msg = f'{prefix}{commit_msg}'
        commit_msg_file.write_text(new_msg)

    return 0


if __name__ == '__main__': # pragma: no cover
    raise SystemExit(main())
