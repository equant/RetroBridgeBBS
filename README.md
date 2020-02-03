<!--
[![HitCount](http://hits.dwyl.io/equant/RetroBridgeBBS.svg)](http://hits.dwyl.io/equant/RetroBridgeBBS)
-->

# RetroBridgeBBS
This software runs on your modern PC and acts as a bridge BBS interface. Connect your retro computers to it (via serial) and download software from the internet using a period approriate interface!

# What is it?

_This software is still in development, not everything is implemented, but it is useful as is._

This software will help you transfer software to your classic Macintosh (e.g.
MacOS System 6, 7, 68k Macs, etc) using the serial port.  Very simply, this
software runs on a modern host computer, and behaves like a BBS would back in
the day.  You connect your Macintosh to the host computer using serial, and
then, using your vintage computer, you can search and download files from
online archives (e.g. Macintosh Garden, Mac Repository).  However, this "BBS"
has only one user, you!

# Motivation

I've written this software to do what I want.  It might not make sense to some
people.  I've lost interest in getting my _____ computer "connected" to the
internet.  I like the BBS interface.  It's fun to use my old computer and
search for files.  I find it incredibly useful to see that a .sit file is not a
pre-5.5 before I go through the trouble of getting it on my System 6 Mac only
to find out I can't uncompress it.  Yes it's slow to do modem transfers
(although it's fast if you download disk images), but it like to dawdle and
play with other things while I wait; it builds excitement.

Ultimately I would like this software to be useful to Commodore, Apple ][,
Tandy, etc users.  But, I'm developing it mostly for my old macs, so it's not
there yet.  If you would like to help connect it to online sources for those
platforms, please do!

Some day I'd like to add web based message board browsing (such as [http://68kmla.com/forums]) to the RetroBridgeBBS.

## Features

_Some of this is implemented, some is not_

* Search and download files from supported online archives
    * Supported archives:
        * Macintosh Garden [http://www.macintoshgarden.org/]
* .SIT algorithm identification 
    * Examines headers of compressed .SIT files _before_ you download them and lets you know if they use early (pre 5.5) or later StuffIt algorithms so you don't download something you can't uncompress on an old Macintosh.
* Transfer files to your retro computer
    * Serial connection using X/Y/ZModem transfers
    * Write disk images to a floppy drive ❌
* Upload files from your retro computer
* Supports multiple connections.
    * Console
    * Telnet
    * Serial
* Setup profiles for different machines. ❌
* Automatic uncompress and recompress of files to compatible formats. ❌


| Icon | Description |
| ---  | ---         |
❌ | not implemented
🚨 | implemented but I broke it, should be fixed soon.

# Installation

## Requirements

For this to be useful, you are expected to have:

1. A host computer with python 3 _and_ a serial port.
2. A Macintosh with some form of terminal software (e.g. ZTerm, QuickLink)
3. A null modem cable to connect the Macintosh and the host PC.
4. Linux command line transfer tools: sz, sx and sb (for ZMODEM, XMODEM and YMODEM)

## Getting things running

### Steps you may need to do
```bash
git clone https://github.com/equant/RetroBridgeBBS
sudo pip install pyserial
sudo pip install beautifulsoup4
```

### Starting the bbs
```bash
cd RetroBridgeBBS
python -i start_bbs.py
```

### Logging in

You can log in on the console after starting the bbs.  Or you can connect via a serial device.  Or you can telnet.

```
telnet localhost 3030
```


# Mac Serial Tips and Notes

## Claris Works

You may find Claris Works installed on your Macintosh.  Claris Works as modem/terminal software built in to it, and can be used for XMODEM transfers


## AppleTalk

"Serial device unavailable" type errors...

You may need to turn off AppleTalk on your Macintosh in order to get your terminal software to work.  For Powerbooks with a single serial port this may be especially important.  To turn off AppleTalk, go to the apple menu (upper left) and select 'chooser'.  Then turn off AppleTalk.  You probably have to restart.  That was the case for my PowerBook 3400c running System 9.
