CREATE TABLE IF NOT EXISTS nyc_trees (
    tree_id INTEGER PRIMARY KEY,
    block_id INTEGER,
    created_at TIMESTAMP,
    tree_dbh INTEGER,
    stump_diam INTEGER,
    curb_loc VARCHAR(50),
    status VARCHAR(20),
    health VARCHAR(20),
    spc_latin VARCHAR(255),
    spc_common VARCHAR(255),
    steward VARCHAR(50),
    guards VARCHAR(50),
    sidewalk VARCHAR(50),
    user_type VARCHAR(50),
    problems TEXT,
    root_stone VARCHAR(10),
    root_grate VARCHAR(10),
    root_other VARCHAR(10),
    trunk_wire VARCHAR(10),
    trnk_light VARCHAR(10),
    trnk_other VARCHAR(10),
    brch_light VARCHAR(10),
    brch_shoe VARCHAR(10),
    brch_other VARCHAR(10),
    address VARCHAR(255),
    postcode INTEGER,
    zip_city VARCHAR(50),
    community_board INTEGER,
    borocode INTEGER,
    borough VARCHAR(50),
    cncldist INTEGER,
    st_assem INTEGER,
    st_senate INTEGER,
    nta VARCHAR(50),
    nta_name VARCHAR(255),
    boro_ct INTEGER,
    state VARCHAR(50),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    x_sp DOUBLE PRECISION,
    y_sp DOUBLE PRECISION,
    council_district INTEGER,
    census_tract INTEGER,
    bin BIGINT,
    bbl BIGINT
);

-- Indexes for optimization
CREATE INDEX IF NOT EXISTS idx_spc_common ON nyc_trees(spc_common);
CREATE INDEX IF NOT EXISTS idx_borough ON nyc_trees(borough);
CREATE INDEX IF NOT EXISTS idx_created_at ON nyc_trees(created_at);
