#! /bin/bash

if [ -n "$1" ]; then 
	if [ $1="flush" ]; then
		rm -rf ./tmp
		rm -rf ./training
		rm pwc-disp.log
	fi
fi

python ./train.py 2>&1 | tee pwc-disp.log
