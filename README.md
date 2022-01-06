# dskmgr

Two dimensional, dynamic desktop/workspace manager for bspwm.

# Description

Dskmgr handles bspwm operations such as creating new desktops, focusing desktops and moving around based on directions. For example, it can allow your desktop layout to look like this:

```
[0-2]       [2-2]
[0-1]       [2-1] [3-1]
[0-0] [1-0] [2-0] [3-0]
```

Where each number pair is a unique desktop, and you can navigate around in 4 directions. The program also remembers you vertical position's history, so if you were in `[0-1]` and moved right to `1-0`, when you will move left again you will return to `[0-1]` rather than `[0-0]`.

## Install

```
python3 -m pip install dskmgr
```

## Usage

Put `dskmgrd &` in you `bspwmrc`, and then change you desktop-managing shortcuts to use `dskmgr` rather than `bspc`.


## TODOs

* Add a subscribe command (like `bspc subscribe`).

* Add proper tests.

* Make it so that when an error occurs (or even when an incorrect command is revieved) the `dskmgr` script will know to return an error code.

* Improve logging support in `dskmgrd`.

* Find a better name (maybe "meja"? It means "desk" in Indonesian)