# -*- coding: utf-8 -*-

from ..builder import (
    build_html_object,
    build_html_object_close_tag,
    build_html_object_open_tag,
    build_html_self_closing_object,
)
from ..utils import (
    mk_literal,
    safestr, 
    sstrip,
    validate_url,
)


def a(href, body=None, title=None, **params):
    if 'validate_url' in params:
        params.pop('validate_url')
        href = validate_url(href, special_protocols=True)
    else:
        href = sstrip(href)

    if not body:
        body = safestr(href)
    if title == None:
        title = safestr(body)

    params['href'] = href
    params['title'] = title

    if title == False:
        params.pop('title')

    return build_html_object(u'a', body, **params)


def img(src, alt=None, **params):
    if 'validate_url' in params:
        params.pop('validate_url')
        params['src'] = validate_url(src, special_protocols=True)
    else:
        params['src'] = sstrip(src)

    if alt:
        params['alt'] = alt
    else:
        params['alt'] = u''
    return build_html_self_closing_object(u'img', **params)


def style(href, **params):
    if 'validate_url' in params:
        params.pop('validate_url')
        href = validate_url(href, special_protocols=True)
    else:
        href = sstrip(href)

    params.update({
        'href': href,
        'rel': u'stylesheet',
        'type': u'text/css',
    })
    return build_html_self_closing_object(u'link', **params)


def script(src, **params):
    if 'validate_url' in params:
        params.pop('validate_url')
        src = validate_url(src, special_protocols=True)
    else:
        src = sstrip(src)

    params.update({
        'src': src,
        'type': u'text/javascript',
    })
    return build_html_object(u'script', u'', **params)


def meta_charset(charset='utf-8'):
    params = {
        'content': u'text/html; charset={0}'.format(charset),
        'http-equiv': u'Content-Type',
    }
    return build_html_self_closing_object(u'meta', **params)


def title(title):
    return build_html_object('title', title)


def comment(comment):
    return mk_literal(u'<!-- {0} -->'.format(comment))


def html_list(items=list(), list_type='ul', **params):
    '''
    Item param can be string or list
        with tuples/lists looking like this:

        [(item1_body, item1_options),(item2_body, item2_options)]
    '''
    out_html = [
        build_html_object_open_tag(list_type, **params),
    ]
    for item in items:
        body = u'&nbsp;'
        params = dict()

        if type(item) == list or type(item) == tuple:
            item_len = len(item)
            if item_len > 0:
                body = item[0]
            if item_len > 1:
                params = item[1]
        elif sstrip(item) != u'':
            body = sstrip(item)

        li_obj = build_html_object(u'li', body, **params)
        out_html.append(li_obj)

    closing_tag = build_html_object_close_tag(list_type)
    out_html.append(closing_tag)
    return mk_literal(u''.join(out_html))


##########################
# aliases and wrappers

link = a
charset = meta_charset

def email(email, body=None, title=None, **params):
    href = u'mailto:{0}'.format(email)
    if not body:
        body = email
    if not title:
        title = u'Mail to {0}'.format(email)
    return a(href, body, title, **params)

def ul(items=list(), **params):
    return html_list(items, u'ul', **params)

def ol(items=list(), **params):
    return html_list(items, u'ol', **params)
