DROP TABLE "packages_commitactivityfeed";

### New Model: packages.PackageBranch
CREATE TABLE "packages_packagebranch" (
    "id" serial NOT NULL PRIMARY KEY,
    "date_created" timestamp with time zone NOT NULL,
    "date_modified" timestamp with time zone,
    "package_id" integer NOT NULL REFERENCES "packages_package" ("id") DEFERRABLE INITIALLY DEFERRED,
    "branch_name" varchar(96) NOT NULL,
    "active" boolean NOT NULL
);