#!/usr/bin/env bash

APP_FILE="gitlab-client.pyz"
SOURCE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
TARGET_DIR=$(mktemp -d -t installXXXXXXXXXXX)

cd $SOURCE_DIR
cp -r $(ls *.py| grep -vE "^venv$") $TARGET_DIR

rm -f $APP_FILE

/usr/bin/env python3 -m zipapp -o $APP_FILE -p '/usr/bin/env python3' $TARGET_DIR
echo "build done, created: $APP_FILE"