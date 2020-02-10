#!/usr/bin/env bash
SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`

## checkout project
function project {
    if [ $# -lt 1 ]; then
        echo "Provide project type (e.g. unity or private)"
        return 1
    fi

    SAVE_FILE=$(mktemp projectXXXXXXXX -t)

    $SCRIPTPATH/gitlab-client.pyz $1 open --save-dir-to $SAVE_FILE --search "${@:2}"

    if [ -s "$SAVE_FILE" ] ; then
		PROJECT_PATH=$(cat $SAVE_FILE)
        cd $PROJECT_PATH
		echo "opening $PROJECT_PATH"
        idea $PROJECT_PATH
    fi
}