from collections import deque
from difflib import SequenceMatcher

from django.conf import settings
from django.contrib.auth.mixins import AccessMixin
from django.db import transaction, IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .forms import LoginForm
from .models import Post, PostRelation, Collection, SiteConfig


class UserIsPostOwnerMixin(AccessMixin):
    """Verify that the current user is the owner of the post."""

    def dispatch(self, request, *args, **kwargs):
        user_of_the_post = get_object_or_404(Post, pk=kwargs["pk"]).User
        if user_of_the_post != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


def reset_post_relations():
    """truncate and reset all post relations
        this function is used when importing data into database"""
    PostRelation.objects.all().delete()
    relations = []
    posts = deque(Post.objects.all())
    while posts:
        from_post = posts.pop()
        for to_post in posts:
            relations.append(PostRelation(
                FromPost=from_post,
                ToPost=to_post,
                Ratio=get_related_ratio(from_post.TitleAndSubtitle, to_post.TitleAndSubtitle)
            ))
    relations = relations + [PostRelation(FromPost=r.ToPost, ToPost=r.FromPost, Ratio=r.Ratio) for r in relations]
    PostRelation.objects.bulk_create(relations)


def set_post_relations(trigger_post) -> None:
    """ algorithm for computing and updating relation ratio
    the operation_type should be 'create', 'update' or 'delete'"""
    # compute
    post_relations = []
    to_posts = Post.objects.exclude(PostId=trigger_post.PostId)
    for to_post in to_posts:
        post_relations.append(PostRelation(
            FromPost=trigger_post,
            ToPost=to_post,
            Ratio=get_related_ratio(trigger_post.TitleAndSubtitle, to_post.TitleAndSubtitle)
        ))
    post_relations = post_relations + \
                     [PostRelation(FromPost=pr.ToPost, ToPost=pr.FromPost, Ratio=pr.Ratio) for pr in post_relations]
    # transaction
    with transaction.atomic():
        try:
            PostRelation.objects.filter(Q(ToPost=trigger_post) | Q(FromPost=trigger_post)).delete()
            PostRelation.objects.bulk_create(post_relations)
        except IntegrityError as e:
            raise e


def get_related_ratio(text1: str, text2: str) -> float:
    return round(SequenceMatcher(None, text1, text2).quick_ratio(), 4)


def get_site_context():
    context = {
        "login_form": LoginForm(),
        "collections": Collection.objects.filter(IsPublic=True).order_by("-RankingIndex")[:16],
        "nav_buttons": settings.NAV_BUTTONS,
        "site_title": settings.SITE_TITLE,
        "site_subtitle": settings.SITE_SUBTITLE,
        "plugins": settings.PLUGINS,
        "author_name": SiteConfig.get(name_space="author", key="name").Value,
        "author_description": SiteConfig.get(name_space="author", key="description").Value,
    }
    return context
