#!/bin/bash
wget https://install.direct/go.sh
if [ $? -eq 0 ];then
bash go.sh
rm go.sh
fi