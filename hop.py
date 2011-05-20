# -*- coding: utf-8 -*-
'''
HTML Object Printer, HOP in short
Helper for rendering safe html objects with ease

Version 1.1

Author: Michał Thoma
Authors website: http://balor.pl
'''

__author__ = u'Michał Thoma'
__version__ = '1.1.0'

class Literal(unicode):
    tag = u''

    def __init__(self, tag):
        self.tag = tag

    def __html__(self):
        return self.tag

    def __str__(self):
        return self.tag

def mk_literal(html):
    return Literal(html)

EMPTY = u''

try:
    from markupsafe import escape_silent as escape
except ImportError:
    try:
        import markupsafe
        def escape(s):
            if s is None:
                return EMPTY
            return markupsafe.escape(s)
    except ImportError:
        def escape(s):
            if s is None:
                return EMPTY
            if hasattr(s, '__html__'):
                return s
            s = s.replace('\n', '')
            s = s.replace('\r', '')
            s = s.replace('<', '&lt;')
            s = s.replace('>', '&gt;')
            s = s.replace('"', '&#34;')
            return s

class HOP(object):
    website_path = ''
    form_fields_num = 0

    def __init__(self, website_path='/', website_name=None):
        if website_path[len(website_path)-1] != '/':
            website_path = '%s/' % website_path
        self.website_path = website_path
        self.website_name = website_name

    def url(self, url=''):
        return self._url_validation(url)

    def a(self, href, body=None, title=None, **params):
        if params.has_key('validate') and params['validate'] == False:
            href = href
            params.pop('validate')
        else:
            href = self._url_validation(href, True)
            if params.has_key('validate'):
                params.pop('validate')

        if not body:
            body = self.safestr(href)
        if title == None:
            title = self.safestr(body)

        params['href'] = href
        params['title'] = title

        if title == False:
            params.pop('title')

        return self.build_html_object('a', body, **params)

    def email(self, email, body=None, title=None, **params):
        href = 'mailto:%s' % email
        return self.a(href, body, title, **params)

    def img(self, src, alt=None, **params):
        params['src'] = src
        if alt:
            params['alt'] = alt
        elif self.website_name:
            params['alt'] = self.website_name
        else:
            params['alt'] = ''
        return self.build_html_self_closing_object('img', **params)

    def style(self, href):
        href = self._url_validation(href)
        params = {
            'href':href,
            'rel':'stylesheet',
            'type':'text/css',
        }
        return self.build_html_self_closing_object('link', **params)

    def script(self, src):
        params = {
            'src':self._url_validation(src),
            'type':'text/javascript',
        }
        return self.build_html_object('script', '', **params)

    def meta_charset(self, charset='utf8'):
        params = {
            'content':'text/html; charset=%s' % charset,
            'http-equiv':'Content-Type',
        }
        return self.build_html_self_closing_object('meta', **params)

    def charset(self, charset='utf8'):
        return self.meta_charset(charset)

    def title(self, title=None):
        if not title:
            if self.website_name:
                title = self.website_name
            elif self.website_path:
                title = self.website_path
            else:
                title = 'My Homepage'
        return self.build_html_object('title', title)

    def comment(self, comment):
        return '<!-- %s -->' % comment

    def table(self, cells=list(), headers=None, **params):
        if ((len(cells) < 1 or
             type(cells[0]) != list or 
             len(cells[0]) < 1
            ) and not headers):
            return self.build_html_object('table', '')
        out_html = [
            self.build_html_object_open_tag('table', **params)
        ]
        fixed_columns_num = params.get('fixed_columns_num', False)
        if headers:
            columns = len(headers)
            out_html.append(u'\n\t%s' % self.build_html_object_open_tag('tr'))
            if fixed_columns_num:
                headers_len = len(headers)
                for header in range(0, fixed_columns_num):
                    if header < headers_len:
                        content = self._str(headers[header])
                    else:
                        content = '&nbsp;'

                    out_html.append(self.build_html_object('th', content))
            else:
                for header in headers:
                    out_html.append(self.build_html_object(
                        'th', self._str(header)))
            out_html.append(self.build_html_object_close_tag('tr'))

        if fixed_columns_num:
            for row in cells:
                out_html.append(u'\n\t'+self.build_html_object_open_tag('tr'))
                row_len = len(row)
                for column in range(0, fixed_columns_num):
                    if column < row_len:
                        content = row[column]
                    else:
                        content = '&nbsp;'

                    out_html.append(self.build_html_object('td', content))
                out_html.append(self.build_html_object_close_tag('tr'))
        else:
            for row in cells:
                tr_params = dict()
                tds = list()
                for column in row:
                    if isinstance(column, dict):
                        if 'tr' in column:
                            tr_params = column['tr']
                    else:
                        td_params = dict()
                        if isinstance(column, tuple):
                            td_params = column[1]
                            column = column[0]
                        tds.append(self.build_html_object(
                            'td', column, **td_params))
                out_html.append(
                    u'\n\t%s%s%s' % (
                        self.build_html_object_open_tag('tr', **tr_params),
                        u''.join(tds),
                        self.build_html_object_close_tag('tr')
                    )
                )

        out_html.append(u'\n%s' % self.build_html_object_close_tag('table'))
        return mk_literal(u''.join(out_html))

    def list(self, items=list(), list_type='ul', **params):
        '''
        Item param can be string or list
            with tuples/lists looking like this:

            [(item1_body, item1_options),(item2_body, item2_options)]
        '''
        out_html = [
            self.build_html_object_open_tag(list_type, **params),
        ]
        for item in items:
            body = '&nbsp;'
            params = dict()
            if type(item) == list or type(item) == tuple:
                item_len = len(item)
                if item_len > 0:
                    body = item[0]
                if item_len > 1:
                    params = item[1]
            elif self._str(item).strip() != '':
                body = self._str(item)
            out_html.append('\n\t%s' % self.build_html_object(
                'li', body, **params))
        out_html.append('\n%s' % self.build_html_object_close_tag(list_type))
        return ''.join(out_html)

    def text(self, name, value='', **params):
        return self.input(
            name = name,
            type = 'text',
            value = self._str(value),
            **params
        )

    def password(self, name, value='', **params):
        return self.input(
            name = name,
            type = 'password',
            value = self._str(value),
            **params
        )

    def file(self, name, **params):
        return self.input(
            name = name,
            type = 'file',
            **params
        )

    def hidden(self, name, value='', **params):
        return self.input(
            name = name,
            type = 'hidden',
            value = self._str(value),
            **params
        )

    def textarea(self, name, body='', **params):
        return self.input(
            name = name,
            textarea = True,
            body = body,
            **params
        )

    def checkbox(self, name, value='true', checked=False, **params):
        if not 'id' in params:
            params['id'] = name

        return self.input(
            name = name,
            type = 'checkbox',
            value = self._str(value),
            checked = checked,
            **params
        )

    def select(self, name, items, selected=None, **params):
        if not isinstance(items, list):
            raise TypeError('items must be an list')
        if items:
            if not isinstance(items[0], tuple):
                temp_items = list()
                for item in items:
                    stringyfied_item = self._str(item)
                    temp_items.append((stringyfied_item, stringyfied_item))
                items = temp_items
        return self.input(
            name = name,
            select = True,
            items = items,
            selected = selected,
            **params
        )

    def radio(self, name, value, checked=False, **params):
        if checked:
            params['checked'] = 'checked'
        return self.input(
            name = name,
            value = value,
            type = 'radio',
            **params
        )

    def submit(self, name, value=None, **params):
        if not value:
            value = name
        return self.input(
            name = name,
            type = 'submit',
            value = value,
            **params
        )

    def input(self, **params):
        '''
        Creates HTML form input

        special params:

                'label':'Label' - creates a label for input

        special objects:

                [TEXTAREA]
                'textarea':True - trigger input to textarea
                'body':str - textarea body

                [SELECT]
                'select':True - trigger input to select
                'selected':str - value of option that is selected by default
                'tabsize':int - increase the indent
                'items':list - list of select options: [(val, body), (val, body)]
        '''
        out_html = list()
        
        if not 'name' in params:
            params['name'] = params['id']

        if params.has_key('label'):
            out_html.append(self.build_html_object(
                'label', params['label'], _for=params['id']))
            params.pop('label')

        if params.has_key('textarea') and params['textarea']:
            body = ''
            params.pop('textarea')

            if params.has_key('body'):
                body = params['body']
                params.pop('body')
            out_html.append(self.build_html_object('textarea', body, **params))

        elif params.has_key('select') and params['select']:
            params.pop('select')
            items = False
            tabs = ''

            if params.has_key('items'):
                items = params['items']
                params.pop('items')

            if params.has_key('tabsize'):
                tabs = params['tabsize'] * '\t'
                params.pop('tabsize')
            out_html.append(self.build_html_object_open_tag('select', **params))

            if items:
                selected_val = self._str(params.pop('selected', items[0][0]))
                for value, body in items:
                    item_params = {
                        'value':value,
                    }
                    if value == selected_val:
                        item_params['selected'] = 'selected'
                    out_html.append(
                        u'\n\t%s%s' % (
                            tabs,
                            self.build_html_object(
                                'option', body, **item_params),
                        )
                    )
            out_html.append(
                '\n%s%s' % (
                    tabs,
                    self.build_html_object_close_tag('select'),
                )
            )
        else:
            if params.has_key('body'):
                params.pop('body')

            if (params.has_key('type') and
                params['type'] == 'checkbox' and
                params.has_key('checked')):
                chd = params['checked']
                if chd:
                    params['checked'] = 'checked'
                else:
                    params.pop('checked')

            if params.has_key('type') and params['type'] == 'hidden':
                out_html.append(self.build_html_object(
                    'div',
                    self.build_html_self_closing_object('input', **params),
                    style = 'display:none;'
                ))
            else:
                out_html.append(self.build_html_self_closing_object(
                    'input', **params))

        self.form_fields_num += 1
        return mk_literal(u''.join(out_html))

    def form(self, action, method='post', multipart=False, **params):
        if not action:
            action = '/'
        if not params.has_key('accept-charset'):
            params['accept-charset'] = 'utf-8'
        if multipart:
            params['enctype'] = 'multipart/form-data'
        params['action'] = action
        params['method'] = method

        self.form_fields_num = 1
        return self.build_html_object_open_tag('form', **params)

    def end_form(self):
        self.form_fields_num = 1
        return self.build_html_object_close_tag('form')

    def auto_form(self, action, fields=[], method='post',
                  upload_form=False, **params):
        '''
        special **params:
            'div':False - disable wrapping inputs in divs
        '''
        wrap_input_with_div = True
        if params.has_key('div') and not params['div']:
            params.pop('div')
            wrap_input_with_div = False

        form_html_code = [
            '%s\n' % self.form(action, method, upload_form, **params),
        ]

        for field in fields:
            if field.has_key('select') and field['select']:
                field['tabsize'] = 1
            if wrap_input_with_div:
                form_chunk = self.build_html_object('div',
                    self.input(**field), _class='input')
            else:
                form_chunk = self.input(**field)
            form_html_code.append('\t%s\n' % form_chunk)

        form_html_code.append(self.end_form())
        return form_html_code

    def build_html_object(self, object_name, body, **params):
        return mk_literal(u''.join([
            self.build_html_object_open_tag(object_name, **params),
            escape(body),
            self.build_html_object_close_tag(object_name),
        ]))

    def build_html_object_open_tag(self, object_name, **params):
        return mk_literal(u'<%s%s>' % (
            self._str(escape(object_name)),
            self._build_html_params(**params),
        ))

    def build_html_object_close_tag(self, object_name):
        return mk_literal(u'</%s>' % self._str(escape(object_name)))

    def build_html_self_closing_object(self, object_name, **params):
        return mk_literal(u'<%s%s />' % (
            self._str(escape(object_name)),
            self._build_html_params(**params),
        ))

    def encode(self, string):
        return string.encode('ascii', 'xmlcharrefreplace')

    def safestr(self, string):
        return (string.
            replace('&', '&amp;').
            replace('"', '&quot;').
            replace('<', '&lt;').
            replace('>', '&gt;')
        )

    def _build_html_params(self, **params):
        params_list = list()
        for (name, value) in params.items():
            if name[0] == '_':
                name = name[1:]
            params_list.append(u' %s="%s"' % (
                escape(name), 
                escape(value),
            ))
        return u''.join(params_list)

    def _url_validation(self, url, special_protocols=False):
        url = self._str(url)
        valid_url_protocols = [
            u'http://',
            u'https://',
        ]
        if special_protocols:
            valid_url_protocols.extend([
                u'mailto:',
                u'skype:',
                u'#',
            ])
        url_has_valid_protocol = False
        for protocol in valid_url_protocols:
            if url.startswith(protocol):
                url_has_valid_protocol = True

        if not url_has_valid_protocol and self.website_path:
            if url and url[0] == '/':
                url = url[1:]
            url = '%s%s' % (self.website_path, url)
        return url

    def _str(self, raw_str):
        if not isinstance(raw_str, basestring):
            raw_str = str(raw_str)
        return raw_str.strip().strip('"')
