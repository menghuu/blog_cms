#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 m <m@meng.hu>
#
# Distributed under terms of the MIT license.

from flask.blueprints import Blueprint
from flask import render_template, abort, request, current_app
from flask_flatpages import FlatPages, pygments_style_defs
from flask_paginate import Pagination, get_page_parameter
from lxml import etree
import re
import os
import time
import datetime

pages = FlatPages()

bp = Blueprint('blog', 'blog')


@bp.app_template_filter('get_summary')
def get_summary(html_str):
    pattern = re.compile(r'<\s*!\s*-\s*-\s*more\s*-\s*-\s*>')
    matcher = pattern.search(html_str)

    get_summary_from_p = True
    limit = 200
    if matcher:
        start, end = matcher.span()
        if html_str[:start].strip():
            html_str = html_str[:start].strip()
            get_summary_from_p = False

    html = etree.HTML(html_str)
    if not html:
        return html
    for ele in html.xpath('//div[@class="toc"]'):
        # remove all toc
        ele.getparent().remove(ele)

    if get_summary_from_p:
        ps = html.xpath('//p')
        if ps:
            p = ps[0]
            summary_html_str = etree.tostring(p).decode()
        else:
            summary_html_str = etree.tostring(html)[:limit].decode()
    else:
        summary_html_str = etree.tostring(html).decode()

    return summary_html_str


@bp.route('/index')
@bp.route('/')
def index():
    search = False
    q = request.args.get('q')
    per_page = current_app.config['PAGINATE_PER_PAGE']
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    sorted_pages = list(sorted(
        filter(lambda page: page.meta['title'] != 'About', pages),
        key=lambda page: page.meta.get('update', None) or page.meta.get(
            'published',
            datetime.date.fromtimestamp(
                os.path.getctime(os.path.join(pages.root, page.path + pages.config('extension'))))
        ),
        reverse=True
    ))

    cut_pages = sorted_pages[(page - 1) * per_page: page * per_page]

    pagination = Pagination(
        page=page, total=len(sorted_pages), per_page=per_page, search=search,
        record_name='articles', bs_version='3.3'
    )

    return render_template('index.html', pages=cut_pages, pagination=pagination)


@bp.route('/<path:path>')
def post(path):
    page = pages.get_or_404(path)
    layout = page.meta.get('layout', 'post')
    if layout != 'draft':
        template = layout + '.html'
        return render_template(template, page=page)
    else:
        abort(404)


@bp.route('/archives')
def archives():
    sorted_pages = list(sorted(
        filter(
            lambda page: page.meta['title'] != 'About', pages),
        key=lambda page: page.meta.get('update', None) or page.meta.get(
            'published',
            datetime.date.fromtimestamp(
                os.path.getctime(os.path.join(pages.root, page.path + pages.config('extension')))
            )
        ),
        reverse=True
    ))
    return render_template('archives.html', pages=sorted_pages)


@bp.route('/tags/<tag>')
def tags(tag):
    sorted_pages = list(sorted(
        filter(lambda page: page.meta['title'] != 'About' and tag in page.meta.get('tags', []), pages),
        key=lambda page: page.meta.get('update', None) or page.meta.get(
            'published',
            datetime.date.fromtimestamp(
                os.path.getctime(os.path.join(pages.root, page.path + pages.config('extension')))
            )
        ),
        reverse=True
    ))
    return render_template('tags.html', pages=sorted_pages, tag=tag)


@bp.route('/about')
def about():
    page = pages.get_or_404('about')
    template = page.meta.get('layout', 'post') + '.html'
    return render_template(template, page=page)
