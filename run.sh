#!/bin/bash

MAIN="yinkana.py"

if (( ! "$#")); then
	echo "Uso: $0 host"
	exit 1
fi

# Send all python files in this directory
if scp *.py "$1": > /dev/null; then
	# -u flag forces stdout and stderr of the interpreter to be unbuffered 
	# This is the closed thing we can get to a "live" execution
	ssh "$1" "python3 -u $MAIN" || echo "Command did not execute right"
else
	echo "Error while coying via scp"
fi
