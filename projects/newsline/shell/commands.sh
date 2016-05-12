#!/bin/sh
# 
# This script will host commands shortened into functions as to avoid all that annyoying typing in the command line.

# No database test runner
nd_test_app(){
	if [ ! -z "$1" -a "$1" != " " ]; then
  		eval "python3 manage.py test newsline.apps.$1 --testrunner=newsline.scripts.no_db_test_runner.NoDbTestRunner"
	else
		echo "You have to specify the test path [without using newsline.apps.]";
	fi	
}
$@