#!/bin/sh

# https://github.com/OnionIoT/Onion-Console/blob/master/www/apps/onion-settings/onion-settings-general.html
uci set system.@system[0].timezone="MSK-3"
uci set system.@system[0].zonename="Moscow, St. Petersburg, Volgograd"
uci commit system
