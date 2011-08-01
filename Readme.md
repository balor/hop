# HTML Object Printer, hop in short

  Hop is a small helpers collection for creating html objects such a hyperlinks, images or forms.

  I've created it while rewriting some webpage from PHP to Python. The one thing that was missing during the development process was a html object printer. So i decided to create a small one, with no dependencies, not related to any framework, KISS'ish etc. Perfect to use with any web-framework, from micros like bottle or fpyf to pylons, pyramid or django.
  Hop is actively maintained and used both in small and big commercial web applications. It's main goal is to bring easy to use html helper library that you can use in any python web projct, without worrying about compatibility or dependencies.

# Installation

  `$ easy_install hop` or `$ pip install hop`

# Documentation

  For now see `tests.py` for a helpers usage.

# Example

  Import hop.tags for direct access to all tags printers:
    
    import hop.tags as h

  then use it in views (for example Mako):

    <html>
        <head>
            ${h.title(u'My website')}
            ${h.charset()}
            ${h.script(u'/javascripts/jquery.js'}}
            ${h.style(u'/style.css'}}
        </head>
        <body>
            <p>${h.a(u'/albums', u'My albums')}</p>
            <p>${h.email(u'my@email.com', u'Mail me!')}</p>
            <div class="form">
                ${h.form(u'/handle/form', multipart=True)}
                    <p>${h.text(u'username')}</p>
                    <p>${h.password(u'password')}</p>
                    <p>${h.file(u'my_file')}</p>
                    <p>${h.radio_list(u'fav_movie', [u'matrix', u'casablanca', u'jasminum'])}</p>
                    <p>${h.checkbox(u'remember_me', checked=True)}</p>
                    <p>${h.submit(u'Submit')}</p>
                ${h.end_form()}
            </div>
            <p>
                <h2>I like:</h2>
                ${h.ul([u'banana', u'apple', u'juice'])}
            </p>
        </body>
    </html>

# To-do

  * Create site-dedicated helper class for even more automatization
  * Create declarative form helper base class and form fields classes
  * More tests
  * More examples!
  * DOCS!

# License

  (The MIT License)

  Copyright (c) 2011 Michał Thoma <michal@balor.pl>

  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
