

# TODO: Add dictionary specifying insert, delete queries as well as
#   batch type (single, split) per layer
US_STATES = 'States_US'
US_COUNTIES = 'Counties_US_WGS84'
PA_TOWNSHIPS = 'Pennsylvania_Townships'
WV_DISTRICTS = 'West_Virginia_Districts'
OH_SECTIONS = 'Ohio_Sections'
OH_MUNIS = 'Ohio_Municipalities'
OH_TOWNSHIPS = 'Ohio_Townships'
TX_ABSTRACTS = 'Texas_Abstracts'
TX_BLOCKS = 'Texas_Blocks'
TOWNSHIPS = [
    'AL_township',
    'AR_township',
    'AZ_township',
    'CA_township',
    'CO_township',
    'FL_township',
    'ID_township',
    'IL_township',
    'IN_township',
    'KS_township',
    'LA_township',
    'MI_township',
    'MO_township',
    'MS_township',
    'MT_township',
    'ND_township',
    'NE_township',
    'NM_township',
    'NV_township',
    'OK_township',
    'OR_township',
    'SD_township',
    'UT_township',
    'WA_township',
    'WY_township',
]
SECTIONS = [
    'AL_section',
    'AR_section',
    'AZ_section',
    'CA_section',
    'CO_section',
    'FL_section',
    'ID_section',
    'IL_section',
    'IN_section',
    'KS_section',
    'LA_section',
    'MI_section',
    'MO_section',
    'MS_section',
    'MT_section',
    'ND_section',
    'NE_section',
    'NM_section',
    'NV_section',
    'OK_section',
    'OR_section',
    'SD_section',
    'UT_section',
    'WA_section',
    'WY_section',
]

# TODO: Consider using named tupes as layer descriptors for attributes

# PostgreSQL
# dml = """
# INSERT INTO landgrid.plss_township (TWPCODE, MER, MST, TWP, THALF,
#                                     TNS, RGE, RHALF, REW, /*SecCount,*/
#                                     TWPLabel, Shape_Length, Shape_Area,
#                                     State_Name, State_Overlaps,
#                                     County_Overlaps, Township, Range,
#                                     geobounds, shape)
# VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
#         %s, %s, ST_GeomFromText(%s, 4326));
# """
# dml = """
# INSERT INTO landgrid.plss_section (StateID, StateAPI, TWPCODE,
#                                    SECCODE, MER, MST, TWP, THALF,
#                                    TNS, RGE, RHALF, REW, SEC,
#                                    Shape_Length, Shape_Area,
#                                    State_Name, State_Overlaps,
#                                    County_Overlaps, Township,
#                                    Range, geobounds, shape)
# VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
#         %s, %s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326));
# """
# dml = """
# INSERT INTO landgrid.pa_township (MSLINK, COUNTY, MUNICIPAL_, MUNICIPAL1,
#                                   FIPS_MUN_C, FED_AID_UR, FIPS_COUNT,
#                                   FIPS_AREA_, FIPS_NAME, FIPS_SQ_MI,
#                                   FIPS_MUN_P, FED_ID_NUM, CLASS_OF_M,
#                                   Shape_Length, Shape_Area, County_Name,
#                                   County_TOWNSHIP, State_Name, State_Overlaps,
#                                   County_Overlaps, geobounds, shape)
# VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
#         %s, %s, %s, %s, ST_GeomFromText(%s, 4326));
# """
# dml = """
# INSERT INTO landgrid.wv_district (WV_ID, DNAME, DNUMBER, CNAME, CNUMBER,
#                                   Area_sqm, lat, long, Shape_Length,
#                                   Shape_Area, County_District,
#                                   State_Name, State_Overlaps,
#                                   County_Overlaps, geobounds, shape)
# VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
#         ST_GeomFromText(%s, 4326));
# """
# dml = """
# INSERT INTO landgrid.tx_abstract (PERIMETER, FIPS, CountyName,
#                                   Shape_Length, Shape_Area,
#                                   AbstractNumber, AbstractName,
#                                   Block, Township, Section,
#                                   AbstractNameALT, FormNumber,
#                                   ControlNumber, State_Name,
#                                   State_Overlaps, County_Overlaps,
#                                   geobounds, shape)
# VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
#         %s, %s, %s, ST_GeomFromText(%s, 4326));
# """
# dml = """
# INSERT INTO landgrid.tx_block (Block, Township, State_Name,
#                                State_Overlaps, County_Overlaps,
#                                geobounds, shape)
# VALUES (%s, %s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326));
# """
# dml = """
# INSERT INTO landgrid.ohio_municipality (COUNTY, TOWNSHIP,
#                                         State_Name, State_Overlaps,
#                                         County_Overlaps, geobounds,
#                                         shape)
# VALUES (%s, %s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326));
# """
# dml = """
# INSERT INTO landgrid.ohio_township (COUNTY, TOWNSHIP,
#                                     TWP, TNS, RGE, REW,
#                                     State_Name, State_Overlaps,
#                                     County_Overlaps, geobounds,
#                                     shape)
# VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
#         ST_GeomFromText(%s, 4326));
# """
# dml = """
# INSERT INTO landgrid.ohio_section (COUNTY, TOWNSHIP,
#                                    TWP, TNS, RGE, REW, SEC,
#                                    State_Name, State_Overlaps,
#                                    County_Overlaps, geobounds,
#                                    shape)
# VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
#         ST_GeomFromText(%s, 4326));
# """
# dml = """
# INSERT INTO landgrid.state_us (State_Name, Shape_Length,
#                                Shape_Area, geobounds, shape)
# VALUES (%s, %s, %s, %s, ST_GeomFromText(%s, 4326));
# """
# dml = """
# INSERT INTO landgrid.county_us (County_Name, State_Name, CountyID,
#                                 StateID, FIPS_State, FIPS_County,
#                                 API_State, API_County, LAT, LON,
#                                 Shape_Length, Shape_Area, geobounds,
#                                 shape)
# VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
#         ST_GeomFromText(%s, 4326));
# """
# dml = """
# INSERT INTO landgrid.ohio_section_base (SUBDIV_NM, TWP, TNS, RGE, REW, SEC,
#                                         QTR_TWP, ALLOTMENT, TRACT, LOT, DIVISION,
#                                         FRACTION, COUNTY, TOWNSHIP, SURVEY_TYP,
#                                         ObjectID, VMSLOT, OTHER_SUB, Shape_Length,
#                                         Shape_Area, State_Name, geobounds, shape)
# VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
#         %s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326));
# """
# Subdivide
# dml2 = """
# INSERT INTO landgrid.state_us_grid (State_Name, shape)
# SELECT 	State_Name, ST_Subdivide(shape, 255) AS grid_shape
# FROM	landgrid.state_us;
# """
# dml2 = """
# INSERT INTO landgrid.county_us_grid (State_Name, shape)
# SELECT 	county_name, ST_Subdivide(shape, 255) AS grid_shape
# FROM	landgrid.county_us;
# """
