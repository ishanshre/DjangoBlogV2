from django.contrib import admin
from .models import Post, Comment, Profile, Follower
# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','slug','author','publish','status']
    list_filter = ['status','created','publish','author']
    search_fields = ['title','body']
    prepopulated_fields = {
        'slug':('title',)
    }
    raw_id_fields = ['author']
    ordering = ['status','publish']


admin.site.register(Comment)

admin.site.register(Profile)

admin.site.register(Follower)