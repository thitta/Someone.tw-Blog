from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from cms.models import Post, Collection, PostRelation
from .utils import reset_post_relations

USER1 = {"username": "john", "password": "123456"}
USER2 = {"username": "mary", "password": "123456"}


class CmsModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # create user
        User = get_user_model()
        user1 = User.objects.create_user(**USER1)
        user2 = User.objects.create_user(**USER2)
        # create mock data
        posts = [None] * 6
        posts[0] = Post.create_mock_instance(user1, IsPublic=True, IsOnList=True, RankingIndex=0, )
        posts[1] = Post.create_mock_instance(user1, IsPublic=True, IsOnList=True, RankingIndex=2, )
        posts[2] = Post.create_mock_instance(user1, IsPublic=True, IsOnList=True, RankingIndex=0, )
        posts[3] = Post.create_mock_instance(user1, IsPublic=True, IsOnList=True, RankingIndex=0, IsTop=True)
        posts[4] = Post.create_mock_instance(user1, IsPublic=True, IsOnList=False)
        posts[5] = Post.create_mock_instance(user1, IsPublic=False, IsOnList=False)
        reset_post_relations()
        # Collections
        collections = [None] * 3
        collections[0] = Collection.create_mock_instance(IsPublic=True)
        collections[1] = Collection.create_mock_instance(IsPublic=False)
        collections[0].Posts.add(posts[0], posts[1], posts[4], posts[5])

    # ------------------------------
    # post:read
    # ------------------------------

    def test_ok_GET_post_list(self):
        c = Client()
        res = c.get("/")
        # status code
        exp = 200
        act = res.status_code
        self.assertEqual(exp, act)
        # posts length
        exp = 4
        act = len(res.context["posts"])
        self.assertEqual(exp, act)

    def test_ok_GET_post_detail(self):
        # ok
        c = Client()
        res = c.get("/post/1/title")
        exp = 200
        act = res.status_code
        self.assertEqual(exp, act)
        # none public post: return 404
        c = Client()
        res = c.get("/post/6/title")
        exp = 404
        act = res.status_code
        self.assertEqual(exp, act)
        # none existent post: return 404
        c = Client()
        res = c.get("/post/999/title")
        exp = 404
        act = res.status_code
        self.assertEqual(exp, act)

    # ------------------------------
    # post:create/update/delete
    # ------------------------------

    def test_ok_GET_create_post(self):
        # ok
        c = Client()
        c.login(**USER1)
        res = c.get("/post/create")
        exp = 200
        act = res.status_code
        self.assertEqual(exp, act)
        # not login: return redirect
        c = Client()
        res = c.get("/post/create")
        exp = 302
        act = res.status_code
        self.assertEqual(exp, act)

    def test_ok_GET_update_post(self):
        # ok
        c = Client()
        c.login(**USER1)
        res = c.get("/post/1/update")
        exp = 200
        act = res.status_code
        self.assertEqual(exp, act)
        # not login: return redirect
        c = Client()
        res = c.get("/post/1/update")
        exp = 302
        act = res.status_code
        self.assertEqual(exp, act)
        # login but not author: return forbidden
        c = Client()
        c.login(**USER2)
        res = c.get("/post/1/update")
        exp = 403
        act = res.status_code
        self.assertEqual(exp, act)

    def test_ok_POST_create_update_delete_post(self):
        # prepare: login
        c = Client()
        User = get_user_model()
        c.login(**USER1)
        user = User.objects.get(username=USER1["username"])
        mock_post_created = {"Title": "Created Post",
                             "Subtitle": "xxx", "BodyMarkdown": "xxx", "User": user,
                             "IsOnList": True, "IsPublic": True, "IsTop": True, "RankingIndex": 0}

        # create_ok: redirect 302
        res = c.post(f"/post/create", data=mock_post_created, follow=True)
        final_url, status_code = res.redirect_chain[-1]
        exp = 302
        act = status_code
        self.assertEqual(exp, act)
        # create_ok: post is correctly created
        created_post_id = int(final_url.split("/")[2])
        created_post = Post.objects.get(PostId=created_post_id)
        exp = mock_post_created["Title"]
        act = created_post.Title
        self.assertEqual(exp, act)
        # update_ok: redirect 302
        mock_post_updated = mock_post_created.copy()
        mock_post_updated["Title"] = "Updated Post"
        res = c.post(f"/post/{created_post_id}/update", data=mock_post_updated, follow=True)
        final_url, status_code = res.redirect_chain[-1]
        exp = 302
        act = status_code
        self.assertEqual(exp, act)
        # update_ok: post is correctly updated
        updated_post_id = int(final_url.split("/")[2])
        updated_post = Post.objects.get(PostId=updated_post_id)
        exp = mock_post_updated["Title"]
        act = updated_post.Title
        self.assertEqual(exp, act)
        # update_ok: the created and updated post should be the same post
        self.assertEqual(created_post_id, updated_post_id)

        # delete_ok: redirect 302
        res = c.post(f"/post/{created_post_id}/delete", data=mock_post_updated, follow=True)
        final_url, status_code = res.redirect_chain[-1]
        exp = 302
        act = status_code
        self.assertEqual(exp, act)
        # delete_raise: post is no longer exists
        with self.assertRaises(ObjectDoesNotExist):
            Post.objects.get(PostId=created_post_id)

    # ------------------------------
    # collection: read
    # ------------------------------

    def test_ok_collection_post_list(self):
        c = Client()
        res = c.get("/collection/1/collectionTitle")
        # http status
        exp = 200
        act = res.status_code
        self.assertEqual(exp, act)
        # posts length
        exp = 3
        act = len(res.context["posts"])
        self.assertEqual(exp, act)
