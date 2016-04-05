#!/bin/bash

REPORTING_DIR=/home/django/lvnproject/Weblvn/

cd ${REPORTING_DIR}
echo "im backing up the database at `date`" >>backup.log
cp WeblvnApp.db ~/sandbox_lvnproject/Weblvn/
