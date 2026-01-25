#!/bin/bash
set -e

VERSION="1.1.5"  # Change this

cd releases/windows
zip -r ppmm-windows-x64.zip ppmm-windows-x64.exe
cd ../../

echo "Windows zip created!"
