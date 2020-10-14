DROP SCHEMA IF EXISTS landgrid CASCADE;
CREATE SCHEMA landgrid;

-- TODO: Can create a trigger to listen to geometry changes
-- via: NOT ST_Equals(OLD.geom, NEW.geom).
CREATE TABLE landgrid.state_us
(
    StateId         SERIAL                          NOT NULL
        PRIMARY KEY,
    State_Name      VARCHAR(50)                     NULL,
    Shape_Length    REAL                            NULL,
    Shape_Area      REAL                            NULL,
    -- TODO: Store as JSON?
    geobounds       VARCHAR(1024)                   NULL,
    shape           GEOMETRY(GEOMETRY, 4326)        NULL
        --CHECK (ST_IsValid(shape))
);

CREATE TABLE landgrid.state_us_grid
(
    StateId        SERIAL                        NOT NULL
        PRIMARY KEY,
    State_Name     VARCHAR(50)                   NULL,
	shape		   GEOMETRY(GEOMETRY, 4326)   	 NULL
);

CREATE TABLE landgrid.county_us
(
    CountyKey      SERIAL                         NOT NULL
        PRIMARY KEY,
    County_Name    VARCHAR(50)                    NULL,
    State_Name     VARCHAR(50)                    NULL,
    CountyID       INTEGER                        NULL,
    StateID        INTEGER                        NULL,
    FIPS_State     CHAR(2)                        NULL,
    FIPS_County    CHAR(3)                        NULL,
    API_State      CHAR(2)                        NULL,
    API_County     CHAR(3)                        NULL,
    LAT            REAL                           NULL,
    LON            REAL                           NULL,
    Shape_Length   REAL                           NULL,
    Shape_Area     REAL                           NULL,
    geobounds      VARCHAR(1024)                  NULL,
    shape          GEOMETRY(GEOMETRY, 4326)       NULL
);

CREATE TABLE landgrid.county_us_grid
(
    CountyId      SERIAL                         NOT NULL
        PRIMARY KEY,
    County_Name    VARCHAR(50)                    NULL,
    shape          GEOMETRY(GEOMETRY, 4326)       NULL
);

CREATE TABLE landgrid.plss_township
(
    TownshipID        SERIAL                         NOT NULL
        PRIMARY KEY,
    TWPCODE           VARCHAR(24)                    NULL,
    MER               VARCHAR(5)                     NULL,
    MST               VARCHAR(20)                    NULL,
    TWP               INTEGER                        NULL,
    THALF             INTEGER                        NULL,
    TNS               CHAR(1)                        NULL,
    RGE               INTEGER                        NULL,
    RHALF             INTEGER                        NULL,
    REW               CHAR(1)                        NULL,
    SecCount          INTEGER                        NULL,
    TWPLabel          VARCHAR(20)                    NULL,
    Shape_Length      REAL                           NULL,
    Shape_Area        REAL                           NULL,
    State_Name        VARCHAR(50)                    NULL,
    State_Overlaps    VARCHAR(512)                   NULL,
    County_Name       VARCHAR(50)                    NULL,
    County_Overlaps   VARCHAR(1024)                  NULL,
    Township          VARCHAR(64)                    NULL,
    Range             VARCHAR(64)                    NULL,
    -- TODO: Store as JSON?
    geobounds         VARCHAR(1024)                  NULL,
    -- Support both Polygon and MultiPolygon
    shape             GEOMETRY(GEOMETRY, 4326)       NULL
);

CREATE TABLE landgrid.plss_section
(
    SectionID           SERIAL                          NOT NULL
        PRIMARY KEY,
    StateID             INTEGER                         NULL,
    StateAPI            CHAR(2)                         NULL,
    TWPCODE             VARCHAR(24)                     NULL,
    SECCODE             VARCHAR(20)                     NULL,
    MER                 VARCHAR(5)                      NULL,
    MST                 VARCHAR(20)                     NULL,
    TWP                 INTEGER                         NULL,
    THALF               INTEGER                         NULL,
    TNS                 CHAR(1)                         NULL,
    RGE                 INTEGER                         NULL,
    RHALF               INTEGER                         NULL,
    REW                 CHAR(1)                         NULL,
    SEC                 INTEGER                         NULL,
    Shape_Length        REAL                            NULL,
    Shape_Area          REAL                            NULL,
    State_Name          VARCHAR(50)                     NULL,
    State_Overlaps      VARCHAR(512)                    NULL,
    County_Name         VARCHAR(50)                     NULL,
    County_Overlaps     VARCHAR(1024)                   NULL,
    Township            VARCHAR(64)                     NULL,
    Range               VARCHAR(64)                     NULL,
    -- TODO: Store as JSON?
    geobounds           VARCHAR(1024)                   NULL,
    -- Support both Polygon and MultiPolygon
    shape               GEOMETRY(GEOMETRY, 4326)        NULL
);

CREATE TABLE landgrid.ohio_section_base
(
    SectionId         SERIAL                         NOT NULL
        PRIMARY KEY,
    SUBDIV_NM         VARCHAR(55)                    NULL,
    TWP               INT                            NULL,
    TNS               CHAR(1)                        NULL,
    RGE               INT                            NULL,
    REW               CHAR(1)                        NULL,
    SEC               INT                            NULL,
    QTR_TWP           CHAR(2)                        NULL,
    ALLOTMENT         VARCHAR(55)                    NULL,
    TRACT             VARCHAR(35)                    NULL,
    LOT               VARCHAR(24)                    NULL,
    DIVISION          VARCHAR(24)                    NULL,
    FRACTION          INT                            NULL,
    COUNTY            CHAR(11)                       NULL,
    TOWNSHIP          VARCHAR(50)                    NULL,
    SURVEY_TYP        VARCHAR(50)                    NULL,
    ObjectID          INT                            NULL,
    VMSLOT            VARCHAR(50)                    NULL,
    OTHER_SUB         VARCHAR(65)                    NULL,
    Shape_Length      FLOAT                          NULL,
    Shape_Area        FLOAT                          NULL,
    State_Name        VARCHAR(50)                    NULL,
    State_Overlaps    VARCHAR(512)                   NULL,
    County_Name       VARCHAR(50)                    NULL,
    County_Overlaps   VARCHAR(1024)                  NULL,
    geobounds         VARCHAR(1024)                  NULL,
    shape             GEOMETRY(GEOMETRY, 4326)       NULL
);

CREATE TABLE landgrid.ohio_municipality
(
    MunicipalityId    SERIAL                         NOT NULL
        PRIMARY KEY,
    COUNTY            CHAR(11)                       NULL,
    TOWNSHIP          VARCHAR(50)                    NULL,
    State_Name        VARCHAR(50)                    NULL,
    State_Overlaps    VARCHAR(512)                   NULL,
    --County_Name       VARCHAR(50)                    NULL,
    County_Overlaps   VARCHAR(1024)                  NULL,
    geobounds         VARCHAR(1024)                  NULL,
    shape             GEOMETRY(GEOMETRY, 4326)       NULL
);

CREATE TABLE landgrid.ohio_township
(
    TownshipId         SERIAL                         NOT NULL
        PRIMARY KEY,
    COUNTY            CHAR(11)                       NULL,
    TOWNSHIP          VARCHAR(50)                    NULL,
    TWP               INT                            NULL,
    TNS               CHAR(1)                        NULL,
    RGE               INT                            NULL,
    REW               CHAR(1)                        NULL,
    State_Name        VARCHAR(50)                    NULL,
    State_Overlaps    VARCHAR(512)                   NULL,
    --County_Name       VARCHAR(50)                    NULL,
    County_Overlaps   VARCHAR(1024)                  NULL,
    geobounds         VARCHAR(1024)                  NULL,
    shape             GEOMETRY(GEOMETRY, 4326)       NULL
);

CREATE TABLE landgrid.ohio_section
(
    SectionId         SERIAL                         NOT NULL
        PRIMARY KEY,
    COUNTY            CHAR(11)                       NULL,
    TOWNSHIP          VARCHAR(50)                    NULL,
    TWP               INT                            NULL,
    TNS               CHAR(1)                        NULL,
    RGE               INT                            NULL,
    REW               CHAR(1)                        NULL,
    SEC               INT                            NULL,
    State_Name        VARCHAR(50)                    NULL,
    State_Overlaps    VARCHAR(512)                   NULL,
    --County_Name       VARCHAR(50)                    NULL,
    County_Overlaps   VARCHAR(1024)                  NULL,
    geobounds         VARCHAR(1024)                  NULL,
    shape             GEOMETRY(GEOMETRY, 4326)       NULL
);

CREATE TABLE landgrid.pa_township
(
    TownshipId          SERIAL                      NOT NULL
        PRIMARY KEY,
    MSLINK              FLOAT                       NULL,
    COUNTY              CHAR(2)                     NULL,
    MUNICIPAL_          CHAR(3)                     NULL,
    MUNICIPAL1          VARCHAR(20)                 NULL,
    FIPS_MUN_C          VARCHAR(5)                  NULL,
    FED_AID_UR          CHAR(1)                     NULL,
    FIPS_COUNT          CHAR(3)                     NULL,
    FIPS_AREA_          VARCHAR(5)                  NULL,
    FIPS_NAME           VARCHAR(16)                 NULL,
    FIPS_SQ_MI          FLOAT                       NULL,
    FIPS_MUN_P          FLOAT                       NULL,
    FED_ID_NUM          VARCHAR(10)                 NULL,
    CLASS_OF_M          VARCHAR(4)                  NULL,
    Shape_Length        FLOAT                       NULL,
    Shape_Area          FLOAT                       NULL,
    County_Name         VARCHAR(30)                 NULL,
    County_TOWNSHIP     VARCHAR(40)                 NULL,
    State_Name          VARCHAR(50)                 NULL,
    State_Overlaps      VARCHAR(512)                NULL,
--    County_Name         VARCHAR(50)                 NULL,
    County_Overlaps     VARCHAR(1024)               NULL,
    geobounds           VARCHAR(1024)               NULL,
    shape               GEOMETRY(GEOMETRY, 4326)    NULL
);

CREATE TABLE landgrid.wv_district
(
    DistrictId          SERIAL                      NOT NULL
        PRIMARY KEY,
    WV_ID               INTEGER                     NULL,
    DNAME               VARCHAR(32)                 NULL,
    DNUMBER             VARCHAR(32)                 NULL,
    CNAME               VARCHAR(32)                 NULL,
    CNUMBER             VARCHAR(32)                 NULL,
    Area_sqm            FLOAT                       NULL,
    lat                 FLOAT                       NULL,
    long                FLOAT                       NULL,
    Shape_Length        FLOAT                       NULL,
    Shape_Area          FLOAT                       NULL,
    County_District     VARCHAR(50)                 NULL,
    State_Name          VARCHAR(50)                 NULL,
    State_Overlaps      VARCHAR(512)                NULL,
    County_Name         VARCHAR(50)                 NULL,
    County_Overlaps     VARCHAR(1024)               NULL,
    geobounds           VARCHAR(1024)               NULL,
    shape               GEOMETRY(GEOMETRY, 4326)    NULL
);

CREATE TABLE landgrid.tx_abstract
(
    AbstractId          SERIAL                      NOT NULL
        PRIMARY KEY,
    PERIMETER           FLOAT                       NULL,
    FIPS                CHAR(3)                     NULL,
    CountyName          VARCHAR(30)                 NULL,
    Shape_Length        FLOAT                       NULL,
    Shape_Area          FLOAT                       NULL,
    AbstractNumber      VARCHAR(12)                 NULL,
    AbstractName        VARCHAR(32)                 NULL,
    Block               VARCHAR(10)                 NULL,
    Township            VARCHAR(10)                 NULL,
    Section             VARCHAR(8)                  NULL,
    AbstractNameALT     VARCHAR(32)                 NULL,
    FormNumber          VARCHAR(9)                  NULL,
    ControlNumber       VARCHAR(9)                  NULL,
    State_Name          VARCHAR(50)                 NULL,
    State_Overlaps      VARCHAR(512)                NULL,
--    County_Name         VARCHAR(50)                 NULL,
    County_Overlaps     VARCHAR(1024)               NULL,
    geobounds           VARCHAR(1024)               NULL,
    shape               GEOMETRY(GEOMETRY, 4326)    NULL
);

CREATE TABLE landgrid.tx_block
(
    BlockId          SERIAL                      NOT NULL
        PRIMARY KEY,
    Block               VARCHAR(10)                 NULL,
    Township            VARCHAR(10)                 NULL,
    State_Name          VARCHAR(50)                 NULL,
    State_Overlaps      VARCHAR(512)                NULL,
--    County_Name         VARCHAR(50)                 NULL,
    County_Overlaps     VARCHAR(1024)               NULL,
    geobounds           VARCHAR(1024)               NULL,
    shape               GEOMETRY(GEOMETRY, 4326)    NULL
);