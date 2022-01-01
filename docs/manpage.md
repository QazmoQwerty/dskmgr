% DSKMGR(1) Dskmgr 0.0.1
% Shalev Don Meiri
% January 1, 2022

# NAME

dskmgr - Two dimensional, dynamic desktop/workspace manager for bspwm

# SYNOPSIS

dskmgrd [-h|-v|--wm *WINDOW_MANAGER*]

dskmgr COMMAND [*OPTIONS*]

# DESCRIPTION

Dskmgr handles bspwm operations such as creating new desktops, focusing desktops and moving around based on directions. For example, it can allow your desktop layout to look like this:

```
[0-2]       [2-2]
[0-1]       [2-1] [3-1]
[0-0] [1-0] [2-0] [3-0]
```

Where each number pair is a unique desktop, and you can navigate around in 4 directions. The program also remembers you vertical position's history, so if you were in `[0-1]` and moved right to `1-0`, when you will move left again you will return to `[0-1]` rather than `[0-0]`.

# DSKMGRD

Dskmgr runs as a daemon (`dskmgrd`), and is controlled through `dskmgr` which communicates with the daemon through a socket.

-h, \--help
:   Show help message

-v, \--verbose
:   Enable verbose output

\--wm
:   Set which window manager `dskmgrd` will control.
    Default is 'bspwm'.

# DSKMGR

`dskmgr` controls the `dskmgrd` daemon by communication with it through a socket.

reset NUM_GROUPS
:   Reset the desktops layouts such that there will be `NUM_GROUPS` groups of size=1.

new-x
:   Creates a new desktop at the maximum possible horizontal position.

new-y [GROUP_INDEX]
:   Creates a new desktop at the maximum possible vertical position in the specified group.
    Default group is the currently focused group.

dump
:   Dump the current state of `dskmgrd` to json.

move (up|down|left|right)
:   Focus desktop in the specified direction.

goto GROUP_INDEX
:   Focus the currently focused desktop in the specified group.


# SEE ALSO

Source code can be found here: 
<https://github.com/QazmoQwerty/dskmgr>
