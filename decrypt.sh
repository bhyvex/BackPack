#!/bin/bash

if [ -d $1 ]; then
	cd $1
fi

bcrypt *.* < /pass.txt
