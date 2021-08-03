# blunderboard
random notes

## serial console
https://www.tal.org/tutorials/raspberry-pi-zero-usb-serial-console
`cu -d -l /dev/ttyU0 -s 115200` or equvivalent

## wifi
`sudo rfkill unblock all && sudo reboot`
`sudo raspi-config` or edit /etc/wpa_supplicant/wpa_supplicant.conf

## enable ssh
`systemctl enable ssh`

## blunder definition (lichess)
https://github.com/ornicar/lila/blob/master/modules/analyse/src/main/Advice.scala#L79

## go package zum anflanschen
https://github.com/notnil/chess
