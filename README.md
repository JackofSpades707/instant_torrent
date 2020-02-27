# InstantTorrent ![icon](https://i.imgur.com/fQu32ry.png)

## What is this?
This is a torrent downloading tool, you enter your search query, select a torrent and the program will scrape the magnet link and hand it over to your default torrent application on your PC.
This should be compatible with every OS and torrent client out there, if for some reason your OS/BitTorrent client isn't supported then feel free to open an issue :)

## I Found a bug!
Great! A problem found is a problem solved, Please open an issue and I'll address it as soon as I can :)

## I want a feature!
Great! Feel free to open an issue and I'll tag it as an enhancment :)

## Installation
* pip install instanttorrent (pip3 if needed, python2 is not supported)

## Uninstall
* okay :( just run 'pip uninstall instanttorrent' (might need superuser privileges)

## Usage/Example
$ instanttorrent
![alt tag](http://i.imgur.com/omGYXSZ.png)
Options :

![alt tag](http://i.imgur.com/jTD7Ik1.png)
* -h --help | Displays help
* -q --query | Query to be searched, defaults to prompt you
* -m --max_results | Max results to output, defaults to 10 (Broken, added to TODO)
* -p --proxy | sets proxy, defaults to system proxy
* -s --seeders | hides seeders
* -l --leechers | hides leechers
* -d --date | hides upload date
* --size | hides file size


## TUI
* I may update this to be the default via pip install when I have the time
![TUI List torrents](https://i.imgur.com/uCSss0G.png)
![TUI torrent view](https://i.imgur.com/j7fM4KM.png)

## TODO
* Rewrite max_results
* Support more sites? (maybe an optional flag to switch specify website?)
