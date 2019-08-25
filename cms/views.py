from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic.list import MultipleObjectMixin

from .forms import PostForm
from .models import Post, Collection
from .utils import UserIsPostOwnerMixin, set_post_relations, get_general_context


class PostList(View, MultipleObjectMixin):
    object_list = Post.get_public_posts()
    paginate_by = 12
    context_object_name = "posts"
    url_pattern = "cms_post_list_url"

    def get(self, request):
        ctx = get_general_context()
        ctx.update(super().get_context_data(pagination_base_url=reverse(self.url_pattern)))
        return render(request,
                      template_name="cms/page_post_list.html",
                      context=ctx)


class PostDetail(View):

    def get(self, request, pk, title=""):
        ctx = get_general_context()
        ctx["post"] = get_object_or_404(Post, pk=pk)
        if ctx["post"].IsPublic is True:
            pass
        elif ctx["post"].IsPublic is False and ctx["post"].User == request.user:
            messages.add_message(request, messages.WARNING,
                                 "This post is not published yet and can only be seen by you.")
        else:
            raise Http404()
        return render(request,
                      template_name="cms/page_post_detail.html",
                      context=ctx)


class PostCreate(LoginRequiredMixin, View):

    def get(self, request):
        ctx = get_general_context()
        ctx["form"] = PostForm()
        return render(request,
                      template_name="cms/page_post_form.html",
                      context=ctx)

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.parse_and_save(request.user)
            messages.add_message(request, messages.SUCCESS, f'New post has been created!')
            set_post_relations(trigger_post=post)
            return redirect(post.DetailUrl)
        else:
            ctx = get_general_context()
            ctx["form"] = form
            return render(request,
                          template_name="cms/page_post_form.html",
                          context=ctx)


class PostUpdate(LoginRequiredMixin, UserIsPostOwnerMixin, View):

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        ctx = get_general_context()
        ctx["post"] = post
        ctx["form"] = PostForm(instance=post)
        return render(request,
                      template_name="cms/page_post_form_update.html",
                      context=ctx)

    def post(self, request: HttpRequest, pk):
        post = get_object_or_404(Post, pk=pk)
        former_TitleAndSubtitle = post.TitleAndSubtitle
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.parse_and_save(user=request.user)
            # update relation table
            if former_TitleAndSubtitle != post.TitleAndSubtitle:
                set_post_relations(trigger_post=post)
            # return
            if request.is_ajax():
                return HttpResponse("200_ok")
            else:
                messages.add_message(request, messages.SUCCESS, f'Post has been updated.')
                return redirect(post.DetailUrl)
        else:
            ctx = get_general_context()
            ctx["form"] = form
            # return
            if request.is_ajax():
                return HttpResponseBadRequest()
            else:
                return render(request,
                              template_name="cms/page_post_form_update.html",
                              context=ctx)


class PostDelete(LoginRequiredMixin, UserIsPostOwnerMixin, View):

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        messages.add_message(request, messages.SUCCESS, f'Post has been deleted.')
        return redirect("cms_post_list_url")


class CollectionDetail(View, MultipleObjectMixin):
    object_list = None
    paginate_by = 12
    context_object_name = "posts"
    url_pattern = "cms_collection_detail_url"

    def get(self, request, pk, title):
        collection = get_object_or_404(Collection, pk=pk)
        self.object_list = collection.get_public_posts()
        ctx = get_general_context()
        ctx.update(super().get_context_data(pagination_base_url=
                                            reverse(self.url_pattern, kwargs={"pk": pk, "title": title})))
        ctx["collection"] = collection
        return render(request,
                      template_name="cms/page_post_list.html",
                      context=ctx)


class SearchRedirect(View):

    def get(self, request):
        term = request.GET["term"]
        if len(term) == 0:
            source_page = request.GET.get('source_page', '/')
            return HttpResponseRedirect(source_page)
        return redirect("cms_search_list_url", term=term)


class SearchList(View, MultipleObjectMixin):
    object_list = None
    paginate_by = 12
    context_object_name = "posts"
    url_pattern = "cms_search_list_url"

    def get(self, request, term):
        self.object_list = Post.get_searched_posts(term)
        ctx = get_general_context()
        ctx.update(super().get_context_data(pagination_base_url=reverse(self.url_pattern, kwargs={"term": term})))
        ctx["term"] = term
        return render(request,
                      template_name="cms/page_post_list.html",
                      context=ctx)


class PostAdmin(LoginRequiredMixin, View, MultipleObjectMixin):
    object_list = None
    paginate_by = 12
    context_object_name = "posts"
    url_pattern = "cms_post_admin_url"

    def get(self, request):
        self.object_list = Post.objects.filter(User=request.user).order_by("IsPublic", "IsOnList", "Title")
        ctx = get_general_context()
        messages.add_message(request, messages.WARNING, f"This page can only be seen by you.")
        ctx.update(super().get_context_data(pagination_base_url=reverse(self.url_pattern)))
        return render(request,
                      template_name="cms/page_post_admin.html",
                      context=ctx)
