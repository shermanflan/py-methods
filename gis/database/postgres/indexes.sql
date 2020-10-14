
CREATE INDEX /*CONCURRENTLY*/ state_us_grid_polys_gix
	ON landgrid.state_us_grid
USING GIST (shape);

CREATE INDEX county_us_grid_polys_gix
	ON landgrid.county_us_grid
USING GIST (shape);

CREATE INDEX plss_township_polys_gix
    ON landgrid.plss_township
USING GIST (shape);

CREATE INDEX plss_section_polys_gix
    ON landgrid.plss_section
USING GIST (shape);

CREATE INDEX ohio_municipality_polys_gix
    ON landgrid.ohio_municipality
USING GIST (shape);

CREATE INDEX ohio_township_polys_gix
    ON landgrid.ohio_township
USING GIST (shape);

CREATE INDEX ohio_section_polys_gix
    ON landgrid.ohio_section
USING GIST (shape);

CREATE INDEX pa_township_polys_gix
    ON landgrid.pa_township
USING GIST (shape);

CREATE INDEX wv_district_polys_gix
    ON landgrid.wv_district
USING GIST (shape);

CREATE INDEX tx_abstract_polys_gix
    ON landgrid.tx_abstract
USING GIST (shape);

CREATE INDEX tx_block_polys_gix
    ON landgrid.tx_block
USING GIST (shape);
