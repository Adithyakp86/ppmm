#!/bin/bash
set -e

VERSION="1.1.5"  # Change this

# Create temp folder
rm -rf aur-build
mkdir -p aur-build
cp -r packaging/aur/* aur-build/

# Build AUR package
cd aur-build
makepkg -si

echo "AUR package installed!"
