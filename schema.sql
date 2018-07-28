DROP TABLE IF EXISTS Hikes CASCADE;
CREATE TABLE Hikes (
   id SERIAL  PRIMARY KEY
  , hike_name text
  , region text
  , subregion text
  , total_distance numeric
  , elevation_gain numeric
  , time_from_seattle numeric
  , coast boolean
  , stars numeric
  , dogs_allowed_on_leash boolean
  , established_campsites boolean
  , fall_foliage boolean
  , good_for_kids boolean
  , lakes boolean
  , mountain_views boolean
  , old_growth boolean
  , ridges_passes boolean
  , rivers boolean
  , summits boolean
  , waterfalls boolean
  , wildflowers_meadows boolean
  , wildlife boolean
  , url text
);

DROP TABLE IF EXISTS Tripreports CASCADE;
CREATE TABLE Tripreports (
   author_id numeric
  , creator_id numeric
  , create_date timestamptz
  , hike_id numeric
  , id SERIAL  PRIMARY KEY
  , rating numeric
  , review_text text
);

DROP TABLE IF EXISTS Authors CASCADE;
CREATE TABLE Authors (
   id SERIAL  PRIMARY KEY
  , member_since timestamptz
  , name text
);
