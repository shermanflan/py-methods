SELECT  '[LTC400BaseData]' AS [0]
        , p.[index]
        , p.[PharmacyCode],[Resident]  -- PatientKey
        , p.[FirstName]
        , p.[MiddleInitial]
        , p.[LastName]
        , p.[SexCode]
        , p.[FinPlan]
        , p.[PrivateInsurance2]
        , p.[Medicaidfinancial]
        , p.[Facility]
        , p.[Status]
        , p.[AdmitDate]                -- Grain
        , p.[DischargeDate]            -- Grain
        , p.[Birthdate]
        , p.[MedicareNbr]
        , p.[MedicaidNbr]
        , p.[Address1]
        , p.[Address2]
        , p.[City]
        , p.[State]
        , p.[ZipCode]
        , p.[ZipCodePlus4]
		, z.Latitude
		, z.Longitude
        , p.[HomePhone]
        , p.[WorkPhone]
        , p.[EMailID]
        , p.[FacilityName]
        , p.[FacilityAddress1]
        , p.[FacilityAddress2]
        , p.[FacilityCity]
        , p.[FacilityState]
        , p.[FacilityZip]
        , p.[FacilityPhone]
        , p.[ICD10CODE]                -- Grain
FROM    [Staging].[LTC400BaseData] AS p WITH (READUNCOMMITTED)
	LEFT JOIN [MasterData].[ZipCode] AS z WITH (READUNCOMMITTED)
		ON p.[ZipCode] = z.ZipCode
WHERE	z.Id IS NOT NULL
ORDER BY [PharmacyCode], [Resident];

SELECT  TOP (1000) 
        '[LTC400Crosswalk]' AS [1]
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
FROM    [Staging].[LTC400Crosswalk] WITH (READUNCOMMITTED)
WHERE	[PatientKey] = '000200FJO'
ORDER BY [PatientKey];

SELECT  TOP (1000) 
        '[LTC400PatientScore]' AS [2]
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
FROM    [Staging].[LTC400PatientScore] WITH (READUNCOMMITTED)
WHERE	[PatientKey] = '000200FJO'
ORDER BY [PatientKey];