#!/bin/sh
# 
# This script will host commands shortened into functions as to avoid all that annyoying typing in the command line.

declare -A commands_and_desc
commands_and_desc["nd_test_app"]="nd_test_app appname.path.to.test.method"

help(){
    printf '\n\n\n\033[92mThe newsline project management commands:\n'
	for i in "${!commands_and_desc[@]}"
	do
	  printf "\n\t  \033[1m\033[94m$i\033[0m : \033[95m${commands_and_desc[$i]}\033[0m \n"
	done
	printf "\n\n\n"
}

# No database test runner
nd_test_app(){
	if [ ! -z "$1" -a "$1" != " " ]; then
  		eval "python3 manage.py test newsline.apps.$1 --testrunner=newsline.scripts.no_db_test_runner.NoDbTestRunner"
	else
		echo "You have to specify the test path [without using newsline.apps.]";
	fi	
}
$@