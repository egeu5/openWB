#!/bin/bash
. /var/www/html/openWB/openwb.conf
if [[ $evsecon == "dac" ]]; then
	sudo python /var/www/html/openWB/runs/dac.py 1947 $dacregister
fi
if [[ $evsecon == "modbusevse" ]]; then
	sudo python /var/www/html/openWB/runs/evsewritemodbus.py $modbusevsesource $modbusevseid 15
fi
if [[ $debug == "2" ]]; then
	echo "setz ladung auf 15A" >> /var/www/html/openWB/web/lade.log
fi
if [[ $lastmanagement == "1" ]]; then
	if [[ $evsecons1 == "dac" ]]; then
		sudo python /var/www/html/openWB/runs/dac.py 1947 $dacregisters1
	fi

	if [[ $evsecons1 == "modbusevse" ]]; then
		sudo python /var/www/html/openWB/runs/evsewritemodbus.py $evsesources1 $evseids1 15
	fi
fi
echo 15 > /var/www/html/openWB/ramdisk/llsoll
echo 1 > /var/www/html/openWB/ramdisk/ladestatus
