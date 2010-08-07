# -*- coding: utf-8 -*-

# Html Object Helper - HOP

class HOP(object):
    websitePath = ''

    def __init__(self, websitePath='http://localhost/'):
        # TODO: validate the websitePath
        self.websitePath = websitePath

    def a(self, href, body=None, title=None, options=dict()):
        if not type(options) == dict:
            options = dict()

        if options.has_key('validate') and options['validate'] == False:
            href = href
            options.pop('validate')
        else:
            href = self._urlValidation(href, True)
            if options.has_key('validate'):
                options.pop('validate')

        if not body:
            body = href
        if not title and not body:
            title = href
        elif not title and body:
            title = body

        options['href'] = href
        options['title'] = title

        return self.buildHtmlObject('a', body, options);

    def img(self, src, alt=None, options=dict()):
        if not type(options) == dict:
            options = dict()
        options['src'] = src
        if alt:
            options['alt'] = alt
        else:
            options['alt'] = self.websitePath
        return self.buildHtmlSelfClosingObject('img', options)

    def style(self, href):
        href = self._urlValidation(href)
        options = {
            'href':href,
            'rel':'stylesheet',
            'type':'text/css',
        }
        return self.buildHtmlSelfClosingObject('link', options)

    def script(self, src):
        options = {
            'src':self._urlValidation(src),
            'type':'text/javascript',
        }
        return self.buildHtmlObject('script', '', options)

    def metaCharset(self, charset='utf8'):
        options = {
            'content':'text/html; charset=utf-8',
            'http-equiv':'Content-Type',
        }
        return self.buildHtmlSelfClosingObject('meta', options)

    def title(self, title=None):
        if not title:
            title = self.websitePath
        return self.buildHtmlObject('title', title)

    def table(self, cells=list(), headers=None, options=dict(), fixedColumnsNum=None):
        if len(cells) < 1 or type(cells[0]) != list or len(cells[0]) < 1:
            return self.buildHtmlObject('table')
        outputHtml = self.buildHtmlObjectOpening('table', options)
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

    def list(list=list(), type='ul'):
        pass


    def input(self, options=dict()):
        ''' special options:
                'textarea':True - trigger input to textarea
                'select':True - trigger input to select
                'label':'Label' - creates a label for input
        '''

        '''
        TODO: implement select object
        <select name="data[User][business_type]" id="UserBusinessType">
            <option value=""></option>
            <option value="0">Firma</option>
            <option value="1" selected="selected">Osoba fizyczna</option>
        </select>
        '''

        inputHtml = ''
        if options.has_key('label'):
            if options.has_key('id'):
                inputHtml += self.buildHtmlObject('label',
                    options['label'], {'for':options['id']})
            else:
                inputHtml += self.buildHtmlObject('label', options['label'])
            options.pop('label');

        if options.has_key('textarea') and options['textarea']:
            body = ''
            options.pop('textarea')
            if options.has_key('body'):
                body = options['body']
                options.pop('body')
            inputHtml += self.buildHtmlObject('textarea', body, options)
        else:
            if options.has_key('body'):
                options.pop('body')
            if options.has_key('type') and options['type']=='hidden':
                inputHtml += self.buildHtmlObject('div',
                    self.buildHtmlSelfClosingObject('input', options),
                    {'style':'display:none;'})
            else:
                inputHtml += self.buildHtmlSelfClosingObject('input', options)

        return inputHtml

    def beginForm(self, action, options=dict(), method='post', charset='utf-8'):
        if not action:
            action = '/'
        if not options.has_key('accept-charset'):
            options['accept-charset'] = charset
        options['action'] = action
        options['method'] = method

        return self.buildHtmlObjectOpening('form', options)

    def endForm(self):
        return self.buildHtmlObjectClosing('form')

    def autoForm(self, action, fields=list(), options=dict(), method='post', uploadForm=False):
        ''' special options:
                'div':False - disable wrapping inputs in divs
        '''
        wrapInputWithDiv = True
        if options.has_key('div') and not options['div']:
            options.pop('div')
            wrapInputWithDiv = False

        if uploadForm:
            options['enctype'] = "multipart/form-data"

        formHtml = self.beginForm(action, options, method)+'\n'

        for field in fields:
            formHtml += '\t'
            if wrapInputWithDiv:
                formHtml += self.buildHtmlObject('div',
                    self.input(field), {'class':'input'})
            else:
                formHtml += self.input(field)
            formHtml += '\n'

        formHtml += self.endForm()
        return formHtml

    def buildHtmlObject(self, objectName, body, options=dict()):
        opening = self.buildHtmlObjectOpening(objectName, options)
        closing = self.buildHtmlObjectClosing(objectName)
        return opening+body+closing

    def buildHtmlObjectOpening(self, objectName, options=dict()):
        objectString = '<'+self._prepareString(objectName)
        objectString += self._buildHtmlOptions(options)
        return objectString+'>'

    def buildHtmlObjectClosing(self, objectName):
        return '</'+objectName+'>'

    def buildHtmlSelfClosingObject(self, objectName, options=dict()):
        objectString = '<'+self._prepareString(objectName)
        objectString += self._buildHtmlOptions(options)
        return objectString+'/>'

    def encode(self, string):
        return string.encode('ascii', 'xmlcharrefreplace')

    def _buildHtmlOptions(self, options):
        if not options or type(options) != dict:
            return ''

        optionsString = ''
        for (name,value) in options.items():
            name = self._prepareString(name)
            value = self._prepareString(value)
            optionsString += ' '+name+'="'+value+'"'

        return optionsString

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
