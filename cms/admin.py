from django.contrib import admin

from .models import Post, Profile, PostRelation, Collection

# Register your models here.
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(PostRelation)
admin.site.register(Collection)
