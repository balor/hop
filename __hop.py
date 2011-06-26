class HOP(object):

    def __init__(self, website_path='/', website_name=None):
        if website_path[len(website_path)-1] != '/':
            website_path = u'{0}/'.format(website_path)
        self.website_path = website_path
        self.website_name = website_name
        self.form_fields_num = 0

    def url(self, url=''):
        return validate_url(url)

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
