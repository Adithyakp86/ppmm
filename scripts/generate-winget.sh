#!/bin/bash
set -e

VERSION="1.1.5"  # Change this
SHA256=$(sha256sum releases/windows/ppmm-windows-x64.zip | awk '{print $1}')

cat > packaging/winget/ppmm.yaml <<EOL
Id: Sumangal44.ppmm
Name: ppmm
Version: $VERSION
Publisher: Sumangal44
License: MIT
ShortDescription: Python Project Manager CLI
Installers:
  - Architecture: x64
    InstallerType: portable
    InstallerUrl: https://github.com/Sumangal44/ppmm/releases/download/v$VERSION/ppmm-windows-x64.zip
    InstallerSha256: $SHA256
EOL

echo "Winget manifest generated!"
