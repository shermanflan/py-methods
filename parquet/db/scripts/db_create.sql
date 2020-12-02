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

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[KinnserBIBaseData](
	[index] [bigint] NULL,
	[PatientKey] [bigint] NULL,
	[LastName] [varchar](max) NULL,
	[FirstName] [varchar](max) NULL,
	[MiddleInitial] [varchar](max) NULL,
	[ResidenceType] [varchar](max) NULL,
	[MedicalRecordNum] [varchar](max) NULL,
	[MedicaidNum] [varchar](max) NULL,
	[DateofBirth] [datetime] NULL,
	[Gender] [varchar](max) NULL,
	[Address] [varchar](max) NULL,
	[City] [varchar](max) NULL,
	[County] [varchar](max) NULL,
	[State] [varchar](max) NULL,
	[ZipCode] [varchar](max) NULL,
	[Phone] [varchar](max) NULL,
	[AdmissionKey] [float] NULL,
	[AdmissionDate] [datetime] NULL,
	[DischargeDate] [varchar](max) NULL,
	[AdmissionYear] [float] NULL,
	[DischargeYear] [float] NULL,
	[EpisodeKey] [float] NULL,
	[InsuranceName] [varchar](max) NULL,
	[InsuranceType] [varchar](max) NULL,
	[InsuranceKey] [float] NULL,
	[EpisodeStartDate] [datetime] NULL,
	[EpisodeEndDate] [datetime] NULL,
	[ICD10PrimaryDiagnosisCode] [varchar](max) NULL,
	[ICD10PrimaryDiagnosisDescription] [varchar](max) NULL,
	[ICD10SecondaryDiagnosisCode] [varchar](max) NULL,
	[ICD10SecondaryDiagnosisDescription] [varchar](max) NULL,
	[ICD10PrimaryDiagnosis] [varchar](max) NULL,
	[ICD10SecondaryDiagnosis] [varchar](max) NULL,
	[ICDVersion] [varchar](max) NULL,
	[PrimaryDx] [varchar](max) NULL,
	[SecondaryDx_A] [varchar](max) NULL,
	[SecondaryDx_B] [varchar](max) NULL,
	[SecondaryDx_C] [varchar](max) NULL,
	[SecondaryDx_D] [varchar](max) NULL,
	[SecondaryDx_E] [varchar](max) NULL,
	[SecondaryDx_F] [varchar](max) NULL,
	[SecondaryDx_G] [varchar](max) NULL,
	[SecondaryDx_H] [varchar](max) NULL,
	[SecondaryDx_I] [varchar](max) NULL,
	[SecondaryDx_J] [varchar](max) NULL,
	[SecondaryDx_K] [varchar](max) NULL,
	[SecondaryDx_L] [varchar](max) NULL,
	[SecondaryDx_M] [varchar](max) NULL,
	[SecondaryDx_N] [varchar](max) NULL,
	[SecondaryDx_O] [varchar](max) NULL,
	[SecondaryDx_P] [varchar](max) NULL,
	[SecondaryDx_Q] [varchar](max) NULL,
	[ClinicKey] [float] NULL,
	[BranchKey] [float] NULL,
	[CorporationKey] [float] NULL,
	[CorporationName] [varchar](max) NULL,
	[ClinicName] [varchar](max) NULL,
	[ClinicShortName] [varchar](max) NULL,
	[BranchName] [varchar](max) NULL,
	[BranchShortName] [varchar](max) NULL,
	[ClinicAddress] [varchar](max) NULL,
	[ClinicCity] [varchar](max) NULL,
	[ClinicState] [varchar](max) NULL,
	[ClinicalGroup] [varchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [ix_dbo_KinnserBIBaseData_index] ON [dbo].[KinnserBIBaseData]
(
	[index] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[KinnserCrosswalk](
	[index] [bigint] NULL,
	[PatientKey] [bigint] NULL,
	[icd10_level] [varchar](max) NULL,
	[ICD10CODE] [varchar](max) NULL,
	[ICD10CODE_LEN] [bigint] NULL,
	[ICD_3Char] [varchar](max) NULL,
	[ICD_4Char] [varchar](max) NULL,
	[ICD_5Char] [varchar](max) NULL,
	[row_id] [bigint] NULL,
	[cc_category] [varchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [ix_dbo_KinnserCrosswalk_index] ON [dbo].[KinnserCrosswalk]
(
	[index] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[KinnserPatientScore](
	[level_0] [bigint] NULL,
	[index] [bigint] NULL,
	[PatientKey] [bigint] NULL,
	[hcc_ce] [float] NULL,
	[hcc_ins] [float] NULL,
	[hcc_ne] [float] NULL,
	[hcc_cc_ce] [float] NULL,
	[hcupModelScore] [float] NULL,
	[lr_cc] [float] NULL,
	[rf_cc] [float] NULL,
	[num_cc] [float] NULL,
	[cc_readmission] [float] NULL,
	[patient_risk_score] [float] NULL,
	[patient_risk_score_scale] [float] NULL,
	[RiskStratify] [varchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [ix_dbo_KinnserPatientScore_level_0] ON [dbo].[KinnserPatientScore]
(
	[level_0] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[LTC400BaseData](
	[index] [bigint] NULL,
	[PharmacyCode] [varchar](max) NULL,
	[Resident] [varchar](max) NULL,
	[FirstName] [varchar](max) NULL,
	[MiddleInitial] [varchar](max) NULL,
	[LastName] [varchar](max) NULL,
	[SexCode] [varchar](max) NULL,
	[FinPlan] [varchar](max) NULL,
	[PrivateInsurance2] [varchar](max) NULL,
	[Medicaidfinancial] [varchar](max) NULL,
	[Facility] [varchar](max) NULL,
	[Status] [varchar](max) NULL,
	[AdmitDate] [float] NULL,
	[DischargeDate] [float] NULL,
	[Birthdate] [float] NULL,
	[MedicareNbr] [varchar](max) NULL,
	[MedicaidNbr] [varchar](max) NULL,
	[Address1] [varchar](max) NULL,
	[Address2] [varchar](max) NULL,
	[City] [varchar](max) NULL,
	[State] [varchar](max) NULL,
	[ZipCode] [varchar](max) NULL,
	[ZipCodePlus4] [varchar](max) NULL,
	[HomePhone] [float] NULL,
	[WorkPhone] [float] NULL,
	[EMailID] [varchar](max) NULL,
	[FacilityName] [varchar](max) NULL,
	[FacilityAddress1] [varchar](max) NULL,
	[FacilityAddress2] [varchar](max) NULL,
	[FacilityCity] [varchar](max) NULL,
	[FacilityState] [varchar](max) NULL,
	[FacilityZip] [varchar](max) NULL,
	[FacilityPhone] [float] NULL,
	[ICD10CODE] [varchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [ix_dbo_LTC400BaseData_index] ON [dbo].[LTC400BaseData]
(
	[index] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[LTC400Crosswalk](
	[index] [bigint] NULL,
	[PatientKey] [varchar](max) NULL,
	[icd10_level] [varchar](max) NULL,
	[ICD10CODE] [varchar](max) NULL,
	[ICD10CODE_LEN] [bigint] NULL,
	[ICD_3Char] [varchar](max) NULL,
	[ICD_4Char] [varchar](max) NULL,
	[ICD_5Char] [varchar](max) NULL,
	[row_id] [bigint] NULL,
	[cc_category] [varchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [ix_dbo_LTC400Crosswalk_index] ON [dbo].[LTC400Crosswalk]
(
	[index] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[LTC400PatientScore](
	[level_0] [bigint] NULL,
	[index] [bigint] NULL,
	[PatientKey] [varchar](max) NULL,
	[hcc_ce] [float] NULL,
	[hcc_ins] [float] NULL,
	[hcc_ne] [float] NULL,
	[hcc_cc_ce] [float] NULL,
	[hcupModelScore] [float] NULL,
	[lr_cc] [float] NULL,
	[rf_cc] [float] NULL,
	[num_cc] [float] NULL,
	[cc_readmission] [float] NULL,
	[patient_risk_score] [float] NULL,
	[patient_risk_score_scale] [float] NULL,
	[RiskStratify] [varchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [ix_dbo_LTC400PatientScore_level_0] ON [dbo].[LTC400PatientScore]
(
	[level_0] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
