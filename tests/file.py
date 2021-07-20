def get_content(path_to_file):
    with open(path_to_file) as f:
        return f.read()


def is_same_content(path_to_file1, path_to_file2):
    return get_content(path_to_file1) == get_content(path_to_file2)