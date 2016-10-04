#!/bin/bash

pip install -r requirements.txt

echo 'would you like to install the man page? [1/2]'
select yn in "Yes" "No"; do
	case $yn in
		Yes ) echo 'installing man page'; install -g 0 -o 0 -m 0644 instantrom.1 /usr/share/man/man1; gzip /usr/share/man/man1/instantrom.1 ; break;; 
		No ) exit;;
	esac
echo 'done';
done
