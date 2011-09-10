### New Model: packages.CommitsByAuthorByMonth
CREATE TABLE "packages_commitsbyauthorbymonth" (
    "id" serial NOT NULL PRIMARY KEY,
    "date_created" timestamp with time zone NOT NULL,
    "date_modified" timestamp with time zone,
    "author_id" integer NOT NULL REFERENCES "packages_person" ("id") DEFERRABLE INITIALLY DEFERRED,
    "month" date NOT NULL,
    "commit_count" integer NOT NULL
)
;
### New Model: packages.CommitsByPackageByMonth
CREATE TABLE "packages_commitsbypackagebymonth" (
    "id" serial NOT NULL PRIMARY KEY,
    "date_created" timestamp with time zone NOT NULL,
    "date_modified" timestamp with time zone,
    "package_id" integer NOT NULL REFERENCES "packages_package" ("id") DEFERRABLE INITIALLY DEFERRED,
    "month" date NOT NULL,
    "commit_count" integer NOT NULL
)
;
CREATE INDEX "packages_commitsbyauthorbymonth_author_id" ON "packages_commitsbyauthorbymonth" ("author_id");
CREATE INDEX "packages_commitsbypackagebymonth_package_id" ON "packages_commitsbypackagebymonth" ("package_id");
