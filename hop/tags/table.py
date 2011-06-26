# -*- coding: utf-8 -*-

from ..builder import (
    build_html_object,
    build_html_object_close_tag,
    build_html_object_open_tag,
)
from ..utils import (
    mk_literal,
    sstrip,
)


def _cells_iterator(row, columns_num=None):
    if not columns_num:
        for cell in row:
            yield cell
    else:
        row_len = len(row)
        for x in range(columns_num):
            if x < row_len:
                yield row[x]
            else:
                yield mk_literal(u'&nbsp;')


def table(cells, headers=None, **params):
    headers_are_invalid = bool(headers and not isinstance(headers, list))
    if not isinstance(cells, list) or headers_are_invalid:
        raise TypeError('Cells and headers must be a valid list object')

    out_html = list()

    fixed_columns_num = False
    if 'fixed_columns_num' in params:
        fixed_columns_num = int(params.pop('fixed_columns_num'))

    out_html.append(build_html_object_open_tag(u'table', **params))

    if headers:
        out_html.append(build_html_object_open_tag(u'tr'))

        for header in _cells_iterator(headers, fixed_columns_num):
            out_html.append(build_html_object(u'th', header))

        out_html.append(build_html_object_close_tag(u'tr'))

    for row in cells:
        tr_params = dict()
        tds = list()

        for cell in _cells_iterator(row, fixed_columns_num):
            if isinstance(cell, dict):
                if 'tr' in cell:
                    tr_params = cell['tr']
            else:
                td_params = dict()
                if isinstance(cell, tuple):
                    cell = cell[0]
                    td_params = cell[1]
                td_obj = build_html_object(u'td', cell, **td_params)
                tds.append(td_obj)

        tr_opening = build_html_object_open_tag(u'tr', **tr_params)
        tr_closing = build_html_object_close_tag(u'tr')
        row_html = u''.join(tds)
        out_html.append(u'{0}{1}{2}'.format(tr_opening, row_html, tr_closing))

    out_html.append(build_html_object_close_tag(u'table'))

    return mk_literal(u''.join(out_html))


def fixed_col_table(cells, columns_num, headers=None, **params):
    params['fixed_columns_num'] = columns_num
    return table(cells, headers, **params)
