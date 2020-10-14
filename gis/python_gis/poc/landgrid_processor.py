from collections import namedtuple
from glob import glob
import logging
import re
import os

import fiona
import geojson
import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import (
    mapping, shape
)

from python_gis.poc.io.filegeodb import (
    read_gdb_layer, get_gdb_layer_meta
)
from python_gis.poc.io.shapefile import (
    read_shapefile, write_shapefile,
    split_shapefile, get_shapefile_meta
)
from python_gis.poc.tools.spatial import (
    remove_holes, sub_divide, get_overlaps,
    fix_anti_meridian, de_aggregate
)
from python_gis.poc.util import rm
from python_gis.poc.util.sql_config import (
    US_STATES, US_COUNTIES,
    PA_TOWNSHIPS, WV_DISTRICTS,
    OH_SECTIONS, OH_MUNIS,
    OH_TOWNSHIPS, TX_ABSTRACTS,
    TX_BLOCKS, TOWNSHIPS, SECTIONS
)

logger = logging.getLogger(__name__)
#logger.setLevel(level=logging.DEBUG)


# TODO: Rename poc package to landgrid_geo
class LandgridProcessor(object):

    def __init__(self, gdb_path, tmp_dir, datastore):
        self.gdb_path = gdb_path
        self.tmp_dir = tmp_dir
        self.datastore = datastore
        self.splitter = re.compile(r'\D+')

        # TODO: Experiment with different batch sizes.
        self.__BATCH_SIZE = 1000

    # TODO: This step can be multi-threaded (not memory bound).
    def to_shapefiles(self, redo_grid=True):

        # For testing only
        rm(os.path.join(self.tmp_dir, f'{US_STATES}.*'))
        rm(os.path.join(self.tmp_dir, f'{US_COUNTIES}.*'))
        rm(os.path.join(self.tmp_dir, f'{TX_ABSTRACTS}*.*'))
        rm(os.path.join(self.tmp_dir, f'{TX_BLOCKS}*.*'))
        rm(os.path.join(self.tmp_dir, f'{WV_DISTRICTS}.*'))
        rm(os.path.join(self.tmp_dir, f'{PA_TOWNSHIPS}.*'))
        rm(os.path.join(self.tmp_dir, f'{OH_TOWNSHIPS}*.*'))
        rm(os.path.join(self.tmp_dir, f'{OH_SECTIONS}*.*'))
        rm(os.path.join(self.tmp_dir, f'{OH_MUNIS}*.*'))
        rm(os.path.join(self.tmp_dir, f'*_township*.*'))
        rm(os.path.join(self.tmp_dir, f'*_section*.*'))

        non_batch = TOWNSHIPS + [US_STATES, US_COUNTIES,
                                 PA_TOWNSHIPS, WV_DISTRICTS,
                                 OH_SECTIONS, TX_ABSTRACTS]

        batch = SECTIONS[:]

        for layer in batch + non_batch:
            shape_path = os.path.join(self.tmp_dir, f'{layer}.shp')

            logger.info(f"Reading {layer}...")

            crs, schema, _ = get_gdb_layer_meta(self.gdb_path, layer)
            records = read_gdb_layer(self.gdb_path, layer, validate=True)

            logger.info(f"Exporting {shape_path}...")

            if layer in non_batch:
                write_shapefile(records, crs, schema, shape_path)
            else:
                split_shapefile(records, crs, schema, shape_path)

        if redo_grid:
            logger.info(f"Subdividing {US_STATES}")

            self.subdivide_layer(US_STATES)

            logger.info(f"Subdividing {US_COUNTIES}")

            self.subdivide_layer(US_COUNTIES)

    # TODO: Consider increasing partition size.
    def subdivide_layer(self, layer):
        """
        ST_Subdivide using Shapely implementation.

        :return:
        """
        layer_path = os.path.join(self.tmp_dir, f'{layer}.shp')
        grid_path = os.path.join(self.tmp_dir, f'{layer}_shgrid.shp')

        crs, schema, _ = get_shapefile_meta(layer_path)

        # Copy the source schema and add a property.
        new_schema = schema.copy()
        new_schema['properties']['grid_id'] = 'int'

        try:
            with fiona.open(layer_path) as src, \
                    fiona.open(grid_path, 'w', driver='ESRI Shapefile',
                            schema=new_schema, crs=crs) as tgt:

                grid_id = 1
                for rec in src:

                    try:
                        poly = shape(rec['geometry'])
                        poly = remove_holes(poly)
                    except Exception as e:
                        logger.exception(f"Error reading geometry: {rec['properties']}", e)
                        raise

                    parts = []
                    sub_divide(poly, parts)

                    for part in parts:
                        rec['geometry'] = mapping(part)
                        rec['properties'].update(grid_id=grid_id)
                        grid_id += 1

                        tgt.write(rec)

                    poly = parts = None

        except Exception as e:
            logger.exception(f"Error processing {layer}.", e)
            raise e

    def compute_overlaps(self, state_df, county_df, child_df):

        child_st_df = get_overlaps(state_df, child_df,
                                   label='StateOlap',
                                   grouping_column='State_Code')

        olap_df = get_overlaps(county_df, child_st_df,
                               label='CountyOlap',
                               grouping_column='County_Nam')  # TMP: .lower() for pg

        return olap_df

    def run_transforms(self):

        logger.info("Caching states and counties...")

        state_path = os.path.join(self.tmp_dir, f'{US_STATES}_shgrid.shp')
        state_df = gpd.read_file(state_path)

        state_meta_path = os.path.join(os.environ["DIML_HOME"], 'database',
                                       f'States.csv')
        state_meta_df = pd.read_csv(state_meta_path)
        state_df = state_df.merge(state_meta_df, how='left', left_on='State_Name',
                                  right_on='State')
        state_df.sindex  # pre-generate

        # DEBUG
        # st_debug_path = os.path.join(self.tmp_dir, f'{US_STATES}_debug.shp')
        # state_df.to_file(st_debug_path)

        county_path = os.path.join(self.tmp_dir, f'{US_COUNTIES}_shgrid.shp')
        # county_path = os.path.join(self.tmp_dir, f'Counties_US_pggrid.shp')  # from ST_Subdivide
        county_df = gpd.read_file(county_path)
        county_df.sindex

        # logger.info("Loading plss townships...")
        #
        # self.townships_to_sql(state_df, county_df)
        #
        # logger.info(f"Loading plss sections...")
        #
        # self.sections_to_sql(state_df, county_df)
        #
        # logger.info(f"Loading PA Townships...")
        #
        # self.pa_townships_to_sql(state_df, county_df)
        #
        # logger.info(f"Loading WV Districts...")
        #
        # self.wv_districts_to_sql(state_df, county_df)
        #
        # logger.info(f"Loading TX Abstracts...")
        #
        # self.tx_abstracts_to_sql(state_df, county_df)

        logger.info(f"Loading TX Blocks...")

        self.tx_blocks_to_sql(state_df, county_df)

        # sections_path = os.path.join(self.tmp_dir, f'{OH_SECTIONS}.shp')
        # sections_df = gpd.read_file(sections_path)
        # sections_df.sindex  # TODO: may not be needed
        #
        # logger.info(f"Loading OH Munis...")
        #
        # self.oh_munis_to_sql(state_df, county_df, sections_df)
        #
        # logger.info(f"Loading OH Townships...")
        #
        # self.oh_townships_to_sql(state_df, county_df, sections_df)
        #
        # logger.info(f"Loading OH Sections...")
        #
        # self.oh_sections_to_sql(state_df, county_df, sections_df)
        
        # DEBUG
        # self.__load_oh_sections(sections_df)

        # logger.info(f"Loading states...")
        #
        # self.load_states()
        #
        # logger.info(f"Loading counties...")
        #
        # self.load_counties()

    def townships_to_sql(self, state_df, county_df):

        dml = """
        INSERT INTO landgrid2.plss_township (TWPCODE, MER, MST, TWP, THALF, 
                                             TNS, RGE, RHALF, REW, /*SecCount,*/ 
                                             TWPLabel, Shape_Length, Shape_Area, 
                                             State_Name, State_Overlaps, 
                                             County_Overlaps, Township, Range, 
                                             geobounds, shape)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                ?, ?, geometry::STGeomFromWKB(?, 4326));
        """

        self.datastore.execute_dml('TRUNCATE TABLE landgrid2.plss_township;',
                                   auto_commit=True)  # restart

        batch = []
        self.datastore.set_input_size(18)

        for layer in TOWNSHIPS[:]:
            child_path = os.path.join(self.tmp_dir, f'{layer}.shp')
            child_df = gpd.read_file(child_path)
            child_df.sindex

            logger.info(f"Computing overlaps for {layer}.shp...")

            olap_df = self.compute_overlaps(state_df, county_df, child_df)

            logger.info(f"Writing {layer} to db.")

            # TODO:
            # olap_df.where(pd.notnull(olap_df), None)

            for rec_i, rec in enumerate(olap_df.itertuples()):

                g_json = geojson.dumps(mapping(rec.geometry.envelope))
                twp = None if np.isnan(rec.TWP) else rec.TWP
                thalf = None if np.isnan(rec.THALF) else rec.THALF
                rge = None if np.isnan(rec.RGE) else rec.RGE
                rhalf = None if np.isnan(rec.RHALF) else rec.RHALF
                solap = None if pd.isna(rec.StateOlap) else rec.StateOlap
                colap = None if pd.isna(rec.CountyOlap) else rec.CountyOlap

                try:
                    batch.append((
                        rec.TWPCODE,
                        rec.MER,
                        rec.MST,
                        twp,
                        thalf,
                        rec.TNS,
                        rge,
                        rhalf,
                        rec.REW,
                        # rec['SecCount'],
                        rec.TWPLabel,  # TODO: Split and reuse?
                        rec.Shape_Leng,  # Shape_Length
                        rec.Shape_Area,
                        layer.split('_')[0],  # TMP
                        solap,
                        colap,
                        self.__create_label(twp, thalf, rec.TNS),
                        self.__create_label(rge, rhalf, rec.REW),
                        g_json,
                        rec.geometry.wkb
                    ))

                    if rec_i % self.__BATCH_SIZE == 0:
                        self.datastore.write_batch(dml, batch)
                        batch.clear()
                        logger.info(f"Wrote {rec_i} records...")

                except Exception as e:
                    logger.exception(f"Error writing {rec}", e)
                    raise e

            if batch is not None:
                self.datastore.write_batch(dml, batch)
                batch.clear()
                logger.info(f"Wrote {rec_i} records...")

            self.datastore.batch_commit()  # commit after each layer

        return

    def sections_to_sql(self, state_df, county_df):
        dml = """
        INSERT INTO landgrid2.plss_section (StateID, StateAPI, TWPCODE,
                                            SECCODE, MER, MST, TWP, THALF,
                                            TNS, RGE, RHALF, REW, SEC,
                                            Shape_Length, Shape_Area,
                                            State_Name, State_Overlaps, 
                                            County_Overlaps, Township, 
                                            Range, geobounds, shape)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, geometry::STGeomFromWKB(?, 4326));
        """
        self.datastore.execute_dml('TRUNCATE TABLE landgrid2.plss_section;',
                                   auto_commit=True)  # restart

        batch = []
        self.datastore.set_input_size(21)

        for layer in SECTIONS[:]:

            splits = glob(os.path.join(self.tmp_dir, f'{layer}_*.shp'))
            splits.sort()
            
            for child_path in splits[:]:
                child_df = gpd.read_file(child_path)
                child_df.sindex

                logger.info(f"Computing overlaps for {os.path.split(child_path)[1]}...")

                olap_df = self.compute_overlaps(state_df, county_df, child_df)

                logger.info(f"Writing {child_path} to db.")

                # TODO:
                # olap_df.where(pd.notnull(olap_df), None)

                # TODO: Consider gpd.iterfeatures?
                for rec_i, rec in enumerate(olap_df.itertuples()):

                    g_json = geojson.dumps(mapping(rec.geometry.envelope))

                    # TODO: Maybe inplace fillna(None) is faster?
                    state_id = None if np.isnan(rec.StateID) else rec.StateID
                    twp = None if np.isnan(rec.TWP) else rec.TWP
                    thalf = None if np.isnan(rec.THALF) else rec.THALF
                    rge = None if np.isnan(rec.RGE) else rec.RGE
                    rhalf = None if np.isnan(rec.RHALF) else rec.RHALF
                    sec = None if np.isnan(rec.SEC) else rec.SEC

                    batch.append((
                        state_id,
                        rec.StateAPI,
                        rec.TWPCODE,
                        rec.SECCODE,
                        rec.MER,
                        rec.MST,
                        twp,
                        thalf,
                        rec.TNS,
                        rge,
                        rhalf,
                        rec.REW,
                        sec,
                        rec.Shape_Leng,  # Shape_Length
                        rec.Shape_Area,
                        layer.split('_')[0],  # TMP
                        rec.StateOlap,
                        rec.CountyOlap,
                        self.__create_label(twp, thalf, rec.TNS),
                        self.__create_label(rge, rhalf, rec.REW),
                        g_json,
                        rec.geometry.wkb
                    ))

                    if rec_i % self.__BATCH_SIZE == 0:
                        self.datastore.write_batch(dml, batch)
                        batch.clear()
                        logger.info(f"Wrote {rec_i} records...")

                if batch:
                    self.datastore.write_batch(dml, batch)
                    batch.clear()
                    logger.info(f"Wrote {rec_i} records...")

                self.datastore.batch_commit()  # commit layer

    def pa_townships_to_sql(self, state_df, county_df):
        dml = """
        INSERT INTO landgrid2.pa_township (MSLINK, COUNTY, MUNICIPAL_, MUNICIPAL1,
                                           FIPS_MUN_C, FED_AID_UR, FIPS_COUNT,
                                           FIPS_AREA_, FIPS_NAME, FIPS_SQ_MI,
                                           FIPS_MUN_P, FED_ID_NUM, CLASS_OF_M,
                                           Shape_Length, Shape_Area, County_Name,
                                           County_TOWNSHIP, State_Name, State_Overlaps, 
                                           County_Overlaps, geobounds, shape)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, geometry::STGeomFromWKB(?, 4326));
        """
        self.datastore.execute_dml('TRUNCATE TABLE landgrid2.pa_township;',
                                   auto_commit=True)  # restart
        child_path = os.path.join(self.tmp_dir, f'{PA_TOWNSHIPS}.shp')
        child_df = gpd.read_file(child_path)
        child_df.rename(columns={'County_Nam': 'County_Na2'}, inplace=True)
        child_df.sindex

        logger.debug(f"Computing overlaps for {PA_TOWNSHIPS}...")

        olap_df = self.compute_overlaps(state_df, county_df, child_df)

        logger.info(f"Writing {PA_TOWNSHIPS} to db.")

        batch = []
        self.datastore.set_input_size(21)

        for rec_i, rec in enumerate(olap_df.itertuples()):
            g_json = geojson.dumps(mapping(rec.geometry.envelope))

            batch.append((
                rec.MSLINK,
                rec.COUNTY,
                rec.MUNICIPAL_,
                rec.MUNICIPAL1,
                rec.FIPS_MUN_C,
                rec.FED_AID_UR,
                rec.FIPS_COUNT,
                rec.FIPS_AREA_,
                rec.FIPS_NAME,
                rec.FIPS_SQ_MI,
                rec.FIPS_MUN_P,
                rec.FED_ID_NUM,
                rec.CLASS_OF_M,
                rec.Shape_Leng,  # Shape_Length
                rec.Shape_Area,
                rec.County_Na2,  # County_Name
                rec.County_TOW,  # County_TOWNSHIP
                'PA',  # TMP
                rec.StateOlap,
                rec.CountyOlap,
                g_json,
                rec.geometry.wkb
            ))

            if rec_i % self.__BATCH_SIZE == 0:
                self.datastore.write_batch(dml, batch)
                batch.clear()
                logger.info(f"Wrote {rec_i} records...")

        if batch:
            self.datastore.write_batch(dml, batch)
            batch.clear()
            logger.info(f"Wrote {rec_i} records...")

        self.datastore.batch_commit()

    def wv_districts_to_sql(self, state_df, county_df):
        dml = """
        INSERT INTO landgrid2.wv_district (WV_ID, DNAME, DNUMBER, CNAME, CNUMBER,
                                           Area_sqm, lat, long, Shape_Length,
                                           Shape_Area, County_District,
                                           State_Name, State_Overlaps, 
                                           County_Overlaps, geobounds, shape)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                geometry::STGeomFromWKB(?, 4326));
        """
        self.datastore.execute_dml('TRUNCATE TABLE landgrid2.wv_district;',
                                   auto_commit=True);  # restart
        child_path = os.path.join(self.tmp_dir, f'{WV_DISTRICTS}.shp')
        child_df = gpd.read_file(child_path)
        child_df.sindex

        logger.debug(f"Computing overlaps for {WV_DISTRICTS}...")

        olap_df = self.compute_overlaps(state_df, county_df, child_df)

        logger.info(f"Writing {WV_DISTRICTS} to db.")

        batch = []
        self.datastore.set_input_size(15)
        
        for rec_i, rec in enumerate(olap_df.itertuples()):
            g_json = geojson.dumps(mapping(rec.geometry.envelope))

            batch.append((
                rec.WV_ID,
                rec.DNAME,
                rec.DNUMBER,
                rec.CNAME,
                rec.CNUMBER,
                rec.Area_sqm,
                rec.lat,
                rec.long,
                rec.Shape_Leng,  # Shape_Length
                rec.Shape_Area,
                rec.County_Dis,  # County_District
                'WV',  # TMP
                rec.StateOlap,
                rec.CountyOlap,
                g_json,
                rec.geometry.wkb
            ))

            if rec_i % self.__BATCH_SIZE == 0:
                self.datastore.write_batch(dml, batch)
                batch.clear()
                logger.info(f"Wrote {rec_i} records...")

        if batch:
            self.datastore.write_batch(dml, batch)
            batch.clear()
            logger.info(f"Wrote {rec_i} records...")

        self.datastore.batch_commit()

    def tx_abstracts_to_sql(self, state_df, county_df):

        dml = """
        INSERT INTO landgrid2.tx_abstract (PERIMETER, FIPS, CountyName,
                                           Shape_Length, Shape_Area,
                                           AbstractNumber, AbstractName,
                                           Block, Township, Section,
                                           AbstractNameALT, FormNumber,
                                           ControlNumber, State_Name, 
                                           State_Overlaps, County_Overlaps,
                                           geobounds, shape)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, geometry::STGeomFromWKB(?, 4326));
        """
        self.datastore.execute_dml('TRUNCATE TABLE landgrid2.tx_abstract;',
                                   auto_commit=True);  # restart

        tx_path = os.path.join(self.tmp_dir, f'{TX_ABSTRACTS}.shp')

        logger.info(f"Reading {TX_ABSTRACTS}...")

        crs, schema, _ = get_shapefile_meta(tx_path)
        records = read_shapefile(tx_path, validate=False)

        logger.info(f"Splitting {TX_ABSTRACTS}...")

        splits = split_shapefile(records, crs, schema, tx_path)
        batch = []
        self.datastore.set_input_size(17)

        for child_path in splits[:]:

            child_df = gpd.read_file(child_path)
            child_df.sindex

            logger.info(f"Computing overlaps for {os.path.split(child_path)[1]}...")

            olap_df = self.compute_overlaps(state_df, county_df, child_df)

            logger.info(f"Writing {os.path.split(child_path)[1]} to db.")

            # TODO:
            # olap_df.where(pd.notnull(olap_df), None)

            for rec_i, rec in enumerate(olap_df.itertuples()):
                g_json = geojson.dumps(mapping(rec.geometry.envelope))
                perim = None if np.isnan(rec.PERIMETER) else rec.PERIMETER

                batch.append((
                    perim,
                    rec.FIPS,
                    rec.CountyName,
                    rec.Shape_Leng,  # Shape_Length
                    rec.Shape_Area,
                    rec.AbstractNu,  # AbstractNumber
                    rec.AbstractNa,  # AbstractName
                    rec.Block,
                    rec.Township,
                    rec.Section,
                    rec.Abstract_1,  # AbstractNameALT
                    rec.FormNumber,
                    rec.ControlNum,  # ControlNumber
                    'TX',  # TMP
                    rec.StateOlap,
                    rec.CountyOlap,
                    g_json,
                    rec.geometry.wkb
                ))

                if rec_i % self.__BATCH_SIZE == 0:
                    self.datastore.write_batch(dml, batch)
                    batch.clear()
                    logger.info(f"Wrote {rec_i} records...")

            if batch:
                self.datastore.write_batch(dml, batch)
                batch.clear()
                logger.info(f"Wrote {rec_i} records...")

            self.datastore.batch_commit()

    def tx_blocks_to_sql(self, state_df, county_df):
        """
        For Texas_Abstracts (310692), dissolve (Township, Block) => Block

        PostGIS reference:
        SELECT	f.township, f.block,
                ST_UnaryUnion(ST_Collect(f.the_geom)) AS Blocks,
                COUNT(*) AS CountGeom
        FROM	(
            SELECT 	countyname, township, block, (ST_Dump(shape)).geom AS the_geom
            FROM	landgrid.tx_abstract) AS f
        WHERE	f.countyname = 'Ector'
        GROUP BY f.township, f.block

        :param state_df:
        :param county_df:
        :return:
        """

        dml = """
        INSERT INTO landgrid2.tx_block (Block, Township, State_Name, 
                                        State_Overlaps, County_Overlaps,
                                        geobounds, shape)
        VALUES (?, ?, ?, ?, ?, ?, geometry::STGeomFromWKB(?, 4326));
        """
        self.datastore.execute_dml('TRUNCATE TABLE landgrid2.tx_block;',
                                   auto_commit=True);  # restart

        tx_path = os.path.join(self.tmp_dir, f'{TX_ABSTRACTS}.shp')
        tx_df = gpd.read_file(tx_path)

        # Excluding NULL Township, NULL Block as it results in a
        # MultiPolygon spanning the whole state.
        tx_df.dropna(how='all', subset=['Township', 'Block'],
                     inplace=True)
        tx_df.loc[tx_df.Township.isna(), ['Township']] = 'Missing'
        tx_df.loc[tx_df.Block.isna(), ['Block']] = 'Missing'

        logger.info(f"Dissolving TX Abstracts to Blocks...")

        tx_blocks_df = (tx_df.loc[:, ['Township', 'Block', 'geometry']]  # .copy()
                        .dissolve(by=['Township', 'Block'], aggfunc='first')
                        .reset_index()
                        )

        logger.info(f"De-aggregating {TX_BLOCKS}...")

        tx_blocks_df = de_aggregate(tx_blocks_df)
        tx_blocks_df.sindex

        logger.info(f"Computing overlaps for {TX_BLOCKS}...")

        olap_df = self.compute_overlaps(state_df, county_df, tx_blocks_df)

        # DEBUG
        # tx_block_path = os.path.join(self.tmp_dir, f'{TX_BLOCKS}_deagg2.shp')
        # olap_df.to_file(tx_block_path)

        logger.info(f"Writing {TX_BLOCKS} to db.")

        batch = []
        self.datastore.set_input_size(6)

        for rec_i, rec in enumerate(olap_df.itertuples()):
            g_json = geojson.dumps(mapping(rec.geometry.envelope))

            batch.append((
                rec.Block,
                rec.Township,
                'TX',  # TMP
                rec.StateOlap,
                rec.CountyOlap[:1024],
                g_json,
                rec.geometry.wkb
            ))

            if rec_i % self.__BATCH_SIZE == 0:
                self.datastore.write_batch(dml, batch)
                batch.clear()
                logger.info(f"Wrote {rec_i} records...")

        if batch:
            self.datastore.write_batch(dml, batch)
            batch.clear()
            logger.info(f"Wrote {rec_i} records...")

        self.datastore.batch_commit()

    def oh_munis_to_sql(self, state_df, county_df, sections_df):
        """
        Based on Ohio_Sections (73371)
        Dissolve (COUNTY, TOWNSHIP) => Municipality (1363)

        :param state_df:
        :param county_df:
        :param sections_df:
        :return:
        """

        dml = """
        INSERT INTO landgrid2.ohio_municipality (COUNTY, TOWNSHIP, 
                                                 State_Name, State_Overlaps, 
                                                 County_Overlaps, geobounds, 
                                                 shape)
        VALUES (?, ?, ?, ?, ?, ?, geometry::STGeomFromWKB(?, 4326));
        """
        self.datastore.execute_dml('TRUNCATE TABLE landgrid2.ohio_municipality;',
                                   auto_commit=True);  # restart

        logger.info(f"Dissolving OH Sections to Municipalities...")

        oh_munis_df = (sections_df.loc[:, ['COUNTY', 'TOWNSHIP', 'geometry']]  # .copy()
                       .dissolve(by=['COUNTY', 'TOWNSHIP'], aggfunc='first')
                       .reset_index()
                       )

        # DEBUG
        # oh_munis_path = os.path.join(self.tmp_dir, f'{OH_MUNIS}.shp')
        # oh_munis_df.to_file(oh_munis_path)

        oh_munis_df.sindex

        logger.info(f"Computing overlaps for {OH_MUNIS}...")

        olap_df = self.compute_overlaps(state_df, county_df, oh_munis_df)

        logger.info(f"Writing {OH_MUNIS} to db.")

        batch = []
        self.datastore.set_input_size(6)

        for rec_i, rec in enumerate(olap_df.itertuples()):
            g_json = geojson.dumps(mapping(rec.geometry.envelope))

            batch.append((
                rec.COUNTY,
                rec.TOWNSHIP,
                'OH',  # TMP
                rec.StateOlap,
                rec.CountyOlap[:1024],
                g_json,
                rec.geometry.wkb
            ))

            if rec_i % self.__BATCH_SIZE == 0:
                self.datastore.write_batch(dml, batch)
                batch.clear()
                logger.info(f"Wrote {rec_i} records...")

        if batch:
            self.datastore.write_batch(dml, batch)
            batch.clear()
            logger.info(f"Wrote {rec_i} records...")

        self.datastore.batch_commit()

    def oh_townships_to_sql(self, state_df, county_df, sections_df):
        """
        Based on Ohio_Sections (73371)
        Dissolve (COUNTY, TOWNSHIP, TWP, TNS, RGE, REW) => Township (2295)

        :param state_df:
        :param county_df:
        :param sections_df:
        :return:
        """

        dml = """
        INSERT INTO landgrid2.ohio_township (COUNTY, TOWNSHIP,
                                             TWP, TNS, RGE, REW, 
                                             State_Name, State_Overlaps, 
                                             County_Overlaps, geobounds, 
                                             shape)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                geometry::STGeomFromWKB(?, 4326));
        """
        self.datastore.execute_dml('TRUNCATE TABLE landgrid2.ohio_township;',
                                   auto_commit=True);  # restart

        logger.info(f"Dissolving OH Sections to Townships...")

        # tns, rew can be NULL
        # NOTE: This will update the dataframe used by the section dissolve.
        sections_df.loc[sections_df.TNS.isna(), ['TNS']] = ''
        sections_df.loc[sections_df.REW.isna(), ['REW']] = ''

        oh_twp_df = (sections_df.loc[:, ['COUNTY', 'TOWNSHIP', 'TWP', 'TNS',
                                         'RGE', 'REW', 'geometry']]  # .copy()
                     .dissolve(by=['COUNTY', 'TOWNSHIP', 'TWP', 'TNS',
                                   'RGE', 'REW'], aggfunc='first')
                     .reset_index()
                     )
        oh_twp_df.sindex

        # DEBUG
        # oh_twp_path = os.path.join(self.tmp_dir, f'{OH_TOWNSHIPS}.shp')
        # oh_twp_df.to_file(oh_twp_path)

        logger.info(f"Computing overlaps for {OH_TOWNSHIPS}...")

        olap_df = self.compute_overlaps(state_df, county_df, oh_twp_df)

        logger.info(f"Writing {OH_TOWNSHIPS} to db.")

        batch = []
        self.datastore.set_input_size(10)

        for rec_i, rec in enumerate(olap_df.itertuples()):
            g_json = geojson.dumps(mapping(rec.geometry.envelope))

            batch.append((
                rec.COUNTY,
                rec.TOWNSHIP,
                rec.TWP,
                rec.TNS,
                rec.RGE,
                rec.REW,
                'OH',  # TMP
                rec.StateOlap,
                rec.CountyOlap[:1024],
                g_json,
                rec.geometry.wkb
            ))

            if rec_i % self.__BATCH_SIZE == 0:
                self.datastore.write_batch(dml, batch)
                batch.clear()
                logger.info(f"Wrote {rec_i} records...")

        if batch:
            self.datastore.write_batch(dml, batch)
            batch.clear()
            logger.info(f"Wrote {rec_i} records...")

        self.datastore.batch_commit()

    def oh_sections_to_sql(self, state_df, county_df, sections_df):
        """
        Based on Ohio_Sections (73371)
        Dissolve (COUNTY, TOWNSHIP, TWP, TNS, RGE, REW, SEC) => Section (28834)

        :param state_df:
        :param county_df:
        :param sections_df:
        :return:
        """

        dml = """
        INSERT INTO landgrid2.ohio_section (COUNTY, TOWNSHIP, 
                                            TWP, TNS, RGE, REW, SEC,
                                            State_Name, State_Overlaps, 
                                            County_Overlaps, geobounds, 
                                            shape)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                geometry::STGeomFromWKB(?, 4326));
        """
        self.datastore.execute_dml('TRUNCATE TABLE landgrid2.ohio_section;',
                                   auto_commit=True);  # restart

        logger.info(f"Dissolving to OH Sections...")

        # tns, rew can be NULL.
        sections_df.loc[sections_df.TNS.isna(), ['TNS']] = ''
        sections_df.loc[sections_df.REW.isna(), ['REW']] = ''

        oh_sec_df = (sections_df.loc[:, ['COUNTY', 'TOWNSHIP', 'TWP', 'TNS',
                                         'RGE', 'REW', 'SEC', 'geometry']]  # .copy()
                     .dissolve(by=['COUNTY', 'TOWNSHIP', 'TWP', 'TNS',
                                   'RGE', 'REW', 'SEC'], aggfunc='first')
                     .reset_index()
                     )

        oh_twp_path = os.path.join(self.tmp_dir, f'{OH_SECTIONS}_dissolved.shp')
        oh_sec_df.to_file(oh_twp_path)

        crs, schema, _ = get_shapefile_meta(oh_twp_path)
        records = read_shapefile(oh_twp_path, validate=False)

        logger.info(f"Splitting {OH_SECTIONS}...")

        splits = split_shapefile(records, crs, schema, oh_twp_path)

        batch = []
        self.datastore.set_input_size(11)

        for child_path in splits[:]:

            child_df = gpd.read_file(child_path)
            child_df.sindex

            logger.info(f"Computing overlaps for {os.path.split(child_path)[1]}...")

            olap_df = self.compute_overlaps(state_df, county_df, child_df)

            logger.info(f"Writing {os.path.split(child_path)[1]} to db.")

            for rec_i, rec in enumerate(olap_df.itertuples()):
                g_json = geojson.dumps(mapping(rec.geometry.envelope))

                batch.append((
                    rec.COUNTY,
                    rec.TOWNSHIP,
                    rec.TWP,
                    rec.TNS,
                    rec.RGE,
                    rec.REW,
                    rec.SEC,
                    'OH',  # TMP
                    rec.StateOlap,
                    rec.CountyOlap,
                    g_json,
                    rec.geometry.wkb
                ))

                if rec_i % self.__BATCH_SIZE == 0:
                    self.datastore.write_batch(dml, batch)
                    batch.clear()
                    logger.info(f"Wrote {rec_i} records...")

            if batch:
                self.datastore.write_batch(dml, batch)
                batch.clear()
                logger.info(f"Wrote {rec_i} records...")

            self.datastore.batch_commit()

    def load_states(self):
        dml = """
        INSERT INTO landgrid2.state_us (State_Name, Shape_Length,
                                        Shape_Area, geobounds, shape)
        VALUES (?, ?, ?, ?, geometry::STGeomFromWKB(?, 4326));
        """
        self.datastore.execute_dml('TRUNCATE TABLE landgrid2.state_us;');  # restart
        shapefile_path = os.path.join(self.tmp_dir, f'{US_STATES}.shp')

        batch = []
        self.datastore.set_input_size(4)

        for rec_i, rec in enumerate(read_shapefile(shapefile_path, 
                                                   validate=False)):  # already cleaned

            poly = shape(rec['geometry'])

            # Check for anti-meridian and split polygon if necessary.
            poly_fix = fix_anti_meridian(poly)

            g_json = geojson.dumps(mapping(poly_fix.envelope))

            batch.append((
                rec['properties']['State_Name'],
                rec['properties']['Shape_Leng'],  # Shape_Length
                rec['properties']['Shape_Area'],
                g_json,
                poly.wkb
            ))

            if rec_i % self.__BATCH_SIZE == 0:
                self.datastore.write_batch(dml, batch)
                batch.clear()
                logger.info(f"Wrote {rec_i} records...")

        if batch:
            self.datastore.write_batch(dml, batch)
            batch.clear()
            logger.info(f"Wrote {rec_i} records...")

        self.datastore.batch_commit()

    def load_counties(self):
        dml = """
        INSERT INTO landgrid2.county_us (County_Name, State_Name, CountyID,
                                         StateID, FIPS_State, FIPS_County,
                                         API_State, API_County, LAT, LON,
                                         Shape_Length, Shape_Area, geobounds,
                                         shape)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                geometry::STGeomFromWKB(?, 4326));
        """
        self.datastore.execute_dml('TRUNCATE TABLE landgrid2.county_us;');  # restart
        shapefile_path = os.path.join(self.tmp_dir, f'{US_COUNTIES}.shp')

        batch = []
        self.datastore.set_input_size(13)

        for rec_i, rec in enumerate(read_shapefile(shapefile_path, 
                                                   validate=False)):

            poly = shape(rec['geometry'])

            # Check for anti-meridian and split polygon if necessary.
            poly_fix = fix_anti_meridian(poly)

            g_json = geojson.dumps(mapping(poly_fix.envelope))

            batch.append((
                rec['properties']['County_Nam'],  # County_Name
                rec['properties']['State_Name'],
                rec['properties']['CountyID'],
                rec['properties']['StateID'],
                rec['properties']['FIPS_State'],
                rec['properties']['FIPS_Count'],  # FIPS_County
                rec['properties']['API_State'],
                rec['properties']['API_County'],
                rec['properties']['LAT'],
                rec['properties']['LON'],
                rec['properties']['Shape_Leng'],  # Shape_Length
                rec['properties']['Shape_Area'],
                g_json,
                poly.wkb
            ))

            if rec_i % self.__BATCH_SIZE == 0:
                self.datastore.write_batch(dml, batch)
                batch.clear()
                logger.info(f"Wrote {rec_i} records...")

        if batch:
            self.datastore.write_batch(dml, batch)
            batch.clear()
            logger.info(f"Wrote {rec_i} records...")

        self.datastore.batch_commit()

    def __load_oh_sections(self, sections_df):

        dml = """
        INSERT INTO landgrid2.ohio_section_base (SUBDIV_NM, TWP, TNS, RGE, REW, SEC,
                                                 QTR_TWP, ALLOTMENT, TRACT, LOT, DIVISION,
                                                 FRACTION, COUNTY, TOWNSHIP, SURVEY_TYP,
                                                 ObjectID, VMSLOT, OTHER_SUB, Shape_Length,
                                                 Shape_Area, State_Name, geobounds, shape)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, geometry::STGeomFromWKB(?, 4326));
        """
        self.datastore.execute_dml('TRUNCATE TABLE landgrid2.ohio_section_base;');  # restart

        batch = []
        self.datastore.set_input_size(22)

        for rec_i, rec in enumerate(sections_df.itertuples()):
            g_json = geojson.dumps(mapping(rec.geometry.envelope))

            batch.append((
                rec.SUBDIV_NM,
                rec.TWP,
                rec.TNS,
                rec.RGE,
                rec.REW,
                rec.SEC,
                rec.QTR_TWP,
                rec.ALLOTMENT,
                rec.TRACT,
                rec.LOT,
                rec.DIVISION,
                rec.FRACTION,
                rec.COUNTY,
                rec.TOWNSHIP,
                rec.SURVEY_TYP,
                rec.ObjectID,
                rec.VMSLOT,
                rec.OTHER_SUB,
                rec.Shape_Le_1,  # Shape_Length
                rec.Shape_Area,
                'OH',  # TMP
                g_json,
                rec.geometry.wkb
            ))

            if rec_i % self.__BATCH_SIZE == 0:
                self.datastore.write_batch(dml, batch)
                batch.clear()
                logger.info(f"Wrote {rec_i} records...")

        if batch:
            self.datastore.write_batch(dml, batch)
            batch.clear()
            logger.info(f"Wrote {rec_i} records...")

        self.datastore.batch_commit()

    def __create_label(self, label_id, half, direction):
        """
        Taken from fme workbench.
        
        :param label_id: 
        :param half: 
        :param direction: 
        :return: 
        """
        if label_id is None:
            id_string = ''
        else:
            id_string = self.__prepend_zero(str(label_id))

        if half == 50:
            half_string = '.5'
        else:
            half_string = ''

        if direction is None:
            direction_string = ''
        else:
            direction_string = str(direction)

        return id_string + half_string + direction_string

    def __prepend_zero(self, field):
        """
        Taken from fme workench.
        
        :param field: 
        :return: 
        """
        base = self.splitter.split(field)[0]

        if base is not None and len(base) == 1 and base[0] != '0':
            return '0' + field
        else:
            return field
