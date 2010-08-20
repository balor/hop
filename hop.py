# -*- coding: utf-8 -*-

# Html Object Helper - HOP

__author__ = 'Michał Thoma'

class HOP(object):
    websitePath = ''

    def __init__(self, websitePath='http://localhost/'):
        # TODO: validate the websitePath
        self.websitePath = websitePath

    def a(self, href, body=None, title=None, **params):
        if params.has_key('validate') and params['validate'] == False:
            href = href
            params.pop('validate')
        else:
            href = self._urlValidation(href, True)
            if params.has_key('validate'):
                params.pop('validate')

        if not body:
            body = href
        if not title and not body:
            title = href
        elif not title and body:
            title = body

        params['href'] = href
        params['title'] = title

        return self.buildHtmlObject('a', body, **params);

    def img(self, src, alt=None, **params):
        params['src'] = src
        if alt:
            params['alt'] = alt
        else:
            params['alt'] = self.websitePath
        return self.buildHtmlSelfClosingObject('img', **params)

    def style(self, href):
        href = self._urlValidation(href)
        params = {
            'href':href,
            'rel':'stylesheet',
            'type':'text/css',
        }
        return self.buildHtmlSelfClosingObject('link', **params)

    def script(self, src):
        params = {
            'src':self._urlValidation(src),
            'type':'text/javascript',
        }
        return self.buildHtmlObject('script', '', **params)

    def metaCharset(self, charset='utf8'):
        params = {
            'content':'text/html; charset=%s' % charset,
            'http-equiv':'Content-Type',
        }
        return self.buildHtmlSelfClosingObject('meta', **params)

    def title(self, title=None):
        if not title:
            title = self.websitePath
        return self.buildHtmlObject('title', title)

    def comment(self, comment):
        return '<!-- %s -->' % comment

    def table(self, cells=list(), headers=None, **params):
        if len(cells) < 1 or type(cells[0]) != list or len(cells[0]) < 1:
            return self.buildHtmlObject('table')
        outputHtml = self.buildHtmlObjectOpening('table', **params)
        fixedColumnsNum = params.get('fixedColumnsNum', False)
        if headers:
            columns = len(headers)
            outputHtml += '\n\t'+self.buildHtmlObjectOpening('tr')
            if fixedColumnsNum:
                headers_len = len(headers)
                for header in range(0, fixedColumnsNum):
                    if header < headers_len:
                        content = str(headers[header])
                    else:
                        content = '&nbsp;'

                    outputHtml += self.buildHtmlObject('th', content)
            else:
                for header in headers:
                    outputHtml += self.buildHtmlObject('th', str(header))
            outputHtml += self.buildHtmlObjectClosing('tr')

        if fixedColumnsNum:
            for row in cells:
                outputHtml += '\n\t'+self.buildHtmlObjectOpening('tr')
                row_len = len(row)
                for column in range(0, fixedColumnsNum):
                    if column < row_len:
                        content = str(row[column])
                    else:
                        content = '&nbsp;'

                    outputHtml += self.buildHtmlObject('td', content)
                outputHtml += self.buildHtmlObjectClosing('tr')
        else:
            for row in cells:
                outputHtml += '\n\t'+self.buildHtmlObjectOpening('tr')
                for column in row:
                    outputHtml += self.buildHtmlObject('td', str(column))
                outputHtml += self.buildHtmlObjectClosing('tr')

        outputHtml += '\n'+self.buildHtmlObjectClosing('table')
        return outputHtml

    def list(self, items=list(), listType='ul', **params):
        ''' Item param can be string or list with tuples/lists looking like this:
            [(item1_body, item1_options),(item2_body, item2_options)]'''

        outputHtml = self.buildHtmlObjectOpening(listType, **params)
        for item in items:
            body = '&nbsp;'
            params = dict()
            if type(item) == list or type(item) == tuple:
                item_len = len(item)
                if item_len > 0:
                    body = item[0]
                if item_len > 1:
                    params = item[1]
            elif str(item).strip() != '':
                body = str(item)
            outputHtml += '\n\t'+self.buildHtmlObject('li', body, **params)
        outputHtml += '\n'+self.buildHtmlObjectClosing(listType)
        return outputHtml


    def input(self, **params):
        ''' special params:
                'label':'Label' - creates a label for input

                'textarea':True - trigger input to textarea
                'body':str - for textarea only, textarea body'

                'select':True - trigger input to select
                'tabsize':int - for select only, increase the indent
                'items':list - fot select only, list of select options, example:
                    [{'body':'opt1','value':'val1'},{'body':'opt2,'value':'val2'}]
        '''
        outputHtml = ''
        if params.has_key('label'):
            if params.has_key('id'):
                outputHtml += self.buildHtmlObject('label',
                    params['label'], {'for':params['id']})
            else:
                outputHtml += self.buildHtmlObject('label', params['label'])
            params.pop('label');

        if params.has_key('textarea') and params['textarea']:
            body = ''
            params.pop('textarea')
            if params.has_key('body'):
                body = params['body']
                params.pop('body')
            outputHtml += self.buildHtmlObject('textarea', body, **params)
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
            outputHtml += self.buildHtmlObjectOpening('select', **params)
            if items:
                itemNr = 0
                for item in items:
                    if type(item) == dict:
                        item = dict(item)
                        body = itemNr
                        if item.has_key('body'):
                            body = str(item['body'])
                            item.pop('body')
                        if not item.has_key('value'):
                            item['value'] = body
                        outputHtml += '\n\t' + tabs + self.buildHtmlObject('option', body, **item)
                        itemNr += 1
            outputHtml += '\n' + tabs + self.buildHtmlObjectClosing('select')
        else:
            if params.has_key('body'):
                params.pop('body')
            if params.has_key('type') and params['type']=='hidden':
                outputHtml += self.buildHtmlObject('div',
                    self.buildHtmlSelfClosingObject('input', **params),
                    style='display:none;')
            else:
                outputHtml += self.buildHtmlSelfClosingObject('input', **params)

        return outputHtml

    def beginForm(self, action, method='post', **params):
        if not action:
            action = '/'
        if not params.has_key('accept-charset'):
            params['accept-charset'] = 'utf-8'
        params['action'] = action
        params['method'] = method

        return self.buildHtmlObjectOpening('form', **params)

    def endForm(self):
        return self.buildHtmlObjectClosing('form')

    def autoForm(self, action, fields=[], method='post', uploadForm=False, **params):
        ''' special params:
                'div':False - disable wrapping inputs in divs
        '''
        wrapInputWithDiv = True
        if params.has_key('div') and not params['div']:
            params.pop('div')
            wrapInputWithDiv = False

        if uploadForm:
            params['enctype'] = "multipart/form-data"

        formHtml = self.beginForm(action, method, **params)+'\n'

        for field in fields:
            formHtml += '\t'
            if field.has_key('select') and field['select']:
                field['tabsize'] = 1
            if wrapInputWithDiv:
                formHtml += self.buildHtmlObject('div',
                    self.input(**field), _class='input')
            else:
                formHtml += self.input(**field)
            formHtml += '\n'

        formHtml += self.endForm()
        return formHtml

    def buildHtmlObject(self, objectName, body, **params):
        opening = self.buildHtmlObjectOpening(objectName, **params)
        closing = self.buildHtmlObjectClosing(objectName)
        return opening+body+closing

    def buildHtmlObjectOpening(self, objectName, **params):
        objectString = '<'+self._prepareString(objectName)
        objectString += self._buildHtmlParams(**params)
        return objectString+'>'

    def buildHtmlObjectClosing(self, objectName):
        return '</'+objectName+'>'

    def buildHtmlSelfClosingObject(self, objectName, **params):
        objectString = '<'+self._prepareString(objectName)
        objectString += self._buildHtmlParams(**params)
        return objectString+'/>'

    def encode(self, string):
        return string.encode('ascii', 'xmlcharrefreplace')

    def _buildHtmlParams(self, **params):
        paramsString = ''
        for (name,value) in params.items():
            if name.startswith('_'):
                name = name[1:]
            name = self._prepareString(name)
            value = self._prepareString(value)
            paramsString += ' %s="%s"' % (name, value)

        return paramsString

    def _urlValidation(self, url, specialProtocols=False):
        url = self._prepareString(url)
        validUrlProtocols = [
            'http://',
            'https://',
        ]
        if specialProtocols:
            validUrlProtocols.append('mailto:')
            validUrlProtocols.append('skype:')
            validUrlProtocols.append('#')

        urlHasValidProtocol = False
        for protocol in validUrlProtocols:
            if url.startswith(protocol):
                urlHasValidProtocol = True

        if not urlHasValidProtocol:
            url = self.websitePath+url

        return url

    def _prepareString(self, rawString):
        return str(rawString).strip().strip('"')
