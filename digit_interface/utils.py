def get_cpp_path():
    """Returns the path to the directory containing the C++ source code."""
    import pkg_resources

    return pkg_resources.resource_filename("digit", "cpp/")
