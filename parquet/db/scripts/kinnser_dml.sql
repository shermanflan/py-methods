SELECT  TOP (100)
        '[KinnserBIBaseData]' AS [0]
        , p.[index]
        , p.[PatientKey]       -- grain
        , p.[LastName]
        , p.[FirstName]
        , p.[MiddleInitial]
        , p.[ResidenceType]
        , p.[MedicalRecordNum]
        , p.[MedicaidNum]
        , p.[DateofBirth]
        , p.[Gender]
        , p.[Address]
        , p.[City]
        , p.[County]
        , p.[State]
        , p.[ZipCode]
		, z.Latitude
		, z.Longitude
        , p.[Phone]
        , p.[AdmissionKey]     -- grain
        , p.[AdmissionDate]
        , p.[DischargeDate]
        , p.[AdmissionYear]
        , p.[DischargeYear]
        , p.[EpisodeKey]       -- grain
        , p.[InsuranceName]
        , p.[InsuranceType]
        , p.[InsuranceKey]
        , p.[EpisodeStartDate]
        , p.[EpisodeEndDate]
        , p.[ICD10PrimaryDiagnosisCode]
        , p.[ICD10PrimaryDiagnosisDescription]
        , p.[ICD10SecondaryDiagnosisCode]
        , p.[ICD10SecondaryDiagnosisDescription]
        , p.[ICD10PrimaryDiagnosis]
        , p.[ICD10SecondaryDiagnosis]
        , p.[ICDVersion]
        , p.[PrimaryDx]
        , p.[SecondaryDx_A]
        , p.[SecondaryDx_B]
        , p.[SecondaryDx_C]
        , p.[SecondaryDx_D]
        , p.[SecondaryDx_E]
        , p.[SecondaryDx_F]
        , p.[SecondaryDx_G]
        , p.[SecondaryDx_H]
        , p.[SecondaryDx_I]
        , p.[SecondaryDx_J]
        , p.[SecondaryDx_K]
        , p.[SecondaryDx_L]
        , p.[SecondaryDx_M]
        , p.[SecondaryDx_N]
        , p.[SecondaryDx_O]
        , p.[SecondaryDx_P]
        , p.[SecondaryDx_Q]
        , p.[ClinicKey]
        , p.[BranchKey]
        , p.[CorporationKey]
        , p.[CorporationName]
        , p.[ClinicName]
        , p.[ClinicShortName]
        , p.[BranchName]
        , p.[BranchShortName]
        , p.[ClinicAddress]
        , p.[ClinicCity]
        , p.[ClinicState]
        , p.[ClinicalGroup]
FROM    [Staging].[KinnserBIBaseData] AS p WITH (READUNCOMMITTED)
	LEFT JOIN [MasterData].[ZipCode] AS z WITH (READUNCOMMITTED)
		ON p.[ZipCode] = z.ZipCode
WHERE	p.[AdmissionYear] > 2000
		AND z.Id IS NULL
ORDER BY [PatientKey];

SELECT  TOP (100) 
        '[KinnserCrosswalk]' AS [1]
        ,[index]
        ,[PatientKey]
        ,[icd10_level]
        ,[ICD10CODE]
        ,[ICD10CODE_LEN]
        ,[ICD_3Char]
        ,[ICD_4Char]
        ,[ICD_5Char]
        ,[row_id]
        ,[cc_category]
FROM    [Staging].[KinnserCrosswalk] WITH (READUNCOMMITTED)
ORDER BY [PatientKey];

SELECT  TOP (100) 
        '[KinnserPatientScore]' AS [2]
        ,[level_0]
        ,[index]
        ,[PatientKey]
        ,[hcc_ce]
        ,[hcc_ins]
        ,[hcc_ne]
        ,[hcc_cc_ce]
        ,[hcupModelScore]
        ,[lr_cc]
        ,[rf_cc]
        ,[num_cc]
        ,[cc_readmission]
        ,[patient_risk_score]
        ,[patient_risk_score_scale]
        ,[RiskStratify]
FROM    [Staging].[KinnserPatientScore] WITH (READUNCOMMITTED)
ORDER BY [PatientKey];