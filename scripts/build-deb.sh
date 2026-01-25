#!/bin/bash
set -e

VERSION="1.1.5"  # Change this

rm -rf build
mkdir -p build/DEBIAN build/usr/bin

# Build binary
cargo build --release
cp target/release/ppmm build/usr/bin/ppmm

# Copy control file
cp packaging/deb/control build/DEBIAN/control

# Build deb package
dpkg-deb --build build ppmm_${VERSION}_amd64.deb

echo "Deb package created: ppmm_${VERSION}_amd64.deb"
