#!/bin/bash
source ~/.bash_profile

currentpwd=$PWD

cd ~/daily-api
python -m app.usecase.add_updated_pages_to_daily_log

cd $currentpwd
