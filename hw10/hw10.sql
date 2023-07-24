CREATE TABLE parents AS
  SELECT "abraham" AS parent, "barack" AS child UNION
  SELECT "abraham"          , "clinton"         UNION
  SELECT "delano"           , "herbert"         UNION
  SELECT "fillmore"         , "abraham"         UNION
  SELECT "fillmore"         , "delano"          UNION
  SELECT "fillmore"         , "grover"          UNION
  SELECT "eisenhower"       , "fillmore";

CREATE TABLE dogs AS
  SELECT "abraham" AS name, "long" AS fur, 26 AS height UNION
  SELECT "barack"         , "short"      , 52           UNION
  SELECT "clinton"        , "long"       , 47           UNION
  SELECT "delano"         , "long"       , 46           UNION
  SELECT "eisenhower"     , "short"      , 35           UNION
  SELECT "fillmore"       , "curly"      , 32           UNION
  SELECT "grover"         , "short"      , 28           UNION
  SELECT "herbert"        , "curly"      , 31;

CREATE TABLE sizes AS
  SELECT "toy" AS size, 24 AS min, 28 AS max UNION
  SELECT "mini"       , 28       , 35        UNION
  SELECT "medium"     , 35       , 45        UNION
  SELECT "standard"   , 45       , 60;


-- All dogs with parents ordered by decreasing height of their parent
CREATE TABLE by_parent_height AS
  SELECT a.name from dogs as a
  inner join parents as b on a.name = b.child
  inner join dogs as c on b.parent = c.name
  order by c.height desc;


-- The size of each dog
CREATE TABLE size_of_dogs AS
  SELECT a.name, b.size from dogs as a
  inner join sizes as b on (b.min < a.height and a.height <= b.max);


-- Filling out this helper table is optional
CREATE TABLE siblings AS
  SELECT "REPLACE THIS LINE WITH YOUR SOLUTION";

-- Sentences about siblings that are the same size
CREATE TABLE sentences AS
  SELECT 'The two siblings, ' || a.name || ' plus ' || b.name || ' have the same size: ' || a.size 
  from (
    select ax.name, ax.size, ap.parent
    from size_of_dogs as ax
    inner join parents as ap on ax.name = ap.child
  ) as a
  inner join (
    select bx.name, bx.size, bp.parent
    from size_of_dogs as bx
    inner join parents as bp on bx.name = bp.child
  ) as b on (a.parent = b.parent and a.size = b.size and (a.name < b.name));

