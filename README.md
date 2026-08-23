# bundlewrap-commit-hooks

A collection of pre-commit hooks for [bundlewrap](https://bundlewrap.org/) projects.

## Hooks

### prefix-commit

Automatically prefixes commit messages based on the directories of staged files.

When you commit changes to files in specific directories, the hook will prefix your commit message with the deepest common directory path of all staged files.

**Behavior:**
- Single directory: `directory/path: Your commit message`
- Multiple directories with common prefix: `common/prefix: Your commit message`
- Multiple unrelated directories: `Your commit message` (unchanged)
- Root-level files only: `Your commit message` (unchanged)

**Examples:**

```bash
# Editing bundles/docker/items.py
$ git commit -m "Add new feature"
# Result: "bundles/docker: Add new feature"

# Editing bundles/docker/items.py and bundles/docker/metadata.py
$ git commit -m "Update configuration"
# Result: "bundles/docker: Update configuration"

# Editing bundles/docker/items.py and bundles/nginx/metadata.py
$ git commit -m "Refactor structure"
# Result: "bundles: Refactor structure"
```

## Installation

### 1. Add to your `.pre-commit-config.yaml`

```yaml
default_install_hook_types: [..., prepare-commit-msg]
repos:
  - repo: https://github.com/CommanderRedYT/bundlewrap-commit-hooks
    rev: main
    hooks:
      - id: prefix-commit
```

### 2. Install the hook

```bash
pre-commit install --install-hooks
```

### 3. Test it

```bash
git add <some files>
git commit -m "Test message"
```

The commit message should be prefixed automatically.