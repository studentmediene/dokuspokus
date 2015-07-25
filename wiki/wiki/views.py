#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from wiki.models import Page
from django.http import JsonResponse
import reversion
import reversion_compare


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
def page_history(request, slug):

    page = Page.objects.get(slug=slug)
    version_list = reversion.get_unique_for_object(page)

    """
    version_id = int(request.GET.get('id', -1))
    if version_id >= 0:
        if version_id + 1 >= len(version_list):
            compare = ''
        else:
            compare = version_list[version_id + 1].field_dict['content']

        html = reversion_compare.helpers.html_diff(version_list[version_id].field_dict['content'],
                                                   compare)
        return render(request, 'page_history_diff.html', {
                      'page': page,
                      'slug': slug,
                      'page_title': slug.replace('_', ' '),
                      'html': html,
                      })
    """

    changelog = list()
    for i in range(len(version_list)):
        if i < len(version_list) - 1:
            diff = len(version_list[i].field_dict['content'].replace('\n', '').replace('\r', '')) - len(version_list[i+1].field_dict['content'].replace('\n', '').replace('\r', ''))
            if diff < 0:
                diff_text = '-{} characters'.format(abs(diff))
            else:
                diff_text = '+{} characters'.format(diff)
        else:
            diff_text = '+{} characters'.format(len(version_list[i].field_dict['content'].replace('\n', '').replace('\r', '')))
        changelog.append({
                         'id': version_list[i].revision.id,
                         'user': version_list[i].revision.user,
                         'date': version_list[i].revision.date_created,
                         'diff': diff_text
                         })

    return render(request, 'page_history.html', {
                  'page': page,
                  'slug': slug,
                  'page_title': slug.replace('_', ' '),
                  'changelog': changelog,
                  })


@login_required(login_url='/login')
def page_change(request, slug, version_id):

    try:
        version_id = abs(int(version_id))
    except TypeError:
        version_id = 0

    page = Page.objects.get(slug=slug)
    version_list = reversion.get_unique_for_object(page)

    # version_id = len(reversion.get_unique_for_object(page)) - version_id - 1

    try:
        if version_id + 1 >= len(version_list):
            compare = ''
        else:
            compare = version_list[version_id + 1].field_dict['content']

        html = reversion_compare.helpers.html_diff(compare,
                                                   version_list[version_id].field_dict['content'])
    except IndexError:
        html = ''

    return JsonResponse({
                  'slug': slug,
                  'page_title': slug.replace('_', ' '),
                  'html': html,
                  })


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
