# HTML Object Printer, HOP in short

  HOP is a small helper class for creating html objects souch a hyperlinks, images or forms.

  I've created it while rewriting some webpage from PHP (dead-simple inline scripts) to Python (Bottle + SQLAlchemy). 
  The one thing that was missing during the development process was a html object printer. So i decided to create a small one, with no dependencies, not related to any framework, KISS'ish etc. Perfect to use with any web-framework, from micros like bottle or fpyf to pylons, pyramid or django.
  HOP is actively maintained and used both in small and big commercial web applications. It's main goal is to bring easy to use html helper library that you can use in any python web projct, without worrying about compatibility or dependencies.

# Installation

  Just add the `hop.py` file to your project and use it!

# Example

  Import HOP and create new instance which will be passed to views:

    from hop import HOP

    hop = HOP(website_name=u'MySite.com')

  then use it in views (for example Mako):

    <html>
        <head>
            ${hop.title()}
            ${hop.charset()}
            ${hop.script(u'/javascripts/jquery.js'}}
            ${hop.style(u'/style.css'}}
        </head>
        <body>
            <p>${hop.a(u'/albums', u'My albums')}</p>
            <p>${hop.emial(u'my@email.com', u'Mail me!')}</p>
            <div class="form">
                ${hop.form(u'/handle/form', multipart=True)}
                    <p>${hop.text(u'username')}</p>
                    <p>${hop.password(u'password')}</p>
                    <p>${hop.checkbox(u'remember_me', checked=True)}</p>
                    <p>${hop.submit(u'Submit')}</p>
                ${hop.end_form()}
            </div>
            <p>
                <h2>I like:</h2>
                ${hop.list([u'banana', u'apple', u'juice'])}
            </p>
        </body>
    </html>

# License

  (The MIT License)

  Copyright (c) 2011 Michał Thoma <michal@balor.pl>

  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
