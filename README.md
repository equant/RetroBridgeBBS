# RetroBridgeBBS
This software runs on your modern PC and acts as a bridge BBS interface. Connect your retro computers to it (via serial) and download software from the internet using a period approriate interface!

# What is it?

_NONE OF THIS WORKS YET_

This software will help you transfer software to your classic Macintosh (e.g. MacOS System 6, 7, 68k Macs, etc) using the serial port.  Very simply, this software runs on a modern host computer, and behaves like a BBS would back in the day.  You connect your Macintosh to the host computer using serial, and then you can download files from online archives (e.g. Macintosh Garden, Mac Repository), and browse message boards (e.g. 68kmla.org).  However, this "BBS" has only one user, you!

Ultimately I would like this software to be useful to Commodore, Apple ][, Tandy, etc users.  But, I'm developing it mostly for my old macs, so it's not there yet.  If you would like to help connect it to online sources for those platforms, please do!

# Instalation

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
