#!/bin/bash

echo "Changing to home directory..."
pushd "$HOME"

echo "Update the repository and any packages..."
sudo apt update && sudo apt upgrade -y

echo "Install prerequisite packages..."
sudo apt install wget curl unzip -y

echo "Download the latest Chrome .deb file..."
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

echo "Install Google Chrome..."
sudo dpkg -i google-chrome-stable_current_amd64.deb

echo "Fix dependencies..."
sudo apt --fix-broken install -y

echo "Deleting the .deb file..."
rm google-chrome-stable_current_amd64.deb

chrome_version=($(google-chrome-stable --version))
echo "Chrome version: ${chrome_version[2]}"


cdriver_ver=$(curl -s 'https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json' | \
    python3 -c "import sys, json; print(json.load(sys.stdin)['channels']['Stable']['version'])")
chrome_ver=$(echo "$(cut -d"." -f1 <<< ${chrome_version[2]})")
cdriver_ver=$(echo "$(cut -d"." -f1 <<< ${cdriver_ver})")

echo "Comparing the latest available Chrome driver to the installed Chrome..."
if [[ "$chrome_ver" == "$cdriver_ver" ]]; then
    echo "Installing the fitting Chrome driver..."
    cdriver=$(curl -s 'https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json' | \
        python3 -c "import sys, json; print(next(item['url'] for item in json.load(sys.stdin)['channels']['Stable']['downloads']['chromedriver'] if item['platform'] == 'linux64'))")
    wget -O "$(basename "$cdriver")" "$cdriver"
    unzip -j "$(basename "$cdriver")"
    sudo mv chromedriver /usr/bin/chromedriver
    sudo chown root:root /usr/bin/chromedriver
    sudo chmod +x /usr/bin/chromedriver
else
    echo "Chrome browser and the latest Chrome driver versions are not matching; download a fitting Chrome driver version and install it manually"
fi

popd