import os, os.path, shutil

# GDAL libraries
from osgeo import gdal
from osgeo import ogr
from osgeo import osr  # open spatial reference
from osgeo import gdal_array  # array integration with numpy
from osgeo import gdalconst


# TODO: Could probably use GDAL CLI utility as well.
def lambert_to_wgs84(src_path, tgt_path):
    """
    Converts shapefile projected in Lambert Conformal Conic to WGS84 (unprojected).

    :param src_path:
    :type src_path:
    :param tgt_path:
    :type tgt_path:
    :return:
    :rtype:
    """
    tgt_spatRef = osr.SpatialReference()
    tgt_spatRef.ImportFromEPSG(4326)  # wgs84

    driver = ogr.GetDriverByName('ESRI Shapefile')
    src = driver.Open(src_path)
    srcLyr = src.GetLayer()
    src_spatRef = srcLyr.GetSpatialRef()

    tgt = driver.CreateDataSource(tgt_path)

    # Use well-known binary format (WKB) to specify geometry
    tgtLyr = tgt.CreateLayer('NYC_Museums_GEO', srs=tgt_spatRef, geom_type=ogr.wkbPoint)
    featDef = srcLyr.GetLayerDefn()
    trans = osr.CoordinateTransformation(src_spatRef, tgt_spatRef)

    srcFeat = srcLyr.GetNextFeature()

    while srcFeat:
        geom = srcFeat.GetGeometryRef()
        geom.Transform(trans)

        feature = ogr.Feature(featDef)
        feature.SetGeometry(geom)
        tgtLyr.CreateFeature(feature)

        feature.Destroy()  # or feature = None
        srcFeat.Destroy()  # or srcFeat = None

        srcFeat = srcLyr.GetNextFeature()

    src.FlushCache()
    src.Destroy()  # or src = None
    tgt.FlushCache()
    tgt.Destroy()  # or tgt = None

    src_base_path, _ = os.path.split(src_path)
    tgt_base_path, _ = os.path.split(tgt_path)

    # Copy attributes (unchanged)
    src_dbf_path = os.path.join(src_base_path, os.path.splitext(src_path)[0] + '.dbf')
    tgt_dbf_path = os.path.join(tgt_base_path, os.path.splitext(tgt_path)[0] + '.dbf')
    shutil.copyfile(src_dbf_path, tgt_dbf_path)


# TODO: Could probably use GDAL CLI utility as well.
def utm_to_projection(src_path, tgt_path, cs='WGS84'):
    """
    Reprojects a UTM shapefile to WGS84

    :param src_path:
    :type src_path:
    :param tgt_path:
    :type tgt_path:
    :param cs:
    :type cs:
    :return:
    :rtype:
    """
    srcProjection = osr.SpatialReference()
    srcProjection.SetUTM(17)

    dstProjection = osr.SpatialReference()
    dstProjection.SetWellKnownGeogCS(cs)  # Lat/long.

    transform = osr.CoordinateTransformation(srcProjection, dstProjection)

    srcFile = ogr.Open(src_path)
    srcLayer = srcFile.GetLayer(0)

    # Create the dest shapefile, and give it the new projection.
    driver = ogr.GetDriverByName("ESRI Shapefile")
    dstFile = driver.CreateDataSource(tgt_path)
    dstLayer = dstFile.CreateLayer("layer", dstProjection)

    field = ogr.FieldDefn("ID", ogr.OFTInteger)
    field.SetWidth(4)
    dstLayer.CreateField(field)

    field = ogr.FieldDefn("LUCODE", ogr.OFTInteger)
    field.SetWidth(4)
    dstLayer.CreateField(field)

    # Reproject each feature in turn.
    for i in range(srcLayer.GetFeatureCount()):
        feature = srcLayer.GetFeature(i)
        lucode = feature.GetField("LUCODE")
        geometry = feature.GetGeometryRef()

        newGeometry = geometry.Clone()
        newGeometry.Transform(transform)

        feature = ogr.Feature(dstLayer.GetLayerDefn())

        feature.SetField("ID", i)
        feature.SetField("LUCODE", lucode)
        feature.SetGeometry(newGeometry)
        dstLayer.CreateFeature(feature)

        feature.Destroy()

    dstFile.FlushCache()
    dstFile.Destroy()


# TODO: Could probably use GDAL CLI utility as well.
def nad27_to_datum(src_path, tgt_path, from_cs='NAD27', to_cs='WGS84'):
    """
    Datums: Reprojects a NAD27 shapefile to WGS84

    :param src_path:
    :type src_path:
    :param tgt_path:
    :type tgt_path:
    :param cs:
    :type cs:
    :return:
    :rtype:
    """
    src_datum = osr.SpatialReference()
    src_datum.SetWellKnownGeogCS(from_cs)

    dst_datum = osr.SpatialReference()
    dst_datum.SetWellKnownGeogCS(to_cs)

    transform = osr.CoordinateTransformation(src_datum, dst_datum)

    srcFile = ogr.Open(src_path)
    srcLayer = srcFile.GetLayer(0)

    # Create the dest shapefile, and give it the new datum.
    driver = ogr.GetDriverByName("ESRI Shapefile")
    dstFile = driver.CreateDataSource(tgt_path)
    dstLayer = dstFile.CreateLayer("layer", dst_datum)

    field = ogr.FieldDefn("ID", ogr.OFTInteger)
    field.SetWidth(4)
    dstLayer.CreateField(field)

    field = ogr.FieldDefn("TIGER_ID", ogr.OFTInteger)
    field.SetWidth(4)
    dstLayer.CreateField(field)

    field = ogr.FieldDefn("CFCC", ogr.OFTString)
    field.SetWidth(4)
    dstLayer.CreateField(field)

    # Reproject each feature in turn.
    for i in range(srcLayer.GetFeatureCount()):
        feature = srcLayer.GetFeature(i)
        id = feature.GetField("TIGER_ID")
        cfcc = feature.GetField("CFCC")
        geometry = feature.GetGeometryRef()

        newGeometry = geometry.Clone()
        newGeometry.Transform(transform)

        feature = ogr.Feature(dstLayer.GetLayerDefn())

        feature.SetField("ID", i)
        feature.SetField("TIGER_ID", id)
        feature.SetField("CFCC", cfcc)
        feature.SetGeometry(newGeometry)
        dstLayer.CreateFeature(feature)

        feature.Destroy()

    dstFile.FlushCache()
    dstFile.Destroy()
