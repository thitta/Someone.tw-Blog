from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, \
    CollectionDetail, SearchList, SearchRedirect, PostAdmin



urlpatterns = [
    path("", PostList.as_view(), name="cms_post_list_url"),
    # Post
    path(r"post/create", PostCreate.as_view(), name="cms_post_create_url"),
    path(r"post/<int:pk>/update", PostUpdate.as_view(), name="cms_post_update_url"),
    path(r"post/<int:pk>/delete", PostDelete.as_view(), name="cms_post_delete_url"),
    path(r"post/<int:pk>/<str:title>", PostDetail.as_view(), name="cms_post_detail_url"),
    path(r"post/<int:pk>", PostDetail.as_view(), name="cms_post_detail_absolute_url"),
    # Collection
    path(r"collection/<int:pk>/<str:title>", CollectionDetail.as_view(), name="cms_collection_detail_url"),
    # search
    path(r"search", SearchRedirect.as_view(), name="cms_search_redirect_url"),
    path(r"search/<str:term>/", SearchList.as_view(), name="cms_search_list_url"),
    # postadmin
    path(r"postadmin", PostAdmin.as_view(), name="cms_post_admin_url")
]
