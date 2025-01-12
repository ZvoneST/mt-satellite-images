DROP TABLE landing.paths_to_dem CASCADE;

CREATE TABLE landing.paths_to_dem
(
    paths_to_dem_id SERIAL PRIMARY KEY,
    field_id INT NOT NULL,
    satellite_image_path VARCHAR(255) NOT NULL,
    response_meta_path VARCHAR(255) NOT NULL,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,

    CONSTRAINT fk_paths_to_dem_field_id FOREIGN KEY (field_id) REFERENCES public.fields (field_id)
);

GRANT ALL PRIVILEGES ON TABLE landing.paths_to_dem TO ms_thes;
