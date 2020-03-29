#!/usr/bin/env python

import os
import re
import urwid
import requests
import pyperclip
from bs4 import BeautifulSoup
from argparse import ArgumentParser


def get(url, proxies):
    if proxies is None:
        proxies = {
            'http': os.environ.get("HTTP_PROXY"),
            'https': os.environ.get("HTTPS_PROXY"),
            'ftp': os.environ.get("FTP_PROXY")
        }
    else:
        proxies = {
            'http': 'http://{}'.format(proxies),
            'https': 'https://{}'.format(proxies),
            'ftp': 'ftp://{}'.format(proxies)
        }
    return requests.get(url, proxies=proxies)

def parse_args():
    #TODO: How will the user define the sort method?
    parser = ArgumentParser()
    parser.add_argument('-q', '--query', help='query to be searched', type=str, default=None)
    parser.add_argument('-p', '--proxy', help='proxy to access TPB', type=str, default=None)
    parser.add_argument('-s', '--sort', help='sort method seeders/leechers/date/size', default='seeders', type=str)
    return parser.parse_args()

def make_torrent_dict(title, seeders, leechers, catagory, date, size, mgnt_uri, source):
    return {
        'title': title,
        'seeders': seeders,
        'leechers': leechers,
        'catagory': catagory,
        'date': date,
        'size': size,
        'mgnt_uri': mgnt_uri,
        'source': source
    }

def sort_torrents(torrents, key='seeders', descending_order=True):
    '''
    takes a list of dicts and sorts them by the key

    :param torrents: list of torrent dicts
    :param key: the key to sort the list of dicts by
    '''
    #TODO: fix size sorting
    valid_keys = ['seeders', 'leechers', 'date', 'size']
    if key not in valid_keys:
        print("Invalid key: {}".format(key))
        raise KeyError
    return sorted(torrents, key=lambda torrent: torrent[key], reverse=descending_order)

def open_torrent(button, mgnt_uri):
    if os.name == 'nt': # windows
        os.startfile(mgnt_uri)
    else:
        from subprocess import call
        call(['xdg-open', mgnt_uri])

def thepiratebay(query, proxies=None):
    '''
    parses html output into an array of dicts
    '''
    url = "https://thepiratebay.org/search/{}".format(query)
    r = get(url, proxies)
    results = []
    html = BeautifulSoup(r.content, 'html.parser').findAll('tr')
    for tag in html:
        try:
            title = tag.find(class_='detName').find('a').get_text().strip()
            for i in tag.findAll('a'):
                if 'magnet' in i['href']:
                    mgnt_uri = i['href']
            catagory = '{} - {}'.format(tag.get_text().split()[0], tag.get_text().split()[1]).rstrip(')').replace('(', '')
            seeders = int(tag.findAll('td')[-2:][0].get_text().strip())
            leechers = int(tag.findAll('td')[-2:][1].get_text().strip())
            date = tag.find(class_='detDesc').get_text()
            date = date.split(',')[0].replace('Uploaded ', '').strip()
            size = tag.find(class_='detDesc').get_text()
            size = re.search(r'Size [0-9]+.[0-9]+....', size).group().replace('Size ', '').strip()
            results.append(make_torrent_dict(title, seeders, leechers, catagory, date, size, mgnt_uri, 'TPB'))
        except AttributeError:
            pass
    return results

def kickasstorrents(query, proxies=None):
    '''
    parses html output into an array of dicts
    '''
    results = []
    for i in range(10):
        url = "https://katcr.co/katsearch/page/{}/{}".format(i, query.replace(' ', '%20'))
        r = get(url, proxies)
        html = BeautifulSoup(r.content, 'html.parser').findAll('tr')
        for tag in html:
            try:
                title = tag.find(class_="torrents_table__torrent_title").text.strip()
                mgnt_uri = tag.findAll(class_="button button--small")[1]['href']
                catagory = tag.find(class_="text--muted").text.strip()
                size = tag.findAll(class_='text--nowrap text--center')[0].text
                date = tag.findAll(class_='text--nowrap text--center')[2].text
                seeders = int(tag.find(class_='text--nowrap text--center text--success').text)
                leechers = int(tag.find(class_='text--nowrap text--center text--error').text)
                results.append(make_torrent_dict(title, seeders, leechers, catagory, date, size, mgnt_uri, 'KAT'))
            except AttributeError:
                pass
    return results


def TUI_torrents_list(torrents):
    body = [urwid.Text("InstantTorrent", align='center'), urwid.Divider()]
    for torrent in torrents:
        button = urwid.Button(torrent['title'])
        urwid.connect_signal(button, 'click', TUI_torrent_chosen, torrent)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def TUI_torrent_chosen(button, torrent):
    response = [urwid.Text(
        [
            'Title: {}\n\n'.format(torrent['title']),
            'Seeders: {}\n'.format(torrent['seeders']),
            'Leechers: {}\n'.format(torrent['leechers']),
            'Catagory: {}\n'.format(torrent['catagory']),
            'Upload Date: {}\n'.format(torrent['date']),
            'Size: {}\n'.format(torrent['size']),
            'Source: {}\n'.format(torrent['source'])
        ]
    ), urwid.Divider()]
    copy = urwid.Button('Copy Magnet URI to clipboard')
    urwid.connect_signal(copy, 'click', copy_magnet_uri, torrent) # works

    download = urwid.Button('Download Torrent')
    urwid.connect_signal(download, 'click', open_torrent, torrent)

    back = urwid.Button('Back')
    urwid.connect_signal(back, 'click', TUI_back_button)

    quit = urwid.Button('Quit')
    urwid.connect_signal(quit, 'click', TUI_exit_program)
    buttons = [copy, download, back, quit]
    for button in buttons:
        response.append(urwid.AttrMap(button, None, focus_map='reversed'))
    main.original_widget = urwid.Filler(urwid.Pile(response))

def TUI_exit_program(button):
    raise urwid.ExitMainLoop()

def TUI_exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

def copy_magnet_uri(button, torrent):
    pyperclip.copy(torrent['mgnt_uri'])

def TUI_back_button(button):
    main.original_widget = urwid.Padding(TUI_torrents_list(torrents), left=2, right=2)

# def TUI_prompt_user():
#     txt = urwid.Text("Enter your search query")
#     prompt = urwid.Edit(u'')
#     button = urwid.Button('Search')
#     urwid.connect_signal(button, 'click', TUI_torrents_list, torrents)
#     div = urwid.Divider()
#     pile = urwid.Pile([txt, div, prompt, button])
#     # top = urwid.Filler(pile, valign='top')
#     main.original_widget = urwid.Padding(pile, left=2, right=2)
#     # urwid.MainLoop(top, unhandled_input=TUI_exit_on_q).run()
#     query = prompt.get_text()[0].strip()
#     return query


if __name__ == '__main__':
    # README: probably a good idea to convert all TUI_* functions into a class,
    # I may come back and do this if I keep messing with the urwid library
    # This program was always  intended for educational purposes so I may abandon it
    args = parse_args()
    torrents = []
    if args.query is None:
        # TODO: Replace this with erwid
        args.query = input("Enter your search query\n>_ ").strip()
    torrents += thepiratebay(args.query, args.proxy)
    torrents += kickasstorrents(args.query, args.proxy)
    torrents = sort_torrents(torrents, key=args.sort)
    # output(torrents)
    main = urwid.Padding(TUI_torrents_list(torrents), left=2, right=2)
    top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                        align='center', width=('relative', 80),
                        valign='middle', height=('relative', 80),
                        min_width=20, min_height=9)
    urwid.MainLoop(top, palette=[('reversed', 'standout', '')], unhandled_input=TUI_exit_on_q).run()
