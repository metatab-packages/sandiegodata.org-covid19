# Task definitions for invoke
# You must first install invoke, https://www.pyinvoke.org/

from invoke import task

# Set this to the S3 bucket where you will publish public data packages
# You must have a boto or .aws configuration and credentials to access the bucket
# s3_bucket = 'library.metatab.org'
s3_bucket = None

# Set the wordpress site where package documentation and links will be published
# The string is a reference to the `wordpress` section in  ~/.metapack.yaml .
# wp_site = 'dataa.sandiegodata.org'
wp_site = None

# Groups will be come categories when publishing to Wordpress
groups = ['Health']
# Tags are tags when publilshing to wordpress.
tags = ['county', 'national']

group_flags = ' '.join([f"-g{g}" for g in groups])
tag_flags = ' '.join([f"-t{t}" for t in tags])


def force_flag(force):
    return '-F' if force else ''


wp_flags = f' -w {wp_site} {group_flags} {tag_flags}' if wp_site else ''
s3_flags = f' -s {s3_bucket}' if s3_bucket else ''


@task
def make(c, force=False):
    """Build, write to S3, and publish to wordpress, but only if necessary"""
    c.run(f'mp -q  make {force_flag(force)} -r  -b {s3_flags} {wp_flags}')


@task
def build(c, force=False):
    # Build a filesystem package.
    c.run(f"mp build -r {force_flag(force)}")


# Publish to s3 and wordpress, if the proper bucket and site
# variables are defined
@task
def publish(c):
    if s3_bucket:
        c.run(f"mp s3 -s {s3_bucket}")
    if wp_site:
        c.run(f"mp wp -s {wp_site} {group_flags} {tag_flags} -p")
