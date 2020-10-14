import geojson


def import_file(path):
    """
    Usage:
    ms_counties_path = os.path.join(os.environ["DATA_DIR"], 'Mississippi', 'ms_counties.geojson')

    :param path:
    :type path:
    :return:
    :rtype:
    """
    with open(path, 'r') as f:
        # Wraps json lib - same syntax/semantics
        counties = geojson.load(f)
        print(counties['name'])