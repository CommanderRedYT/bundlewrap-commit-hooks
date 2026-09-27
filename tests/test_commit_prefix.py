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


def test_root_single_file_changed():
    CHANGED_FILES = [
        'README.md'
    ]

    prefix = get_prefix_from_files(CHANGED_FILES)

    assert prefix == 'bw: '

def test_root_multiple_files_changed():
    CHANGED_FILES = [
        'README.md',
        '.gitignore'
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

def test_node_single_file_changed():
    CHANGED_FILES = [
        'nodes/my_awesome_node.toml'
    ]

    prefix = get_prefix_from_files(CHANGED_FILES)

    assert prefix == 'nodes/my_awesome_node: '

def test_group_single_file_changed():
    CHANGED_FILES = [
        'groups/my_awesome_group.toml'
    ]

    prefix = get_prefix_from_files(CHANGED_FILES)

    assert prefix == 'groups/my_awesome_group: '


def test_item_single_file_changed():
    CHANGED_FILES = [
        'items/my_awesome_item.py'
    ]

    prefix = get_prefix_from_files(CHANGED_FILES)

    assert prefix == 'items/my_awesome_item: '

def test_libs_single_file_changed():
    CHANGED_FILES = [
        'libs/tools.py'
    ]

    prefix = get_prefix_from_files(CHANGED_FILES)

    assert prefix == 'libs/tools: '

def test_data_single_file_changed():
    CHANGED_FILES = [
        'data/my_awesome_file.txt'
    ]

    prefix = get_prefix_from_files(CHANGED_FILES)

    assert prefix == 'data: '
