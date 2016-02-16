# ZoeyBot - A Python IRC Bot

### Intro

ZoeyBot is a faithful little companion IRC bot written in Python. It does not use any of the IRC libraries available for Python. Instead, lower level networking libraries are used to directly send and receive packets to servers. This makes it a very flexible bot, which can be extended to work with systems that implement their own versions of the IRC protocol, such as Twitch chat and Slack.

### Usage

Configure by editing the file `zoey` on the top level directory.
Once done, `chmod +x zoey` and run it with `./zoey`.

For Windows you might have to use run `zoey` from Python IDLE or use `python zoey` at the command prompt.

License information and changelog can be found on the top level directory, under `LICENSE.txt` and `changelog.txt` respectively.

### Release details

* Version:        0.0.3
* Written by:     Phixyn (http://phixyn.com/blog)
* Date started:   31/03/2012
* Last release:   16/02/2016
* Current stage:  Alpha

Developed with `Python 2.7` _(currently being ported to `Python 3` as part of v1.0.0 milestone)._

### Documentation

Documentation can be found in `doc/` folder. Open `index.html` on an internet browser to see the contents. You will find a list of commands and more.

For developers/contributors there is also a set of technical documentation. Please note that this is still not fully complete and a lot of code documentation is missing.

See also `doc/to-do.txt` if you're willing to help with new features and bug fixes!

### More coming soon

This project hasn't been worked on since 2014, finally being resurrected in February 2016. A lot more exciting features are on the way!
