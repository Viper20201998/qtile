#!/bin/sh

killall -9 volumeicon udiskie nm-applet setxkbmap feh picom /usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 numlockx lxqt-powermanagement optimus-manager-qt

# systray battery icon
#cbatticon -u 5 &
# systray volume
volumeicon &
udiskie -t &
nm-applet &
setxkbmap us &
feh --bg-scale /home/viper/fondo.jpg &
picom &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
numlockx on &
lxqt-powermanagement &
optimus-manager-qt &
