import markdown
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery
from markdown.extensions.extra import ExtraExtension


class Profile(models.Model):
    User = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    DisplayName = models.CharField(max_length=64)

    def __str__(self):
        return self.DisplayName


class Post(models.Model):
    # basic columns
    PostId = models.AutoField(primary_key=True, max_length=256)
    Title = models.CharField(max_length=256)
    Subtitle = models.CharField(max_length=256)
    BodyMarkdown = models.TextField()
    BodyHTML = models.TextField()
    CoverImageUrl = models.URLField(blank=True)
    # public and ranking
    IsOnList = models.BooleanField(default=True)
    IsPublic = models.BooleanField(default=True)
    IsTop = models.BooleanField(default=False)
    RankingIndex = models.IntegerField(default=0)
    # datetime
    CreateDate = models.DateTimeField(auto_now_add=True)
    UpdateDate = models.DateTimeField(auto_now=True)
    # FK
    User = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name="Posts", on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['IsPublic']),
            models.Index(fields=['IsTop']),
        ]

    def __str__(self):
        return f"({self.PostId}){self.Title}"

    @classmethod
    def create_mock_instance(cls, user, **kwargs):
        data = dict()
        data["Title"] = "x"
        data["Subtitle"] = "x"
        data["BodyMarkdown"] = "x"
        data["BodyHTML"] = "x"
        data["CoverImageUrl"] = "x"
        data["IsOnList"] = True
        data["IsPublic"] = True
        data["IsOnList"] = True
        data["RankingIndex"] = 0
        data["User"] = user
        data.update(kwargs)
        return cls.objects.create(**data)

    def parse_and_save(self, user=None, user_id=None):
        # parse markdown into html
        md_extentions = [ExtraExtension()]
        self.BodyHTML = markdown.markdown(self.BodyMarkdown, extensions=md_extentions)
        # append user FK
        if user is not None:
            self.User = user
        else:
            self.User_id = user_id if user_id is not None else self.User_id
        # save
        self.save()

    @classmethod
    def get_public_posts(cls):
        posts = cls.objects.filter(IsPublic=True, IsOnList=True) \
            .order_by("-IsTop", "-RankingIndex", "-CreateDate")
        return posts

    @classmethod
    def get_searched_posts(cls, text):
        vector = SearchVector('Title', 'Subtitle', 'BodyMarkdown')
        query = SearchQuery(text)
        posts = cls.objects.annotate(rank=SearchRank(vector, query)). \
            filter(IsPublic=True, rank__gte=0.02).order_by('-rank')
        return posts

    @property
    def Abstract(self):
        return self.BodyHTML.split("\n")[0]

    @property
    def DetailUrl(self):
        kwargs = dict()
        kwargs["pk"] = self.pk
        kwargs["title"] = self.Title.strip().replace(" ", "-")
        return reverse("cms_post_detail_url", kwargs=kwargs)

    @property
    def AbsoluteUrl(self):
        kwargs = dict()
        kwargs["pk"] = self.pk
        return reverse("cms_post_detail_absolute_url", kwargs=kwargs)

    @property
    def UpdateUrl(self):
        return reverse("cms_post_update_url", kwargs={"pk": self.pk})

    @property
    def DeleteUrl(self):
        return reverse("cms_post_delete_url", kwargs={"pk": self.pk})

    @property
    def TitleAndSubtitle(self):
        return f"{self.Title}-{self.Subtitle}"

    @property
    def RelatedPosts(self):
        relations = PostRelation.objects.filter(FromPost=self.PostId, Ratio__gte=0.35).order_by("-Ratio")[:3]
        result = [relation.ToPost for relation in relations
                  if self.IsOnList == relation.ToPost.IsOnList and relation.ToPost.IsPublic is True]
        return result


class SiteConfig(models.Model):
    Name = models.CharField(max_length=32, primary_key=True)
    CategoryName = models.CharField(max_length=32)
    Value = models.CharField(max_length=128)

    def __str__(self):
        return self.Name


class PostRelation(models.Model):
    PostRelationId = models.AutoField(primary_key=True)
    FromPost = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="ToPosts")
    ToPost = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="FromPosts")
    Ratio = models.FloatField()

    class Meta:
        indexes = [
            models.Index(fields=["Ratio"])
        ]
        unique_together = ("FromPost", "ToPost")

    def __srt__(self):
        return f"Post({self.FromPost.PostId}) to Post({self.ToPost.PostId})"


class Collection(models.Model):
    CollectionId = models.AutoField(primary_key=True, max_length=256)
    DisplayName = models.CharField(max_length=256)
    IsPublic = models.BooleanField(default=True)
    RankingIndex = models.IntegerField(default=0)
    CreateDate = models.DateTimeField(auto_now_add=True)
    Posts = models.ManyToManyField(Post)

    def __str__(self):
        return self.DisplayName

    def get_public_posts(self):
        posts = self.Posts.filter(IsPublic=True).order_by("-IsTop", "-RankingIndex", "-CreateDate")
        return posts

    @classmethod
    def create_mock_instance(cls, **kwargs):
        data = dict()
        data["DisplayName"] = "x"
        data["IsPublic"] = True
        data["RankingIndex"] = 0
        for key, val in kwargs.items():
            data[key] = val
        return cls.objects.create(**data)

    @property
    def DetailUrl(self):
        kwargs = dict()
        kwargs["pk"] = self.CollectionId
        kwargs["title"] = self.DisplayName.strip().replace(" ", "-")
        return reverse("cms_collection_detail_url", kwargs=kwargs)
