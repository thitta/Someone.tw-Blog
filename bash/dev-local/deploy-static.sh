#!/usr/bin/env bash

# source path
site_dirpath="/Users/hsufeng/PycharmProjects/someone_blog/static"
post_dirpath="/Users/hsufeng/Desktop/gc_image_host"

# remote path
gc_site_bucket="gs://blog-someone-tw-static/site"
gc_post_bucket="gs://blog-someone-tw-static/post"

# collect static
cd ~/PycharmProjects/someone_blog
printf 'yes' | python ./manage.py collectstatic

# deploy
gsutil -m rsync -r ${site_dirpath} ${gc_site_bucket}
gsutil -m rsync -r ${post_dirpath} ${gc_post_bucket}
