#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from wiki.models import Page


def home_page(request):
    return redirect('/view/start.html')


def view_page(request, slug):
    try:
        page = Page.objects.get(slug=slug)
        return render(request, 'view_page.html', {
                      'page': page,
                      'page_title': slug.replace('_', ' ')
                      })
    except Page.DoesNotExist:
        return render(request, 'create_page.html', {
                      'slug': slug,
                      'page_title': slug.replace('_', ' '),
                      })


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        site = request.POST.get('next', '/')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(site)
    else:
        form = AuthenticationForm(request)
        form.fields['username'].widget.attrs.update({
                'placeholder': 'username'
            })
        form.fields['password'].widget.attrs.update({
                'placeholder': 'password'
            })
        site = request.GET.get('next', '/manage')
        return render(request, 'login.html', {
                      'form': form,
                      'next': site,
                      'request': request,
                      })


def logout_user(request):
    """ Log out a user """
    site = request.GET.get('next', '/')
    logout(request)
    return redirect(site)


@login_required(login_url='/login')
def edit_page(request, slug):
    try:
        page = Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        page = None
    return render(request, 'edit_page.html', {
                  'page': page,
                  'page_title': slug.replace('_', ' '),
                  'slug': slug,
                  })


@login_required(login_url='/login')
def save_page(request, slug):
    if request.method == 'POST':
        content = request.POST.get('content', '')
        if content == '':
            return redirect('/edit/{slug}.html'.format(slug=slug))
        page, created = Page.objects.update_or_create(slug=slug, defaults={'content': content})
        return redirect('/view/{slug}.html'.format(slug=page.get_url()))
