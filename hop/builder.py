# -*- coding: utf-8 -*-

from utils import (
    escape, 
    mk_literal,
    sstrip,
)


def build_html_params(**params):
    params_list = list()
    for (name, value) in params.items():
        if name[0] == u'_':
            name = name[1:]
        params_list.append(u' {0}="{1}"'.format(
            escape(name), 
            escape(value),
        ))
    return u''.join(params_list)


def build_html_object_open_tag(object_name, **params):
    return mk_literal(u'<{0}{1}>'.format(
        sstrip(escape(object_name)),
        build_html_params(**params),
    ))


def build_html_object_close_tag(object_name):
    return mk_literal(u'</{0}>'.format(sstrip(escape(object_name))))


def build_html_object(object_name, body, **params):
    return mk_literal(u''.join([
        build_html_object_open_tag(object_name, **params),
        escape(body),
        build_html_object_close_tag(object_name),
    ]))


def build_html_self_closing_object(object_name, **params):
    return mk_literal(u'<{0}{1} />'.format(
        sstrip(escape(object_name)),
        build_html_params(**params),
    ))
