from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from .forms import LoginForm
from cms.utils import get_site_context


class Login(View):
    ERR_MSG = "Invalid account or password."

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, f'Welcome back, {user.profile.DisplayName}')
                return HttpResponseRedirect(request.GET.get('next'))
            else:
                messages.add_message(request, messages.ERROR, self.ERR_MSG)
                return HttpResponseRedirect(request.GET.get('next'))
        else:
            messages.add_message(request, messages.ERROR, self.ERR_MSG)
            return HttpResponseRedirect(request.GET.get('next'))


class Logout(View):
    MSG = "Bye~Bye!"

    def post(self, request):
        logout(request)
        messages.add_message(request, messages.SUCCESS, self.MSG)
        return redirect(reverse("cms_post_list_url"))


def handler404(request, exception=None):
    ctx = dict()
    ctx["status"] = 404
    ctx = get_site_context()
    return render(request, 'cms/page_404.html', context=ctx, status=404)


def handler500(request):
    ctx = dict()
    ctx["status"] = 500
    ctx = get_site_context()
    return render(request, 'cms/page_500.html', context=ctx, status=500)
