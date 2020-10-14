import shapefile


def import_file(path):
    """
    Usage:
    nyc_path = os.path.join(os.environ["DATA_DIR"], 'shapefile_out', 'NYC_MUSEUMS_GEO.shp')
    :param path:
    :type path:
    :return:
    :rtype:
    """

    with shapefile.Reader(path) as shp_reader:
        print(f"Geometry Type: {shp_reader.shapeTypeName}")
        print(f"Features: {len(shp_reader)}")
        print(f"Bounding Box: {shp_reader.bbox}")

        # Attribute Definitions
        for meta in shp_reader.fields:
            print(meta)

        # Attribute Records
        for rec in shp_reader.records()[:10]:
            print(rec['NAME'])
            print(rec[2])

        # Geometries
        for i, s in enumerate(shp_reader.shapes()[:10]):
            print(f"Geometry-{i}: {s.points[0]}")
            print(f"Geometry-{i}: {s.shapeTypeName}")

        # Read both attributes and geometries.
        for srec in shp_reader.shapeRecords()[:10]:
            print(f"Geometry-{srec.record.oid}: {srec.shape.points[0]}")
            print(f"Geometry-{srec.record.oid}: {srec.shape.shapeTypeName}")
            print(f"Record-{srec.record.oid}: {srec.record['NAME']}, {srec.record[2]}")