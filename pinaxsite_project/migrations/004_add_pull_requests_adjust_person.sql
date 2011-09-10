ALTER TABLE "packages_person" ADD COLUMN "github_id" integer;
ALTER TABLE "packages_person" ADD COLUMN "url" varchar(96);
ALTER TABLE "packages_person" ADD COLUMN "avatar_url" varchar(255);
ALTER TABLE "packages_person" ALTER COLUMN "name" DROP NOT NULL;

### New Model: packages.PullRequest
CREATE TABLE "packages_pullrequest" (
    "id" serial NOT NULL PRIMARY KEY,
    "date_created" timestamp with time zone NOT NULL,
    "date_modified" timestamp with time zone,
    "package_id" integer NOT NULL REFERENCES "packages_package" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" integer NOT NULL REFERENCES "packages_person" ("id") DEFERRABLE INITIALLY DEFERRED,
    "number" integer NOT NULL,
    "state" integer NOT NULL,
    "title" varchar(255),
    "body" text,
    "url" varchar(96) NOT NULL,
    "html_url" varchar(96) NOT NULL,
    "diff_url" varchar(96) NOT NULL,
    "patch_url" varchar(96),
    "issue_url" varchar(96),
    "created_at" timestamp with time zone NOT NULL,
    "closed_at" timestamp with time zone,
    "merged_at" timestamp with time zone,
    "updated_at" timestamp with time zone
)
;
CREATE INDEX "packages_pullrequest_package_id" ON "packages_pullrequest" ("package_id");
CREATE INDEX "packages_pullrequest_user_id" ON "packages_pullrequest" ("user_id");
