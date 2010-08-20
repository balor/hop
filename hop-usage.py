#!/usr/bin/python
import hop
# -*- coding: utf-8 -*-

from hop import HOP

# hop object creation for site http://hop.com
hop = HOP('http://hop.com/')

# Some head tags
print hop.title()
print hop.title('Html object helper')
print hop.style('main.css')
print hop.script('jquery.js')
print hop.metaCharset()

# A-tag
print hop.a('balor.pl')
print hop.a('skype:balor')
print hop.a('https://balor.pl/index.php', 'Moja strona domowa!')
print hop.a('https://balor.pl/index.php', 'Moja strona domowa!', 'Wiesz ze mnie chcesz', style='color:red;font-weight:bold', onclick='showTitle();end();')

# IMG-tag
print hop.img('balor.pl/logo.png')
print hop.img('balor.pl/logo.png', "Logo balor.pl")
print hop.img('balor.pl/logo.png', "Logo balor.pl", style='color:red;font-weight:bold', onclick='showTitle();end();')

# comment
print hop.comment('You don\'t see me! Oh, you do..')

# tables
headers = ['Animals', 'Fruits', 'Operating Systems']
cells = [
    ['Leopard', 'Apple', 'Mac Os X'],
    ['Penguin', 'Lemon', 'GNU/Linux'],
    ['Cow', 'Potato', 'Windows'],
]
print hop.table(cells, headers)
print hop.table(cells, headers, id='table_with_fixed_colnr', fixedColumnsNum=2)
print hop.table(cells, headers, id='another_table_with_fixed_colnr', fixedColumnsNum=5)

# lists
listContent = [
    'Cow',
    ('Chicken', {'class':'bird'}),
    'Lion',
    ('Pidgeon', {'class':'bird'}),
]
print hop.list(listContent)
print hop.list(listContent, 'ol')

# forms objects
selectItems = [
    {'body':'apple'},
    {'body':'banana', 'value':'custom'},
    {'body':'pineapple', 'class':'indent'},
    {'body':'grapefruit'},
]
print hop.beginForm('do.cgi')
print hop.input(type='hidden', name='id', value='4')
print hop.input(select=True, items=selectItems)
print hop.input(type='submit', value='Delete')
print hop.endForm()

# automatic forms
print hop.autoForm('logme.php', (
    {'type':'text', 'name':'username'},
    {'type':'text', 'name':'pass'},
    {'textarea':True, 'body':'pass custom text here'},
    {'select':True, 'items':selectItems, 'class':'nice_select', 'id':'fruits'},
    {'type':'hidden', 'name':'spy', 'value':'im so secret!'},
    {'type':'submit', 'value':'Log in'}
), {'id':'myCleanForm'})
