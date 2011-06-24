class HOP(object):

    def __init__(self, website_path='/', website_name=None):
        if website_path[len(website_path)-1] != '/':
            website_path = u'{0}/'.format(website_path)
        self.website_path = website_path
        self.website_name = website_name
        self.form_fields_num = 0

    def url(self, url=''):
        return validate_url(url)

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
            tr_obj = u'\n\t{0}'.format(self.build_html_object_open_tag('tr'))
            out_html.append(tr_obj)
            if fixed_columns_num:
                headers_len = len(headers)
                for header in range(0, fixed_columns_num):
                    if header < headers_len:
                        content = sstrip(headers[header])
                    else:
                        content = '&nbsp;'

                    out_html.append(self.build_html_object('th', content))
            else:
                for header in headers:
                    out_html.append(self.build_html_object(
                        'th', sstrip(header)))
            out_html.append(self.build_html_object_close_tag('tr'))

        if fixed_columns_num:
            for row in cells:
                tr_obj = u'\n\t{0}'.format(
                    self.build_html_object_open_tag('tr'))
                out_html.append(tr_obj)
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
            u'{0}\n'.format(self.form(action, method, upload_form, **params)),
        ]

        for field in fields:
            if field.get('select'):
                field['tabsize'] = 1

            if not 'type' in field:
                field['type'] = 'text'

            div_attrs = dict()
            if 'div_attrs' in field:
                div_attrs = field.pop('div_attrs')

            if 'class' in div_attrs:
                div_attrs['_class'] = div_attrs.pop('class')

            div_attrs['_class'] = '{0} input_field {1}_input_field'.format(
                    div_attrs.get('_class', ''), field['type'])
            
            if wrap_input_with_div:
                form_chunk = self.build_html_object('div',
                    self.input(**field), **div_attrs)
            else:
                form_chunk = self.input(**field)
            form_html_code.append(u'\t{0}\n'.format(form_chunk))

        form_html_code.append(self.end_form())
        return u''.join(form_html_code)
