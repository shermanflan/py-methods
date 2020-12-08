/*
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
*/
USE MasterData_BSHFinancials;
GO

DROP TABLE IF EXISTS [Staging].[KinnserBIBaseData];
DROP TABLE IF EXISTS [Staging].[KinnserCrosswalk];
DROP TABLE IF EXISTS [Staging].[KinnserPatientScore];
DROP TABLE IF EXISTS [Staging].[LTC400BaseData];
DROP TABLE IF EXISTS [Staging].[LTC400Crosswalk];
DROP TABLE IF EXISTS [Staging].[LTC400PatientScore];

CREATE TABLE [Staging].[KinnserBIBaseData]
(
	Id										INT IDENTITY(1, 1)		NOT NULL
		PRIMARY KEY
	, [index]								[bigint]				NULL
	, [PatientKey]							[bigint]				NULL
	, [LastName]							[varchar](max)			NULL
	, [FirstName]							[varchar](max)			NULL
	, [MiddleInitial]						[varchar](max)			NULL
	, [ResidenceType]						[varchar](max)			NULL
	, [MedicalRecordNum]					[varchar](max)			NULL
	, [MedicaidNum]							[varchar](max)			NULL
	, [DateofBirth]							[datetime]				NULL
	, [Gender]								[varchar](max)			NULL
	, [Address]								[varchar](max)			NULL
	, [City]								[varchar](max)			NULL
	, [County]								[varchar](max)			NULL
	, [State]								[varchar](max)			NULL
	, [ZipCode]								[varchar](max)			NULL
	, [Phone]								[varchar](max)			NULL
	, [AdmissionKey]						INT						NULL
	, [AdmissionDate]						[datetime]				NULL
	, [DischargeDate]						[varchar](max)			NULL
	, [AdmissionYear]						INT						NULL
	, [DischargeYear]						INT						NULL
	, [EpisodeKey]							INT						NULL
	, [InsuranceName]						[varchar](max)			NULL
	, [InsuranceType]						[varchar](max)			NULL
	, [InsuranceKey]						INT						NULL
	, [EpisodeStartDate]					[datetime]				NULL
	, [EpisodeEndDate]						[datetime]				NULL
	, [ICD10PrimaryDiagnosisCode]			[varchar](max)			NULL
	, [ICD10PrimaryDiagnosisDescription]	[varchar](max)			NULL
	, [ICD10SecondaryDiagnosisCode]			[varchar](max)			NULL
	, [ICD10SecondaryDiagnosisDescription]	[varchar](max)			NULL
	, [ICD10PrimaryDiagnosis]				[varchar](max)			NULL
	, [ICD10SecondaryDiagnosis]				[varchar](max)			NULL
	, [ICDVersion]							[varchar](max)			NULL
	, [PrimaryDx]							[varchar](max)			NULL
	, [SecondaryDx_A]						[varchar](max)			NULL
	, [SecondaryDx_B]						[varchar](max)			NULL
	, [SecondaryDx_C]						[varchar](max)			NULL
	, [SecondaryDx_D]						[varchar](max)			NULL
	, [SecondaryDx_E]						[varchar](max)			NULL
	, [SecondaryDx_F]						[varchar](max)			NULL
	, [SecondaryDx_G]						[varchar](max)			NULL
	, [SecondaryDx_H]						[varchar](max)			NULL
	, [SecondaryDx_I]						[varchar](max)			NULL
	, [SecondaryDx_J]						[varchar](max)			NULL
	, [SecondaryDx_K]						[varchar](max)			NULL
	, [SecondaryDx_L]						[varchar](max)			NULL
	, [SecondaryDx_M]						[varchar](max)			NULL
	, [SecondaryDx_N]						[varchar](max)			NULL
	, [SecondaryDx_O]						[varchar](max)			NULL
	, [SecondaryDx_P]						[varchar](max)			NULL
	, [SecondaryDx_Q]						[varchar](max)			NULL
	, [ClinicKey]							INT						NULL
	, [BranchKey]							INT						NULL
	, [CorporationKey]						INT						NULL
	, [CorporationName]						[varchar](max)			NULL
	, [ClinicName]							[varchar](max)			NULL
	, [ClinicShortName]						[varchar](max)			NULL
	, [BranchName]							[varchar](max)			NULL
	, [BranchShortName]						[varchar](max)			NULL
	, [ClinicAddress]						[varchar](max)			NULL
	, [ClinicCity]							[varchar](max)			NULL
	, [ClinicState]							[varchar](max)			NULL
	, [ClinicalGroup]						[varchar](max)			NULL
)
;

CREATE TABLE [Staging].[KinnserCrosswalk]
(
	Id					INT IDENTITY(1, 1)		NOT NULL
		PRIMARY KEY
	, [index]			[bigint]				NULL
	, [PatientKey]		[bigint]				NULL
	, [icd10_level]		[varchar](max)			NULL
	, [ICD10CODE]		[varchar](max)			NULL
	, [ICD10CODE_LEN]	[bigint]				NULL
	, [ICD_3Char]		[varchar](max)			NULL
	, [ICD_4Char]		[varchar](max)			NULL
	, [ICD_5Char]		[varchar](max)			NULL
	, [row_id]			[bigint]				NULL
	, [cc_category]		[varchar](max)			NULL
)
;

CREATE TABLE [Staging].[KinnserPatientScore]
(
	Id								INT IDENTITY(1, 1)		NOT NULL
		PRIMARY KEY
	, [level_0]						[bigint]				NULL
	, [index]						[bigint]				NULL
	, [PatientKey]					[bigint]				NULL
	, [hcc_ce]						[float]					NULL
	, [hcc_ins]						[float]					NULL
	, [hcc_ne]						[float]					NULL
	, [hcc_cc_ce]					[float]					NULL
	, [hcupModelScore]				[float]					NULL
	, [lr_cc]						[float]					NULL
	, [rf_cc]						[float]					NULL
	, [num_cc]						INT						NULL
	, [cc_readmission]				[float]					NULL
	, [patient_risk_score]			[float]					NULL
	, [patient_risk_score_scale]	[float]					NULL
	, [RiskStratify]				[varchar](max)			NULL
)
;

CREATE TABLE [Staging].[LTC400BaseData]
(
	Id						INT IDENTITY(1, 1)	NOT NULL
		PRIMARY KEY
	, [index]				[bigint]			NULL
	, [PharmacyCode]		[varchar](max)		NULL
	, [Resident]			[varchar](max)		NULL
	, [FirstName]			[varchar](max)		NULL
	, [MiddleInitial]		[varchar](max)		NULL
	, [LastName]			[varchar](max)		NULL
	, [SexCode]				[varchar](max)		NULL
	, [FinPlan]				[varchar](max)		NULL
	, [PrivateInsurance2]	[varchar](max)		NULL
	, [Medicaidfinancial]	[varchar](max)		NULL
	, [Facility]			[varchar](max)		NULL
	, [Status]				[varchar](max)		NULL
	, [AdmitDate]			INT					NULL
	, [DischargeDate]		INT					NULL
	, [Birthdate]			INT					NULL
	, [MedicareNbr]			[varchar](max)		NULL
	, [MedicaidNbr]			[varchar](max)		NULL
	, [Address1]			[varchar](max)		NULL
	, [Address2]			[varchar](max)		NULL
	, [City]				[varchar](max)		NULL
	, [State]				[varchar](max)		NULL
	, [ZipCode]				[varchar](max)		NULL
	, [ZipCodePlus4]		[varchar](max)		NULL
	, [HomePhone]			BIGINT				NULL
	, [WorkPhone]			BIGINT				NULL
	, [EMailID]				[varchar](max)		NULL
	, [FacilityName]		[varchar](max)		NULL
	, [FacilityAddress1]	[varchar](max)		NULL
	, [FacilityAddress2]	[varchar](max)		NULL
	, [FacilityCity]		[varchar](max)		NULL
	, [FacilityState]		[varchar](max)		NULL
	, [FacilityZip]			[varchar](max)		NULL
	, [FacilityPhone]		BIGINT				NULL
	, [ICD10CODE]			[varchar](max)		NULL
)
;

CREATE TABLE [Staging].[LTC400Crosswalk]
(
	Id					INT IDENTITY(1, 1)	NOT NULL
		PRIMARY KEY
	, [index]			[bigint]			NULL
	, [PatientKey]		[varchar](max)		NULL
	, [icd10_level]		[varchar](max)		NULL
	, [ICD10CODE]		[varchar](max)		NULL
	, [ICD10CODE_LEN]	[bigint]			NULL
	, [ICD_3Char]		[varchar](max)		NULL
	, [ICD_4Char]		[varchar](max)		NULL
	, [ICD_5Char]		[varchar](max)		NULL
	, [row_id]			[bigint]			NULL
	, [cc_category]		[varchar](max)		NULL
)
;

CREATE TABLE [Staging].[LTC400PatientScore]
(
	Id								INT IDENTITY(1, 1)	NOT NULL
		PRIMARY KEY
	, [level_0]						[bigint]			NULL
	, [index]						[bigint]			NULL
	, [PatientKey]					[varchar](max)		NULL
	, [hcc_ce]						[float]				NULL
	, [hcc_ins]						[float]				NULL
	, [hcc_ne]						[float]				NULL
	, [hcc_cc_ce]					[float]				NULL
	, [hcupModelScore]				[float]				NULL
	, [lr_cc]						[float]				NULL
	, [rf_cc]						[float]				NULL
	, [num_cc]						INT					NULL
	, [cc_readmission]				[float]				NULL
	, [patient_risk_score]			[float]				NULL
	, [patient_risk_score_scale]	[float]				NULL
	, [RiskStratify]				[varchar](max)		NULL
)
;