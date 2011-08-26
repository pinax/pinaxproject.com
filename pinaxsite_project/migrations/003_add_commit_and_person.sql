### New Model: packages.Person
CREATE TABLE "packages_person" (
    "id" serial NOT NULL PRIMARY KEY,
    "date_created" timestamp with time zone NOT NULL,
    "date_modified" timestamp with time zone,
    "name" varchar(128) NOT NULL,
    "login" varchar(64) NOT NULL,
    "email" varchar(128) NOT NULL
)
;
### New Model: packages.Commit
CREATE TABLE "packages_commit" (
    "id" serial NOT NULL PRIMARY KEY,
    "date_created" timestamp with time zone NOT NULL,
    "date_modified" timestamp with time zone,
    "branch_id" integer NOT NULL REFERENCES "packages_packagebranch" ("id") DEFERRABLE INITIALLY DEFERRED,
    "author_id" integer NOT NULL REFERENCES "packages_person" ("id") DEFERRABLE INITIALLY DEFERRED,
    "committer_id" integer NOT NULL REFERENCES "packages_person" ("id") DEFERRABLE INITIALLY DEFERRED,
    "url" varchar(128) NOT NULL,
    "sha" varchar(64) NOT NULL,
    "committed_date" timestamp with time zone NOT NULL,
    "authored_date" timestamp with time zone NOT NULL,
    "message" text NOT NULL
)
;
CREATE INDEX "packages_commit_branch_id" ON "packages_commit" ("branch_id");
CREATE INDEX "packages_commit_author_id" ON "packages_commit" ("author_id");
CREATE INDEX "packages_commit_committer_id" ON "packages_commit" ("committer_id");
