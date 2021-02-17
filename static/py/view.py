from django.shortcuts import render, redirect


def get_base_context(request, pagename):
    return {
        'pagename': pagename,
        'user': request.user,
    }