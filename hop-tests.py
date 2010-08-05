#!/usr/bin/python
import hop
# -*- coding: utf-8 -*-

from hop import HOP

hop = HOP('http://hop.com/')

print '\nDifferent tags tests:'
print hop.title()
print hop.title('Html object helper')
print hop.style('main.css')
print hop.script('jquery.js')
print hop.metaCharset()

print '\nA-tag tests:'
print hop.a('balor.pl')
print hop.a('skype:balor')
print hop.a('https://balor.pl/index.php', 'Moja strona domowa!')
print hop.a('https://balor.pl/index.php', 'Moja strona domowa!', 'Wiesz ze mnie chcesz',
    {'style':'color:red;font-weight:bold', 'onclick':'showTitle();end();'})

print '\nImg-tag tests:'
print hop.img('balor.pl/logo.png')
print hop.img('balor.pl/logo.png', "Logo balor.pl")
print hop.img('balor.pl/logo.png', "Logo balor.pl",
    {'style':'color:red;font-weight:bold', 'onclick':'showTitle();end();'})

print '\nForm object tests:'
print hop.beginForm('do.cgi')
print hop.input({'type':'hidden', 'name':'id', 'value':'4'})
print hop.input({'type':'submit', 'value':'Delete'})
print hop.endForm()


print '\nAutoForm tests:'
print hop.autoForm('logme.php', (
    {'type':'text', 'name':'username'},
    {'type':'text', 'name':'pass'},
    {'textarea':True, 'body':'pass custom text here'},
    {'type':'hidden', 'name':'spy', 'value':'im so secret!'},
    {'type':'submit', 'value':'Log in'}
), {'id':'myCleanForm'})
