from bundlewrap_commit_hooks.prefix_commit import find_common_directory, get_prefix_from_files

def test_single_bundle():
    CHANGED_FILES = [
        'bundles/xyz/items.py',
        'bundles/xyz/metadata.py',
        'bundles/xyz/files/foo.txt'
    ]

    prefix = get_prefix_from_files(CHANGED_FILES)

    assert prefix == 'bundles/xyz: '

def test_multiple_bundles():
    CHANGED_FILES = [
        'bundles/bundle1/items.py',
        'bundles/bundle2/metadata.py',
        'bundles/bundle3/files/foo.txt'
    ]

    prefix = get_prefix_from_files(CHANGED_FILES)

    assert prefix == 'bundles: '

def test_multiple_bundles_and_root_files_changed():
    CHANGED_FILES = [
        'bundles/bundle1/items.py',
        'bundles/bundle2/metadata.py',
        'bundles/bundle3/files/foo.txt',
        'README.md'
    ]

    prefix = get_prefix_from_files(CHANGED_FILES)

    assert prefix == 'bw: '

def test_root_files_changed():
    CHANGED_FILES = [
        'README.md'
    ]

    prefix = get_prefix_from_files(CHANGED_FILES)

    assert prefix == 'bw: '

def test_invalid_files_passed():
    CHANGED_FILES = [
        '',
        '.'
    ]

    common_directory = find_common_directory(CHANGED_FILES)

    assert common_directory is None

def test_single_file_changed():
    CHANGED_FILES = [
        'docs/README.md'
    ]

    prefix = get_prefix_from_files(CHANGED_FILES)

    assert prefix == 'docs: '
