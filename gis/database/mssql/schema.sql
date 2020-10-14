-- USE DS9;
-- GO

-- TODO: Add create/modified date, error status.
-- TODO: Check which fields need to be unicode.
IF OBJECT_ID(N'landgrid2.state_us', N'U') IS NOT NULL
	DROP TABLE landgrid2.state_us;

IF OBJECT_ID(N'landgrid2.county_us', N'U') IS NOT NULL
	DROP TABLE landgrid2.county_us;

IF OBJECT_ID(N'landgrid2.plss_township', N'U') IS NOT NULL
	DROP TABLE landgrid2.plss_township;

IF OBJECT_ID(N'landgrid2.plss_section', N'U') IS NOT NULL
	DROP TABLE landgrid2.plss_section;

IF OBJECT_ID(N'landgrid2.ohio_section_base', N'U') IS NOT NULL
	DROP TABLE landgrid2.ohio_section_base;

IF OBJECT_ID(N'landgrid2.ohio_municipality', N'U') IS NOT NULL
	DROP TABLE landgrid2.ohio_municipality;

IF OBJECT_ID(N'landgrid2.ohio_township', N'U') IS NOT NULL
	DROP TABLE landgrid2.ohio_township;

IF OBJECT_ID(N'landgrid2.ohio_section', N'U') IS NOT NULL
	DROP TABLE landgrid2.ohio_section;

IF OBJECT_ID(N'landgrid2.pa_township', N'U') IS NOT NULL
	DROP TABLE landgrid2.pa_township;

IF OBJECT_ID(N'landgrid2.wv_district', N'U') IS NOT NULL
	DROP TABLE landgrid2.wv_district;

IF OBJECT_ID(N'landgrid2.tx_abstract', N'U') IS NOT NULL
	DROP TABLE landgrid2.tx_abstract;

IF OBJECT_ID(N'landgrid2.tx_block', N'U') IS NOT NULL
	DROP TABLE landgrid2.tx_block;

-- IF EXISTS (SELECT   *
-- 				FROM    sys.schemas
-- 				WHERE   name = N'landgrid2')
-- 	DROP SCHEMA landgrid2;
--
-- CREATE SCHEMA landgrid2
-- 	AUTHORIZATION dbo;

CREATE TABLE landgrid2.state_us
(
    StateId         INT IDENTITY		NOT NULL
        PRIMARY KEY,
    State_Name      VARCHAR(50)         NULL,
    Shape_Length    FLOAT               NULL,
    Shape_Area      FLOAT				NULL,
    geobounds       VARCHAR(1024)       NULL,
    shape           GEOMETRY			NULL,
	ErrorStatus		BIT					NULL
		DEFAULT (0)
);

CREATE TABLE landgrid2.county_us
(
    CountyKey      INT IDENTITY			NOT NULL
        PRIMARY KEY,
    County_Name    VARCHAR(50)          NULL,
    State_Name     VARCHAR(50)          NULL,
    CountyID       INT					NULL,
    StateID        INT					NULL,
    FIPS_State     CHAR(2)              NULL,
    FIPS_County    CHAR(3)              NULL,
    API_State      CHAR(2)              NULL,
    API_County     CHAR(3)              NULL,
    LAT            FLOAT                NULL,
    LON            FLOAT                NULL,
    Shape_Length   FLOAT                NULL,
    Shape_Area     FLOAT                NULL,
    geobounds      VARCHAR(1024)        NULL,
    shape          GEOMETRY				NULL,
	ErrorStatus		BIT					NULL
		DEFAULT (0)
);

CREATE TABLE landgrid2.plss_township
(
    TownshipID			INT IDENTITY    NOT NULL
        PRIMARY KEY,
    TWPCODE				VARCHAR(24)     NULL,
    MER					VARCHAR(5)      NULL,
    MST					VARCHAR(20)     NULL,
    TWP					INT				NULL,
    THALF				INT				NULL,
    TNS					CHAR(1)         NULL,
    RGE					INT				NULL,
    RHALF				INT				NULL,
    REW					CHAR(1)         NULL,
    SecCount			INT				NULL,
    TWPLabel			VARCHAR(20)     NULL,
    Shape_Length		FLOAT           NULL,
    Shape_Area			FLOAT           NULL,
    State_Name			VARCHAR(50)     NULL,
    State_Overlaps		VARCHAR(512)    NULL,
    County_Name			VARCHAR(50)     NULL,
    County_Overlaps		NVARCHAR(1024)  NULL,
    Township			VARCHAR(64)     NULL,
    Range				VARCHAR(64)     NULL,
    geobounds			VARCHAR(1024)   NULL,
    shape				GEOMETRY		NULL,
	ErrorStatus			BIT				NULL
		DEFAULT (0)
);

CREATE TABLE landgrid2.plss_section
(
    SectionID           INT IDENTITY    NOT NULL
        PRIMARY KEY,
    StateID             INT             NULL,
    StateAPI            CHAR(2)         NULL,
    TWPCODE             VARCHAR(24)     NULL,
    SECCODE             VARCHAR(20)     NULL,
    MER                 VARCHAR(5)      NULL,
    MST                 VARCHAR(20)     NULL,
    TWP                 INT             NULL,
    THALF               INT             NULL,
    TNS                 CHAR(1)         NULL,
    RGE                 INT             NULL,
    RHALF               INT             NULL,
    REW                 CHAR(1)         NULL,
    SEC                 INT             NULL,
    Shape_Length        FLOAT           NULL,
    Shape_Area          FLOAT           NULL,
    State_Name          VARCHAR(50)     NULL,
    State_Overlaps      VARCHAR(512)    NULL,
    County_Name         VARCHAR(50)     NULL,
    County_Overlaps     NVARCHAR(1024)  NULL,
    Township            VARCHAR(64)     NULL,
    Range               VARCHAR(64)     NULL,
    geobounds           VARCHAR(1024)   NULL,
    shape               GEOMETRY        NULL,
	ErrorStatus			BIT				NULL
		DEFAULT (0)
);

CREATE TABLE landgrid2.ohio_section_base
(
    SectionId			INT IDENTITY		NOT NULL
        PRIMARY KEY,
    SUBDIV_NM			VARCHAR(55)			NULL,
    TWP					INT					NULL,
    TNS					CHAR(1)				NULL,
    RGE					INT					NULL,
    REW					CHAR(1)				NULL,
    SEC					INT					NULL,
    QTR_TWP				CHAR(2)				NULL,
    ALLOTMENT			VARCHAR(55)			NULL,
    TRACT				VARCHAR(35)			NULL,
    LOT					VARCHAR(24)			NULL,
    DIVISION			VARCHAR(24)			NULL,
    FRACTION			INT					NULL,
    COUNTY				CHAR(11)			NULL,
    TOWNSHIP			VARCHAR(50)			NULL,
    SURVEY_TYP			VARCHAR(50)			NULL,
    ObjectID			INT					NULL,
    VMSLOT				VARCHAR(50)			NULL,
    OTHER_SUB			VARCHAR(65)			NULL,
    Shape_Length		FLOAT				NULL,
    Shape_Area			FLOAT				NULL,
    State_Name			VARCHAR(50)			NULL,
    State_Overlaps		VARCHAR(512)		NULL,
    County_Name			VARCHAR(50)			NULL,
    County_Overlaps		NVARCHAR(1024)		NULL,
    geobounds			VARCHAR(1024)		NULL,
    shape				GEOMETRY			NULL,
	ErrorStatus			BIT					NULL
		DEFAULT (0)
);

CREATE TABLE landgrid2.ohio_municipality
(
    MunicipalityId		INT IDENTITY		NOT NULL
        PRIMARY KEY,
    COUNTY				CHAR(11)			NULL,
    TOWNSHIP			VARCHAR(50)			NULL,
    State_Name			VARCHAR(50)			NULL,
    State_Overlaps		VARCHAR(512)		NULL,
    --County_Name       VARCHAR(50)                    NULL,
    County_Overlaps		NVARCHAR(1024)		NULL,
    geobounds			VARCHAR(1024)		NULL,
    shape				GEOMETRY			NULL,
	ErrorStatus			BIT					NULL
		DEFAULT (0)
);

CREATE TABLE landgrid2.ohio_township
(
    TownshipId			INT IDENTITY		NOT NULL
        PRIMARY KEY,
    COUNTY				CHAR(11)			NULL,
    TOWNSHIP			VARCHAR(50)			NULL,
    TWP					INT					NULL,
    TNS					CHAR(1)				NULL,
    RGE					INT					NULL,
    REW					CHAR(1)				NULL,
    State_Name			VARCHAR(50)			NULL,
    State_Overlaps		VARCHAR(512)		NULL,
    --County_Name       VARCHAR(50)                    NULL,
    County_Overlaps		NVARCHAR(1024)		NULL,
    geobounds			VARCHAR(1024)		NULL,
    shape				GEOMETRY			NULL,
	ErrorStatus			BIT					NULL
		DEFAULT (0)
);

CREATE TABLE landgrid2.ohio_section
(
    SectionId			INT IDENTITY		NOT NULL
        PRIMARY KEY,
    COUNTY				CHAR(11)			NULL,
    TOWNSHIP			VARCHAR(50)			NULL,
    TWP					INT					NULL,
    TNS					CHAR(1)				NULL,
    RGE					INT					NULL,
    REW					CHAR(1)				NULL,
    SEC					INT					NULL,
    State_Name			VARCHAR(50)			NULL,
    State_Overlaps		VARCHAR(512)		NULL,
    --County_Name       VARCHAR(50)                    NULL,
    County_Overlaps		NVARCHAR(1024)		NULL,
    geobounds			VARCHAR(1024)		NULL,
    shape				GEOMETRY			NULL,
	ErrorStatus			BIT					NULL
		DEFAULT (0)
);

CREATE TABLE landgrid2.pa_township
(
    TownshipId          INT IDENTITY    NOT NULL
        PRIMARY KEY,
    MSLINK              FLOAT           NULL,
    COUNTY              CHAR(2)         NULL,
    MUNICIPAL_          CHAR(3)         NULL,
    MUNICIPAL1          VARCHAR(20)     NULL,
    FIPS_MUN_C          VARCHAR(5)      NULL,
    FED_AID_UR          CHAR(1)         NULL,
    FIPS_COUNT          CHAR(3)         NULL,
    FIPS_AREA_          VARCHAR(5)      NULL,
    FIPS_NAME           VARCHAR(16)     NULL,
    FIPS_SQ_MI          FLOAT           NULL,
    FIPS_MUN_P          FLOAT           NULL,
    FED_ID_NUM          VARCHAR(10)     NULL,
    CLASS_OF_M          VARCHAR(4)      NULL,
    Shape_Length        FLOAT           NULL,
    Shape_Area          FLOAT           NULL,
    County_Name         VARCHAR(30)     NULL,
    County_TOWNSHIP     VARCHAR(40)     NULL,
    State_Name          VARCHAR(50)     NULL,
    State_Overlaps      VARCHAR(512)    NULL,
--    County_Name         VARCHAR(50)                 NULL,
    County_Overlaps     NVARCHAR(1024)  NULL,
    geobounds           VARCHAR(1024)   NULL,
    shape               GEOMETRY		NULL,
	ErrorStatus			BIT				NULL
		DEFAULT (0)
);

CREATE TABLE landgrid2.wv_district
(
    DistrictId          INT IDENTITY    NOT NULL
        PRIMARY KEY,
    WV_ID               INT             NULL,
    DNAME               VARCHAR(32)     NULL,
    DNUMBER             VARCHAR(32)     NULL,
    CNAME               VARCHAR(32)     NULL,
    CNUMBER             VARCHAR(32)     NULL,
    Area_sqm            FLOAT           NULL,
    lat                 FLOAT           NULL,
    long                FLOAT           NULL,
    Shape_Length        FLOAT           NULL,
    Shape_Area          FLOAT           NULL,
    County_District     VARCHAR(50)     NULL,
    State_Name          VARCHAR(50)     NULL,
    State_Overlaps      VARCHAR(512)    NULL,
    County_Name         VARCHAR(50)     NULL,
    County_Overlaps     NVARCHAR(1024)  NULL,
    geobounds           VARCHAR(1024)   NULL,
    shape               GEOMETRY		NULL,
	ErrorStatus			BIT				NULL
		DEFAULT (0)
);

CREATE TABLE landgrid2.tx_abstract
(
    AbstractId          INT IDENTITY    NOT NULL
        PRIMARY KEY,
    PERIMETER           FLOAT           NULL,
    FIPS                CHAR(3)         NULL,
    CountyName          VARCHAR(30)     NULL,
    Shape_Length        FLOAT           NULL,
    Shape_Area          FLOAT           NULL,
    AbstractNumber      VARCHAR(12)     NULL,
    AbstractName        VARCHAR(32)     NULL,
    Block               VARCHAR(10)     NULL,
    Township            VARCHAR(10)     NULL,
    Section             VARCHAR(8)      NULL,
    AbstractNameALT     VARCHAR(32)     NULL,
    FormNumber          VARCHAR(9)      NULL,
    ControlNumber       VARCHAR(9)      NULL,
    State_Name          VARCHAR(50)     NULL,
    State_Overlaps      VARCHAR(512)    NULL,
--    County_Name         VARCHAR(50)                 NULL,
    County_Overlaps     NVARCHAR(1024)  NULL,
    geobounds           VARCHAR(1024)   NULL,
    shape               GEOMETRY		NULL,
	ErrorStatus			BIT				NULL
		DEFAULT (0)
);

CREATE TABLE landgrid2.tx_block
(
    BlockId          INT IDENTITY       NOT NULL
        PRIMARY KEY,
    Block               VARCHAR(10)     NULL,
    Township            VARCHAR(10)     NULL,
    State_Name          VARCHAR(50)     NULL,
    State_Overlaps      VARCHAR(512)    NULL,
--    County_Name         VARCHAR(50)                 NULL,
    County_Overlaps     NVARCHAR(1024)  NULL,
    geobounds           VARCHAR(1024)   NULL,
    shape               GEOMETRY		NULL,
	ErrorStatus			BIT				NULL
		DEFAULT (0)
);