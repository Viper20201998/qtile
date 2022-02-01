# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401

from scripts import storage

import os
import subprocess
from libqtile import qtile
from libqtile import bar, layout, widget, hook
from libqtile.widget import base
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
#from libqtile.utils import guess_terminal

# default variables
mod = "mod4"
home_dir = os.path.expanduser("~")
terminal = f"alacritty --config-file {home_dir}/.config/qtile/alacritty/alacritty.yml"
keys = [Key(key[0], key[1], *key[2:]) for key in [
    # ------------ Window Configs ------------

    # Switch between windows in current stack pane
    ([mod], "Down", lazy.layout.down()),
    ([mod], "Up", lazy.layout.up()),
    ([mod], "Left", lazy.layout.left()),
    ([mod], "Right", lazy.layout.right()),

    # Change window sizes (MonadTall)
    ([mod, "shift"], "Right", lazy.layout.grow()),
    ([mod, "shift"], "Left", lazy.layout.shrink()),

    # Toggle floating
    ([mod, "shift"], "f", lazy.window.toggle_floating()),

    # Move windows up or down in current stack
    ([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    ([mod, "shift"], "Up", lazy.layout.shuffle_up()),

    # Toggle between different layouts as defined below
    ([mod], "Tab", lazy.next_layout()),
    ([mod, "shift"], "Tab", lazy.prev_layout()),

    # Kill window
    ([mod], "w", lazy.window.kill()),

    # Switch focus of monitors
    ([mod], "period", lazy.next_screen()),
    ([mod], "comma", lazy.prev_screen()),

    # Restart Qtile
    ([mod, "control"], "r", lazy.restart()),

    ([mod, "control"], "q", lazy.shutdown()),
    ([mod], "r", lazy.spawncmd()),

    # ------------ App Configs ------------

    # Menu
    ([mod], "m", lazy.spawn("rofi -show drun")),

    # Discord
    ([mod], "d", lazy.spawn("discord")),

    # Window Nav
    ([mod, "shift"], "m", lazy.spawn("rofi -show")),

    # Browser
    ([mod], "g", lazy.spawn("google-chrome-stable")),

    # File Explorer
    ([mod], "e", lazy.spawn("pcmanfm")),

    # Terminal
    ([mod], "Return", lazy.spawn("alacritty")),

    #Vmware
    ([mod], "v", lazy.spawn("vmware")),

    # Redshift
    ([mod], "r", lazy.spawn("redshift -O 2400")),
    ([mod, "shift"], "r", lazy.spawn("redshift -x")),

    # screenshot
    ([mod], "s", lazy.spawn("scrot")),
    ([mod, "shift"], "s", lazy.spawn("scrot -s /home/viper/")),
#    ("Print", lazy.spawn("xfce4-screenshooter")),

    # ------------ Hardware Configs ------------

    # Volume
    ([], "XF86AudioLowerVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ -5%"
    )),
    ([], "XF86AudioRaiseVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ +5%"
    )),
    ([], "XF86AudioMute", lazy.spawn(
        "pactl set-sink-mute @DEFAULT_SINK@ toggle"
    )),

    # Brightness
    ([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    ([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),
]]

# custom workspace names and initialization
class Groupings:

    def init_group_names(self):
        return [("", {"layout": "monadtall"}),     # Terminals
                ("", {"layout": "monadtall"}),     # Web Browser
                ("", {"layout": "monadtall"}),     # File Manager
                ("", {"layout": "monadtall"}),     # Text Editor
                ("", {"layout": "monadtall"}),
                ("", {"layout": "monadtall"}),     # Media
                ("", {"layout": "monadtall"}),     # Music/Audio
                ("漣", {"layout": "monadtall"})]    # Settings

    def init_groups(self):
        return [Group(name, **kwargs) for name, kwargs in group_names]


if __name__ in ["config", "__main__"]:
    group_names = Groupings().init_group_names()
    groups = Groupings().init_groups()

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group

##### DEFAULT THEME SETTINGS FOR LAYOUTS #####
layout_theme = {"border_width": 3,
                "margin": 10,
                "font": "Source Code Pro Medium",
                "font_size": 10,
                "border_focus": "#82dbf4",
                "border_normal": "#0F131F"
                }

# window layouts
layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Floating(**layout_theme),
    # Try more layouts by unleashing below layouts.
    # layout.Columns(**layout_theme),
    # layout.Stack(num_stacks=2),
    # layout.Bsp(**layout_theme),
    # layout.Matrix(**layout_theme),
    # layout.MonadWide(**layout_theme),
    # layout.RatioTile(**layout_theme),
    # layout.Tile(**layout_theme),
    # layout.TreeTab(**layout_theme),
    # layout.VerticalTile(**layout_theme),
    # layout.Zoomy(**layout_theme),
]


# colors for the bar/widgets/panel
def init_colors():
    return [["#0F131F", "#0F131F"], # color 0 | bg
            ["#0F131F", "#0F131F"], # color 1 | bg
            ["#82dbf4", "#82dbf4"], # color 2 | fg
            ["#F7A01D", "#F7A01D"], # color 3 | red
            ["#F7A11D", "#F7A11D"], # color 4 | green
            ["#1A6897", "#1A6897"], # color 5 | yellow
            ["#548FAB", "#548FAB"], # color 6 | blue
            ["#1798E5", "#1798E5"], # color 7 | magenta
            ["#16B0F7", "#16B0F7"], # color 8 | cyan
            ["#82dbf4", "#82dbf4"]] # color 9 | white

def init_separator():
    return widget.Sep(
                size_percent = 60,
                margin = 5,
                linewidth = 1,
                background = colors[1],
                foreground = colors[8])

def nerd_icon(nerdfont_icon, fg_color):
    return widget.TextBox(
                font = "Iosevka Nerd Font",
                fontsize = 15,
                text = nerdfont_icon,
                foreground = fg_color,
                background = colors[1])

def init_edge_spacer():
    return widget.Spacer(
                length = 0,
                background = colors[1])


colors = init_colors()
sep = init_separator()
space = init_edge_spacer()

widget_defaults = dict(
    font='Source Code Pro Medium',
    fontsize=12,
    padding=5,
)
extension_defaults = widget_defaults.copy()


def init_widgets_list():
    widgets_list = [
            # Left Side of the bar

            
            #widget.Image(
            #    filename = "/usr/share/pixmaps/archlinux-logo.png",
            #    background = colors[1],
            #    margin = 3
            #),   
            widget.GroupBox(
                font = "Iosevka Nerd Font",
                fontsize = 15,
                foreground = colors[2],
                background = colors[1],
                borderwidth = 8,
                highlight_method = "text",
                this_current_screen_border = colors[5],
                active = colors[4],
                inactive = colors[2]
            ),
            nerd_icon(
                "   ",
                colors[2]
            ),
            widget.Battery(
                foreground = colors[2],
                background = colors[1],
                format = "{percent:2.0%}"
            ),
            widget.Spacer(
                length = bar.STRETCH,
                background = colors[1]
            ),

            # Center bar

            nerd_icon(
                " ",
                colors[2]
            ),
            widget.CurrentLayout(
                foreground = colors[2],
                background = colors[1]
            ),
            
            nerd_icon(
                "﬙",
                colors[2]
            ),
            widget.CPU(
                format = "{load_percent}%",
                foreground = colors[2],
                background = colors[1],
                update_interval = 2,
                mouse_callbacks = {
                    'Button1': lambda : qtile.cmd_spawn(f"{terminal} -e gtop")
                }
            ),
            nerd_icon(
                "",
                colors[2]
            ),
            widget.Memory(
                format = "{MemUsed:.0f}{mm}",
                foreground = colors[2],
                background = colors[1],
                update_interval = 2,
                mouse_callbacks = {
                    'Button1': lambda : qtile.cmd_spawn(f"{terminal} -e gtop")
                }
            ),
            nerd_icon(
                " ",
                colors[2]
            ),
            widget.GenPollText(
                foreground = colors[2],
                background = colors[1],
                update_interval = 5,
                func = lambda: storage.diskspace('FreeSpace'),
                mouse_callbacks = {
                    'Button1': lambda : qtile.cmd_spawn(f"{terminal} -e gtop")
                }
            ),
            nerd_icon(
                " ",
                colors[2]
            ),
            widget.GenPollText(
                foreground = colors[2],
                background = colors[1],
                update_interval = 5,
                func = lambda: subprocess.check_output(f"{home_dir}/.config/qtile/scripts/num-installed-pkgs").decode("utf-8")
            ),

            # Left Side of the bar

            widget.Spacer(
                length = bar.STRETCH,
                background = colors[1]
            ),
            nerd_icon(
                " ",
                colors[2]
            ),
            widget.Net(
                format = "{down} ↓↑ {up}",
                foreground = colors[2],
                background = colors[1],
                update_interval = 2,
                mouse_callbacks = {
                    'Button1': lambda : qtile.cmd_spawn(f"{terminal} -e iwctl")
                }
            ),
            nerd_icon(
                " ",
                colors[2]
            ),
            widget.Clock(
                format = '%b %d-%Y',
                foreground = colors[2],
                background = colors[1]
            ),
            nerd_icon(
                " ",
                colors[2]
            ),
            widget.Clock(
                format = '%I:%M:%S %p',
                foreground = colors[2],
                background = colors[1]
            ),
            sep,
            widget.Systray(
                    padding = 15,
                    background = colors[1]
            )
        ]
    return widgets_list


# screens/bar
def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_list(), size=35, opacity=0.9, margin=[1,10,0,10]))]

screens = init_screens()

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

#
# assign apps to groups/workspace
#
@hook.subscribe.client_new
def assign_app_group(client):
    d = {}

    # assign deez apps
    d[group_names[0][0]] = ['Alacritty', 'xfce4-terminal']
    d[group_names[1][0]] = ['google-chrome', 'discord', 'brave-browser', 'midori', 'qutebrowser']
    d[group_names[2][0]] = ['pcmanfm', 'thunar']
    d[group_names[3][0]] = ['code', 'geany']
    d[group_names[4][0]] = ['android-studio', 'jetbrains-studio']
    d[group_names[5][0]] = ['vlc', 'obs', 'mpv', 'mplayer', 'lxmusic', 'gimp']
    d[group_names[6][0]] = ['spotify']
    d[group_names[7][0]] = ['lxappearance', 'gpartedbin', 'lxtask', 'lxrandr', 'arandr', 'pavucontrol', 'xfce4-settings-manager']

    wm_class = client.window.get_wm_class()[0]
    for i in range(len(d)):
        if wm_class in list(d.values())[i]:
            group = list(d.keys())[i]
            client.togroup(group)
            client.group.cmd_toscreen(toggle=False)


main = None
@hook.subscribe.startup
def start_once():
    start_script = os.path.expanduser("~/.config/qtile/scripts/autostart.sh")
    subprocess.call([start_script])

@hook.subscribe.startup_once
def start_always():
    # fixes the cursor
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])


dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(wm_class='Viewnior'),  # Photos/Viewnior 
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
], **layout_theme)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
