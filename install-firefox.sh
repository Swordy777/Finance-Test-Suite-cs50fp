#!/bin/bash 

echo "Changing to home directory..."
pushd "$HOME"

echo "Update the repository and any packages..."
sudo apt update && sudo apt upgrade -y

echo "Installing necessary packages..."
sudo apt-get install libdbus-glib-1-2
sudo apt install bzip2

echo "Download the latest Firefox installation package..."
wget -O ~/FirefoxSetup.tar.bz2 "https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US"

echo "Install Mozilla Firefox..."
sudo tar xvjf ~/FirefoxSetup.tar.bz2 --directory /etc/alternatives/

echo "Deleting the installation package..."
rm FirefoxSetup.tar.bz2

echo "Creating symbolic link for the unpacked Firefox..."
sudo ln -s /etc/alternatives/firefox/firefox /usr/bin/firefox

firefox_version=($(firefox --version))
echo "Firefox version: ${firefox_version[2]}"

popd