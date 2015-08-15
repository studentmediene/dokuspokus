#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from haystack.management.commands import update_index
from wiki.models import Page, LinkGroup
from django.http import JsonResponse
from markdown_shortcodes import shortcode
from wiki.utils.slugify import slugify
import reversion
import reversion_compare


def home_page(request):
    return redirect('/view/start.html')


def view_page(request, slug):
    link_groups = LinkGroup.objects.all()
    slug = slug.lower()
    try:
        page = Page.objects.get(slug=slug)
        return render(request, 'view_page.html', {
                      'page': page,
                      'link_groups': link_groups,
                      })
    except Page.DoesNotExist:
        return render(request, 'create_page.html', {
                      'slug': slug,
                      'page_title': slug.replace('-', ' '),
                      'link_groups': link_groups,
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

    link_groups = LinkGroup.objects.all()
    form = AuthenticationForm(request)
    form.fields['username'].widget.attrs.update({
            'placeholder': 'brukernavn'
        })
    form.fields['password'].widget.attrs.update({
            'placeholder': 'passord'
        })
    site = request.GET.get('next', '/')
    return render(request, 'login.html', {
                  'form': form,
                  'next': site,
                  'request': request,
                  'link_groups': link_groups,
                  })


def logout_user(request):
    """ Log out a user """
    site = request.GET.get('next', '/')
    logout(request)
    return redirect(site)


@login_required(login_url='/login')
def page_history(request, slug):
    link_groups = LinkGroup.objects.all()
    page = Page.objects.get(slug=slug)
    version_list = reversion.get_unique_for_object(page)

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
                  'changelog': changelog,
                  'link_groups': link_groups,
                  })


@login_required(login_url='/login')
def page_change(request, slug, version_id):
    try:
        version_id = abs(int(version_id))
    except TypeError:
        version_id = 0

    page = Page.objects.get(slug=slug)
    version_list = reversion.get_unique_for_object(page)

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
    link_groups = LinkGroup.objects.all()
    if request.GET:
        title = request.GET.get('title', slug.replace('-', ' '))
    else:
        title = slug.replace('-', ' ')
    try:
        page = Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        page = None
    return render(request, 'edit_page.html', {
                  'page': page,
                  'page_title': title,
                  'slug': slug,
                  'link_groups': link_groups,
                  })


@login_required(login_url='/login')
def save_page(request, slug):
    if request.method == 'POST':
        content = request.POST.get('content', '')
        title = request.POST.get('title', slug.replace('-', '').title())
        if content == '':
            return redirect('/edit/{slug}.html'.format(slug=slug))
        try:
            page = Page.objects.get(slug=slug)
            setattr(page, 'content', content)
            page.save()
        except Page.DoesNotExist:
            page = Page(slug=slug, content=content, title=title)
            page.save()
        update_index.Command().handle(using=['default'], remove=True)
        return redirect('/view/{slug}.html'.format(slug=page.get_url()))


@login_required(login_url='/login')
def delete_page(request):
    if request.method == 'POST':
        slug = request.POST.get('slug', '')
        print(slug)
        if slug != '':
            Page.objects.filter(slug=slug).delete()
            update_index.Command().handle(using=['default'], remove=True)
        return redirect('/')


# Shortcodes
@shortcode
def shortcode_side(*args):
    link = slugify(args[0].split('#')[0].lower())
    segment = slugify(args[0].split('#')[-1].lower()) if '#' in args[0] else ''
    title = args[-1]
    try:
        Page.objects.get(slug=link)
        link_class = ''
    except Page.DoesNotExist:
        link_class = 'DoesNotExist'
    return render_to_string('shortcodes/link.html', {
        'link': link,
        'segment': segment,
        'title': title,
        'class': link_class,
    })
