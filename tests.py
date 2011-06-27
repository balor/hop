# -*- coding: utf-8 -*-

import unittest

import hop.tags as hop


class TagsTests(unittest.TestCase):

    def test_a_tag(self):

        html = u'<a href="http://balor.pl" title="http://balor.pl">http://balor.pl</a>'
        self.assertEqual(hop.a(u'http://balor.pl'), html)

        html = u'<a href="http://balor.pl" title="http://balor.pl">http://balor.pl</a>'
        self.assertEqual(hop.a(u'    http://balor.pl \n\n\n\t'), html)

        html = u'<a href="http://balor.pl" title="balor website">balor website</a>'
        self.assertEqual(hop.a(u'http://balor.pl', u'balor website'), html) 

        html = u'<a href="http://balor.pl" title="balor website">http://balor.pl</a>'
        self.assertEqual(hop.a(u'http://balor.pl', title=u'balor website'), html)

        html = u'<a title="balor website" style="color:red;" href="http://balor.pl" id="ganja" class="myLink">BALOR</a>'
        self.assertEqual(hop.a(u'http://balor.pl', u'BALOR', u'balor website', _class=u'myLink', id=u'ganja', style=u'color:red;'), html)
        
        html = u'<a href="http://balor.pl" title="http://balor.pl">http://balor.pl</a>'
        self.assertEqual(hop.a(u'balor.pl', validate_url=True), html)


    def test_email_alias(self):

        html = u'<a href="mailto:fake@balor.pl" title="Mail to fake@balor.pl">fake@balor.pl</a>'
        self.assertEqual(hop.email(u'fake@balor.pl'), html)


    def test_img_tag(self):

        html = u'<img src="http://balor.pl/picture.png" alt="" />'
        self.assertEqual(hop.img(u'http://balor.pl/picture.png'), html)

        html = u'<img src="http://balor.pl/picture.png" alt="" />'
        self.assertEqual(hop.img(u'\t  http://balor.pl/picture.png  '), html)

        html = u'<img src="/picture.png" alt="My picture" />'
        self.assertEqual(hop.img(u'/picture.png', alt=u'My picture'), html)

        html = u'<img src="/picture.png" alt="My picture" class="thePicture" />'
        self.assertEqual(hop.img(u'/picture.png', alt=u'My picture', _class=u'thePicture'), html)


    def test_script_tag(self):

        html = u'<script src="/jquery.js" type="text/javascript"></script>'
        self.assertEqual(hop.script(u'/jquery.js'), html)

        html = u'<script src="http://balor.pl/jquery.js" type="text/javascript"></script>'
        self.assertEqual(hop.script(u'http://balor.pl/jquery.js', validate_url=True), html)

        html = u'<script src="http://balor.pl/jquery.js" type="text/javascript"></script>'
        self.assertEqual(hop.script(u'balor.pl/jquery.js', validate_url=True), html)


    def test_style_tag(self):

        html = u'<link href="http://balor.pl/my.css" type="text/css" rel="stylesheet" />'
        self.assertEqual(hop.style(u'http://balor.pl/my.css'), html)


    def test_meta_charser_tag(self):

        html = u'<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />'
        self.assertEqual(hop.charset(), html)


    def test_title_tag(self):

        html = u'<title>Balors cave</title>'
        self.assertEqual(hop.title(u'Balors cave'), html)


    def test_comment_tag(self):

        html = u'<!-- rage age -->'
        self.assertEqual(hop.comment(u'rage age'), html)


    def test_list_tag(self):

        data = [
            u'Apple',
            u'Microsoft',
            u'Oracle',
            u'VMWare',
        ]

        html = u'<ul><li>Apple</li><li>Microsoft</li><li>Oracle</li><li>VMWare</li></ul>'
        self.assertEqual(hop.ul(data), html)

        html = u'<ol><li>Apple</li><li>Microsoft</li><li>Oracle</li><li>VMWare</li></ol>'
        self.assertEqual(hop.ol(data), html)


    def test_form_tag(self):

        html = u'<form action="#" accept-charset="utf-8" method="post">'
        self.assertEqual(hop.form(), html)

        html = u'<form action="/trolling/hard.php" accept-charset="utf-8" method="post" enctype="multipart/form-data">'
        self.assertEqual(hop.form(u'/trolling/hard.php', multipart=True), html)

        html = u'<form action="http://balor.pl/process/form" accept-charset="utf-8" class="EineKleineForm" method="get">'
        self.assertEqual(hop.form(u'http://balor.pl/process/form', u'get', _class=u'EineKleineForm'), html)


    def test_end_form_tag(self):

        html = u'</form>'
        self.assertEqual(hop.end_form(), html)

    
    def test_textarea_tag(self):

        html = u'<textarea name="ta" id="ta">This is content</textarea>'
        self.assertEqual(hop.textarea(u'ta', u'This is content'), html)

        html = u'<textarea class="beauty" name="my_textarea" id="my_textarea">Content</textarea>'
        self.assertEqual(hop.textarea(u'my_textarea', u'Content', _class=u'beauty'), html)


    def test_select_tag(self):

        data = [
            u'Apple',
            u'Microsoft',
            u'Oracle',
            u'VMWare',
        ]
        html = u'<select name="my_select" id="my_select"><option selected="selected" value="Apple">Apple</option><option value="Microsoft">Microsoft</option><option value="Oracle">Oracle</option><option value="VMWare">VMWare</option></select>'
        self.assertEqual(hop.select(u'my_select', data), html)

        data = [
            (1, u'Apple'),
            (2, u'Microsoft'),
            (3, u'Oracle'),
            (4, u'VMWare'),
        ]
        html = u'<select name="my_select" id="my_select"><option selected="selected" value="1">Apple</option><option value="2">Microsoft</option><option value="3">Oracle</option><option value="4">VMWare</option></select>'
        self.assertEqual(hop.select(u'my_select', data), html)

        data = [
            (1, u'Apple'),
            (2, u'Microsoft'),
            (3, u'Oracle'),
            (4, u'VMWare'),
        ]
        html = u'<select class="my_selector" name="tech_companies" id="tech_companies"><option value="1">Apple</option><option value="2">Microsoft</option><option selected="selected" value="3">Oracle</option><option value="4">VMWare</option></select>'
        self.assertEqual(hop.select(u'tech_companies', data, 3, _class=u'my_selector'), html)

        data = [
            (1, u'Apple'),
            (2, u'Microsoft'),
            (3, u'Oracle'),
            (4, u'VMWare'),
        ]
        html = u'<label for="tech_companies">tech_companies</label><select class="my_selector" id="tech_companies" name="tech_companies"><option value="1">Apple</option><option value="2">Microsoft</option><option selected="selected" value="3">Oracle</option><option value="4">VMWare</option></select>'
        self.assertEqual(hop.select(u'tech_companies', data, 3, _class=u'my_selector', label=True), html)


    def test_input_field_tag(self):

        html = u'<input type="text" value="" />'
        self.assertEqual(hop.input_field(u'text'), html)

        html = u'<input checked="checked" name="omni_auth" value="true" class="checkers" type="checkbox" id="omni_auth" />'
        self.assertEqual(hop.input_field(u'checkbox', u'omni_auth', u'true', checked=True, _class=u'checkers'), html)

        html = u'<div style="display:none;"><input type="hidden" name="nightmare" value="1" id="nightmare" /></div>'
        self.assertEqual(hop.input_field(u'hidden', u'nightmare', u'1'), html)

        html = u'<label for="nightmare">nightmare</label><input type="text" id="nightmare" value="" name="nightmare" />'
        self.assertEqual(hop.input_field(u'text', u'nightmare', label=True), html)

        html = u'<label for="nightmare">The low night mare:</label><input type="text" id="nightmare" value="" name="nightmare" />'
        self.assertEqual(hop.input_field(u'text', u'nightmare', label=u'The low night mare:'), html)


    def test_text_field_tag(self):

        html = u'<input type="text" name="movie" value="nothing hill" id="movie" />'
        self.assertEqual(hop.text(u'movie', u'nothing hill'), html)

        html = u'<input style="color: red;" type="text" name="movie" value="nothing hill" id="movie" />'
        self.assertEqual(hop.text(u'movie', u'nothing hill', style='color: red;'), html)


    def test_password_field_tag(self):
        
        html = u'<input type="password" name="movie" value="" id="movie" />'
        self.assertEqual(hop.password(u'movie'), html)

        html = u'<input style="color: red;" type="password" name="movie" value="" id="movie" />'
        self.assertEqual(hop.password(u'movie', style='color: red;'), html)


    def test_file_field_tag(self):

        html = u'<input class="file_input" type="file" name="myfile" value="" id="myfile" />'
        self.assertEqual(hop.file(u'myfile', _class=u'file_input'), html)


    def test_hidden_field_tag(self):

        html = u'<label for="secret">My secret is somewhere here...</label><div style="display:none;"><input type="hidden" id="secret" value="" name="secret" /></div>'
        self.assertEqual(hop.hidden(u'secret', label=u'My secret is somewhere here...'), html)


    def test_checkbox_field_tag(self):

        html = u'<input type="checkbox" name="remember_me" value="true" id="remember_me" />'
        self.assertEqual(hop.checkbox(u'remember_me'), html)

        html = u'<input type="checkbox" checked="checked" name="remember_me" value="true" id="remember_me" />'
        self.assertEqual(hop.checkbox(u'remember_me', checked=True), html)

        html = u'<input type="checkbox" checked="checked" name="remember_me" value="please_yeah" id="remember_me" />'
        self.assertEqual(hop.checkbox(u'remember_me', u'please_yeah', checked=True), html)


    def test_radio_field_tag(self):

        html = u'<input type="radio" name="use_power" value="" id="use_power" />'
        self.assertEqual(hop.radio(u'use_power'), html)

        html = u'<label for="use_power">use_power</label><input type="radio" id="use_power" value="1" name="use_power" />'
        self.assertEqual(hop.radio(u'use_power', 1, label=True), html)


    def test_submit_field_tag(self):

        html = u'<input type="submit" name="Log me in" value="Log me in" id="Log me in" />'
        self.assertEqual(hop.submit(u'Log me in'), html)


    def test_table(self):

        headers = [u'corp', u'market share', u'flaship product']
        cells = [
            [u'Microsoft', u'80%', u'Microsoft Windows'],
            [u'Apple', u'12%', u'iPhone'],
            [u'Oracle', u'63%', u'Oracle db'],
        ]

        html = u'<table><tr><th>corp</th><th>market share</th><th>flaship product</th></tr><tr><td>Microsoft</td><td>80%</td><td>Microsoft Windows</td></tr><tr><td>Apple</td><td>12%</td><td>iPhone</td></tr><tr><td>Oracle</td><td>63%</td><td>Oracle db</td></tr></table>'
        self.assertEqual(hop.table(cells, headers), html)

        html = u'<table><tr><th>corp</th></tr><tr><td>Microsoft</td></tr><tr><td>Apple</td></tr><tr><td>Oracle</td></tr></table>'
        self.assertEqual(hop.fixed_col_table(cells, 1, headers), html)

        html = u'<table><tr><th>corp</th><th>market share</th><th>flaship product</th><th>&nbsp;</th><th>&nbsp;</th><th>&nbsp;</th></tr><tr><td>Microsoft</td><td>80%</td><td>Microsoft Windows</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr><tr><td>Apple</td><td>12%</td><td>iPhone</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></table>'
        self.assertEqual(hop.fixed_col_table(cells[:2], 6, headers), html)


if __name__ == '__main__':
    unittest.main()

