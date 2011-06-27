# -*- coding: utf-8 -*-

from constants import (
    EMPTY,
    SPECIAL_URL_PROTOCOLS,
    URL_PROTOCOLS,
)

try:
    from markupsafe import escape_silent as escape
except ImportError:
    try:
        import markupsafe
        def escape(string):
            if string is None:
                return EMPTY
            return markupsafe.escape(string)
    except ImportError:
        def escape(string):
            if string is None:
                return EMPTY
            if hasattr(string, '__html__'):
                return string
            return (string.
                replace(u'\n', u'').
                replace(u'\r', u'').
                replace(u'<', u'&lt;').
                replace(u'>', u'&gt;').
                replace(u'"', u'&#34;'))


class Literal(unicode):
    '''
    Literal class represents the unicode string
    not intented for html-escapeing.

    This object is designed to fit to the auto-escaping
    mechanisms used in pylons, pyramid, mako etc...
    '''
    tag = u''

    def __init__(self, tag):
        self.tag = tag

    def __html__(self):
        return self.tag

    def __str__(self):
        return self.tag


def mk_literal(html):
    '''
    Returns a new instance of Literal class based on given html string.

    Params:
        html - unicode string
    '''
    return Literal(html)


def sstrip(obj):
    '''
    Small function converting any non-string objects to
    string, removing all double-quotes from it and
    stripping it from whitespaces from beginning and end.

    Params:
        obj - object to be stringyfied and stripper
    '''
    if not isinstance(obj, basestring):
        obj = str(obj)
    return obj.strip().strip('"')


def safestr(string):
    '''
    Escapes all xml non-safe characters in string.

    Params:
        string - string that will be escaped
    '''
    return (string.
        replace(u'&', u'&amp;').
        replace(u'"', u'&quot;').
        replace(u'<', u'&lt;').
        replace(u'>', u'&gt;'))


def validate_url(url, special_protocols=False, base_path=None):
    '''
    Safe strips the url and validates its protocol.
    
    Examples:
        >> validate_url(u'http://www.example.com')
        u'http://www.example.com'

        >> validate_url(u'\thttp://www.example.com   ')
        u'http://www.example.com'

        >> validate_url(u'example.com  ')
        u'http://example.com'

        >> validate_url(u'/users/sign_in', base_path='http://example.com')
        u'http://example.com/users/sign_in'

        >> validate_url(u'gg:123123123', True, 'http://example.com')
        u'gg:123123123'

    Params:
        url - string containing a url
        special_protocols - use special protocols (False by default)
        base_path - path used on auto-completing the url
    '''
    url = sstrip(url)
    valid_url_protocols = URL_PROTOCOLS
    if special_protocols:
        valid_url_protocols.extend(SPECIAL_URL_PROTOCOLS)

    url_has_valid_protocol = False
    for protocol in valid_url_protocols:
        if url.startswith(protocol):
            url_has_valid_protocol = True

    if url_has_valid_protocol:
        return url

    url = url[1:] if url and url[0] == '/' else url
    if base_path:
        base_path = base_path[:-1] if base_path[-1] == '/'  else base_path
        url = u'{0}{1}'.format(base_path, url)
    else:
        url = u'http://{0}'.format(url)

    return url
