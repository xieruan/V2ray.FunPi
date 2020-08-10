#!/bin/bash
wget https://install.direct/go.sh
version=$1
file_name="v2ray-${version}.zip"
wget -O ${file_name} "https://github.com/v2fly/v2ray-core/releases/download/${version}/v2ray-linux-arm32-v7a.zip"

bash go.sh --local ${file_name}
rm go.sh
rm ${file_name}