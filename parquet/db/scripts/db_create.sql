USE master;
GO

IF NOT EXISTS (
    SELECT  *
    FROM    sys.databases
    WHERE   name = N'ScratchDB')
BEGIN
    CREATE DATABASE ScratchDB;
END
GO

USE ScratchDB;
GO