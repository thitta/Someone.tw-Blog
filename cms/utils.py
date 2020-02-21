from collections import deque
from difflib import SequenceMatcher

from django.contrib.auth.mixins import AccessMixin
from django.db import transaction, IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404

from settings import general_cfg, plugins_cfg
from .forms import LoginForm
from .models import Post, PostRelation, Collection


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
    """algorithm for computing and updating relation ratio"""
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


def get_general_context():
    # static: reboot required if values are changed
    context = {
        "general_cfg": general_cfg,
        "plugins_cfg": plugins_cfg,
    }
    # dynamic: reboot none-required if values are changed
    context["login_form"] = LoginForm()
    context["collections"] = Collection.objects.filter(IsPublic=True).order_by("-RankingIndex")[:16]
    # return
    return context
