
UPDATE [landgrid2].[plss_township]
	SET [ErrorStatus] = 1
WHERE	-- NULL
		(
			[MER] IS NULL
			OR [MST] IS NULL
			OR [TWPLabel] IS NULL
			OR [TWP] IS NULL
			OR [TWPCODE] IS NULL
			OR [THALF] IS NULL
			OR [TNS] IS NULL
			OR [RGE] IS NULL
			OR [RHALF] IS NULL
			OR [REW] IS NULL
			OR [State_Overlaps] IS NULL
			OR [County_Overlaps] IS NULL
			OR [geobounds] IS NULL
		)
		-- Type
		--OR (
		--	ISNUMERIC([RHALF]) = 0
		--	OR ISNUMERIC([RGE]) = 0
		--	OR ISNUMERIC([THALF]) = 0
		--	OR ISNUMERIC([TWP]) = 0
		--)
		-- Values
		OR (
			[MER] NOT IN ('1', '2', '3', '4', '5', '6', '7', '8', 
						'9', '10','11','14', '15', '16', '17', '18',
						'19', '20', '21', '23', '24', '25', '26', 
						'27', '29', '30', '31', '32', '33', '34', 
						'35', '36', '39', '40', '46', '47', '48', 
						'91', '209')
			OR [MST] NOT IN ('2nd Principal', '3rd Principal',
							'5th Principal', '6th Principal',
							'Black Hills 1878', 'Boise 1867',
							'Chickasaw 1833', 'Choctaw 1821',
							'Cimarron 1881', 'Gila and Salt River',
							'Humbolt 1853', 'Huntsville 1807',
							'Indian 1870', 'Louisiana', 'Michigan',
							'Montana Principal', 'Mount Diablo',
							'New Mexico', 'Salt Lake', 'San Bernardino',
							'Sisselton IR', 'St. Helena', 'St. Stephens',
							'Tallahassee', 'Uintah Special', 'Ute', 
							'Washington', 'Willamette', 'Wind River'
			)
			OR NOT [TWP] BETWEEN 1 AND 200
			OR NOT [THALF] IN (0, 50)
			OR NOT [TNS] IN ('N', 'S')
			OR NOT [RGE] BETWEEN 1 AND 200
			OR NOT [RHALF] IN (0, 50)
			OR NOT [REW] IN ('W', 'E')
		);


UPDATE [landgrid2].[plss_section]
	SET [ErrorStatus] = 1
WHERE	-- NULL
		(
			[MER] IS NULL
			OR [MST] IS NULL
			OR [TWP] IS NULL
			OR [TWPCODE] IS NULL
			OR [THALF] IS NULL
			OR [TNS] IS NULL
			OR [RGE] IS NULL
			OR [RHALF] IS NULL
			OR [REW] IS NULL
			OR [SEC] IS NULL
			OR [SECCODE] IS NULL
			OR [State_Overlaps] IS NULL
			OR [County_Overlaps] IS NULL
			OR [geobounds] IS NULL
		)
		-- Type
		--OR (
		--	ISNUMERIC([RHALF]) = 0
		--	OR ISNUMERIC([RGE]) = 0
		--	OR ISNUMERIC([THALF]) = 0
		--	OR ISNUMERIC([TWP]) = 0
		--	OR ISNUMERIC([SEC]) = 0
		--)
		-- Values
		OR (
			[MER] NOT IN ('1', '2', '3', '4', '5', '6', '7', '8',
						'09', '9', '10','11','14', '15', '16', '17',
						'18', '19', '20', '21', '23', '24', '25', '26',
						'27', '29', '30', '31', '32', '33', '34',
						'35', '36', '39', '40', '46', '47', '48',
						'91', '209')
			OR [MST] NOT IN ('2nd Principal', '3rd Principal',
							'5th Principal', '6th Principal',
							'Black Hills 1878', 'Boise 1867',
							'Chickasaw 1833', 'Choctaw 1821',
							'Cimarron 1881', 'Gila and Salt River',
							'Humbolt 1853', 'Huntsville 1807',
							'Indian 1870', 'Louisiana', 'Michigan',
							'Montana Principal', 'Mount Diablo',
							'New Mexico', 'Salt Lake', 'San Bernardino',
							'Sisselton IR', 'St. Helena', 'St. Stephens',
							'Tallahassee', 'Uintah Special', 'Ute', 
							'Washington', 'Willamette', 'Wind River'
			)
			OR NOT [TWP] BETWEEN 1 AND 200
			OR NOT [THALF] IN (0, 50)
			OR NOT [TNS] IN ('N', 'S')
			OR NOT [RGE] BETWEEN 1 AND 200
			OR NOT [RHALF] IN (0, 50)
			OR NOT [REW] IN ('W', 'E')
			OR NOT [SEC] BETWEEN 1 AND 99
		);

UPDATE [landgrid2].[tx_abstract]
	SET [ErrorStatus] = 1
WHERE	-- NULL
		(
			[State_Overlaps] IS NULL
			OR [County_Overlaps] IS NULL
			OR [geobounds] IS NULL
		);

UPDATE [landgrid2].[tx_block]
	SET [ErrorStatus] = 1
WHERE	-- NULL
		(
			[State_Overlaps] IS NULL
			OR [County_Overlaps] IS NULL
			OR [geobounds] IS NULL
		);

UPDATE [landgrid2].[wv_district]
	SET [ErrorStatus] = 1
WHERE	-- NULL
		(
			[State_Overlaps] IS NULL
			OR [County_Overlaps] IS NULL
			OR [geobounds] IS NULL
		);

UPDATE [landgrid2].[pa_township]
	SET [ErrorStatus] = 1
WHERE	-- NULL
		(
			[State_Overlaps] IS NULL
			OR [County_Overlaps] IS NULL
			OR [geobounds] IS NULL
		);

UPDATE [landgrid2].[ohio_municipality]
	SET [ErrorStatus] = 1
WHERE	-- NULL
		(
			[State_Overlaps] IS NULL
			OR [County_Overlaps] IS NULL
			OR [geobounds] IS NULL
		);

UPDATE [landgrid2].[ohio_township]
	SET [ErrorStatus] = 1
WHERE	-- NULL
		(
			[State_Overlaps] IS NULL
			OR [County_Overlaps] IS NULL
			OR [geobounds] IS NULL
		);

UPDATE [landgrid2].[ohio_section]
	SET [ErrorStatus] = 1
WHERE	-- NULL
		(
			[State_Overlaps] IS NULL
			OR [County_Overlaps] IS NULL
			OR [geobounds] IS NULL
		);
