USE master;
GO

SELECT @@VERSION;
GO

IF NOT EXISTS (SELECT * FROM sys.databases
                WHERE name = N'ScratchDB')
    CREATE DATABASE ScratchDB;
GO

USE ScratchDB;
GO

-- CDC
EXEC sys.sp_cdc_enable_db
GO

IF OBJECT_ID(N'dbo.DirectionalSurvey', N'U') IS NOT NULL
    DROP TABLE dbo.DirectionalSurvey;
GO

CREATE TABLE dbo.DirectionalSurvey
(
    ID          INT         NOT NULL
        PRIMARY KEY,
    API         VARCHAR(32) NULL,
    WKID        VARCHAR(32) NULL,
    FIPS        VARCHAR(4)  NULL,
    STATUS_CODE VARCHAR(1)  NOT NULL  
);
GO

-- CDC
EXEC sys.sp_cdc_enable_table
    @source_schema = N'dbo',
    @source_name   = N'DirectionalSurvey',
    @role_name     = NULL,
    --@filegroup_name = N'MyDB_CT',
    @capture_instance = 'dbo_DirectionalSurvey_v1',
    @supports_net_changes = 1
GO

IF OBJECT_ID(N'dbo.SurveyReport', N'U') IS NOT NULL
    DROP TABLE dbo.SurveyReport;
GO

CREATE TABLE dbo.SurveyReport
(
    ID      INT         NOT             NULL
        PRIMARY KEY,
    DirectionalSurveyId INT             NOT NULL
        FOREIGN KEY REFERENCES dbo.DirectionalSurvey (ID),
    Azimuth             FLOAT           NULL,
    MD                  FLOAT           NULL,
    Inclination         FLOAT           NULL,
    STATUS_CODE         VARCHAR(1)      NOT NULL
);
GO

-- CDC
EXEC sys.sp_cdc_enable_table
    @source_schema = N'dbo',
    @source_name   = N'SurveyReport',
    @role_name     = NULL,
    --@filegroup_name = N'MyDB_CT',
    @capture_instance = 'dbo_SurveyReport_v1',
    @supports_net_changes = 1
GO

IF OBJECT_ID(N'dbo.Well', N'U') IS NOT NULL
    DROP TABLE dbo.Well;
GO

CREATE TABLE dbo.Well
(
    ID          INT             NOT NULL
        PRIMARY KEY,
    API         VARCHAR(32)     NULL,
    LATITUDE    DECIMAL(12, 2)  NULL,
    LONGITUDE   DECIMAL(12, 2)  NULL
);
GO

INSERT INTO dbo.Well
VALUES (1, 'API1', 1.10, 1.10), (2, 'API2', 2.20, 2.20)
        , (3, 'API4', 4.40, 4.40);
GO

INSERT INTO dbo.DirectionalSurvey
VALUES (1, 'API1', 'WKID1', '0001', 'N'), (2, 'API2', 'WKID2', '0002', 'N')
        , (3, 'API3', 'WKID3', '0003', 'N');
GO

INSERT INTO dbo.SurveyReport
VALUES (1, 1, 1.0, 2.0, 3.0, 'N')
        , (2, 1, 4.0, 5.0, 6.0, 'N')
        , (3, 2, 7.0, 8.0, 9.0, 'N')
        , (4, 2, 1.0, 2.0, 3.0, 'N')
        , (5, 3, 4.0, 5.0, 6.0, 'N')
        , (6, 3, 7.0, 8.0, 9.0, 'N');
GO
