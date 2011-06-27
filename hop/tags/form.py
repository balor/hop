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
)


def label(body, _for=None, **params):
    if _for:
        params['for'] = _for
    return build_html_object(u'label', body, **params)


def _set_id_and_name(name, params):
    if name:
        params['name'] = name
        if not 'id' in params:
            params['id'] = name
    elif 'id' in params:
        params['name'] = params['id']
    return params


def _set_label(params):
    label_obj = u''
    if 'label' in params:
        label_body = params['label']
        params.pop('label')
        if isinstance(label_body, bool) and label_body:
            label_obj = label(params.get('id'), params['name'])
        else:
            label_obj = label(label_body, params['name'])
    return label_obj, params


def form(action=u'#', method='post', multipart=False, **params):
    if not params.has_key('accept-charset'):
        params['accept-charset'] = u'utf-8'
    if multipart:
        params['enctype'] = u'multipart/form-data'

    params['action'] = action
    params['method'] = method

    return build_html_object_open_tag('form', **params)


def end_form():
    return build_html_object_close_tag('form')


def textarea(name, body=u'', **params):
    params = _set_id_and_name(name, params)
    label_obj, params = _set_label(params)

    txt_area_obj = build_html_object(u'textarea', body, **params)
    return mk_literal(u'{0}{1}'.format(label_obj, txt_area_obj))


def select(name, items=None, selected=None, **params):

    html = list()

    if not items:
        items = list()

    if not isinstance(items, list):
        raise TypeError('items must be an instance of list')

    params = _set_id_and_name(name, params)
    label_obj, params = _set_label(params)

    select_open_tag = build_html_object_open_tag('select', **params) 
    html.append(select_open_tag)

    if items and not isinstance(items[0], tuple):
        temp_items = list()
        for item in items:
            temp_items.append((item, item))
        items = temp_items

    if not selected and items:
        selected = items[0][0]
    selected = sstrip(selected)

    for value, body in items:
        item_params = dict(value=sstrip(value))

        if item_params['value'] == selected:
            item_params['selected'] = u'selected'

        option_obj = build_html_object(u'option', body, **item_params)
        html.append(option_obj)

    html.append(build_html_object_close_tag('select'))
    select_obj = u''.join(html)
    return mk_literal(u'{0}{1}'.format(label_obj, select_obj))


def input_field(type, name=None, value=None, **params):
    params['type'] = type
    params['value'] = value if value else u''

    params = _set_id_and_name(name, params)
    label_obj, params = _set_label(params)

    if type == 'checkbox' and 'checked' in params:
        if params.pop('checked'):
            params['checked'] = u'checked'

    input_obj = build_html_self_closing_object(u'input', **params)
    if type == 'hidden':
        input_obj = build_html_object(
            u'div', input_obj, style=u'display:none;')

    return mk_literal(u'{0}{1}'.format(label_obj, input_obj))


def text(name, value=u'', **params):
    return input_field(
        type = u'text',
        name = name,
        value = sstrip(value),
        **params
    )


def password(name, value=u'', **params):
    return input_field(
        type = u'password',
        name = name,
        value = sstrip(value),
        **params
    )


def file(name, **params):
    return input_field(
        type = u'file',
        name = name,
        **params
    )


def hidden(name, value=u'', **params):
    return input_field(
        type = u'hidden',
        name = name,
        value = sstrip(value),
        **params
    )


def checkbox(name, value=u'true', checked=False, **params):
    if checked:
        params['checked'] = True

    return input_field(
        type = u'checkbox',
        name = name,
        value = sstrip(value),
        **params
    )


def radio(name, value=u'', checked=False, **params):
    return input_field(
        type = u'radio',
        name = name,
        value = value,
        **params
    )


def submit(name, value=None, **params):
    if not value:
        value = name
    return input_field(
        type = u'submit',
        name = name,
        value = value,
        **params
    )
