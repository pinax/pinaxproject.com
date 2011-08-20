### New Model: packages.Package_package_uses
CREATE TABLE "packages_package_package_uses" (
    "id" serial NOT NULL PRIMARY KEY,
    "from_package_id" integer NOT NULL,
    "to_package_id" integer NOT NULL,
    UNIQUE ("from_package_id", "to_package_id")
)
;
### New Model: packages.Package
CREATE TABLE "packages_package" (
    "id" serial NOT NULL PRIMARY KEY,
    "date_created" timestamp with time zone NOT NULL,
    "date_modified" timestamp with time zone,
    "name" varchar(96) NOT NULL,
    "package_type" integer NOT NULL,
    "repo_url" varchar(200) NOT NULL,
    "description" text,
    "pinax_external" boolean NOT NULL,
    "maturity_level" integer,
    "status" integer,
    "comment" varchar(255),
    "docs_url" varchar(200),
    "blog_post_id" integer REFERENCES "biblion_post" ("id") DEFERRABLE INITIALLY DEFERRED,
    "cpc_tag" varchar(64),
    "package_name" varchar(96)
)
;
ALTER TABLE "packages_package_package_uses" ADD CONSTRAINT "from_package_id_refs_id_ac1219e2" FOREIGN KEY ("from_package_id") REFERENCES "packages_package" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "packages_package_package_uses" ADD CONSTRAINT "to_package_id_refs_id_ac1219e2" FOREIGN KEY ("to_package_id") REFERENCES "packages_package" ("id") DEFERRABLE INITIALLY DEFERRED;
### New Model: packages.CommitActivityFeed
CREATE TABLE "packages_commitactivityfeed" (
    "id" serial NOT NULL PRIMARY KEY,
    "date_created" timestamp with time zone NOT NULL,
    "date_modified" timestamp with time zone,
    "app_id" integer NOT NULL REFERENCES "packages_package" ("id") DEFERRABLE INITIALLY DEFERRED,
    "feed_url" varchar(200) NOT NULL,
    "branch_name" varchar(96) NOT NULL,
    "active" boolean NOT NULL
)
;
CREATE INDEX "packages_package_package_uses_from_package_id" ON "packages_package_package_uses" ("from_package_id");
CREATE INDEX "packages_package_package_uses_to_package_id" ON "packages_package_package_uses" ("to_package_id");
CREATE INDEX "packages_package_blog_post_id" ON "packages_package" ("blog_post_id");
CREATE INDEX "packages_commitactivityfeed_app_id" ON "packages_commitactivityfeed" ("app_id");
