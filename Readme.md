# HTML Object Printer, HOP in short

  HOP is a small helper class for creating html objects souch a hyperlinks, images or forms.

  I've created it while rewriting some webpage from PHP (dead-simple inline scripts) to Python (Bottle + SqlAlchemy). 
  The one thing that was missing during the development process was some html object printer. So i decided to create a small helper class, with no dependencies, not related to any framework, KISS'ish etc. Perfect to use with any simple web-framework like bottle or fpyf.
  It works well also with frameworks like Pylons or Django (supporting thier auto-escape filters).

# Installation

  Just add the `hop.py` file to your project and use it!

# Examples!


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
