# About the distribution
The Ledger Starter uses the SliTaz Linux distro. Find out more here:
http://www.slitaz.org/

# Start
 - Download a SliTaz ISO on slitaz.org
 - Make a bootable flash drive (using various tools like Rufus, UNetbootin, ...) or boot in a virtual machine
 - When prompted, select "Base Live"

# Recipe

#### tazpkg
Run the following commands to install the required packets (as of today, **tazpkg** doesn't allow multiple packages to be installed at once)
```
tazpkg get-install python python-cython
tazpkg get-install git
tazpkg get-install wget
tazpkg get-install gcc
tazpkg get-install slitaz-toolchain
tazpkg get-install python-dev
tazpkg get-install setuptools
tazpkg get-install libtool
tazpkg get-install udev-dev
tazpkg get-install pkg-config
```

#### Configuring libudev
```
pkg-config --libs --cflags libudev
```

#### Installing PYUSB
```
export GIT_SSL_NO_VERIFY=true
git clone https://github.com/walac/pyusb
cd pyusb
python setup.py install
```

#### Install PIP
```
wget https://bootstrap.pypa.io/get-pip.py --no-check-certificate
python get-pip.py
```

#### Ledger Wallet udev rules
Add the Ledger Wallet udev rules (from our FAQ: http://support.ledgerwallet.com/knowledge_base/topics/ledger-wallet-is-not-recognized-on-linux)
```
echo "SUBSYSTEMS==\"usb\", ATTRS{idVendor}==\"2581\", ATTRS{idProduct}==\"1b7c\", MODE=\"0660\", GROUP=\"plugdev\"" >/etc/udev/rules.d/20-hw1.rules
echo "SUBSYSTEMS==\"usb\", ATTRS{idVendor}==\"2581\", ATTRS{idProduct}==\"2b7c\", MODE=\"0660\", GROUP=\"plugdev\"" >>/etc/udev/rules.d/20-hw1.rules
echo "SUBSYSTEMS==\"usb\", ATTRS{idVendor}==\"2581\", ATTRS{idProduct}==\"3b7c\", MODE=\"0660\", GROUP=\"plugdev\"" >>/etc/udev/rules.d/20-hw1.rules
echo "SUBSYSTEMS==\"usb\", ATTRS{idVendor}==\"2581\", ATTRS{idProduct}==\"4b7c\", MODE=\"0660\", GROUP=\"plugdev\"" >>/etc/udev/rules.d/20-hw1.rules
echo "SUBSYSTEMS==\"usb\", ATTRS{idVendor}==\"2581\", ATTRS{idProduct}==\"1807\", MODE=\"0660\", GROUP=\"plugdev\"" >>/etc/udev/rules.d/20-hw1.rules
echo "SUBSYSTEMS==\"usb\", ATTRS{idVendor}==\"2581\", ATTRS{idProduct}==\"1808\", MODE=\"0660\", GROUP=\"plugdev\"" >>/etc/udev/rules.d/20-hw1.rules
udevadm trigger
udevadm control --reload-rules
```

#### BIP39 support
```
git clone https://github.com/trezor/python-mnemonic
cd python-mnemonic
python setup.py install
```

#### Cython
```
wget http://cython.org/release/Cython-0.22.zip
unzip Cython-0.22.zip
cd Cython-0.22
python setup.py build
python setup.py install
```

#### libusb-1.0 1.0.9
```
wget http://downloads.sourceforge.net/project/libusb/libusb-1.0/libusb-1.0.9/libusb-1.0.9.tar.bz2
tar -xvf libusb-1.0.0.tar.bz2
cd libusb-1.0.0 
./configure --prefix=/usr
make
make install
ln -s /usr/include/libusb-1.0/libusb.h /usr/include/
```
*Note:  you may need to download **libusb-1.0.9.tar.bz2** manually*

#### hidapi
```
git clone git://github.com/signal11/hidapi.git
cd hidapi
autoreconf -i
automake
LIBS="-lusb-1.0 -ludev" ./configure --prefix=/usr
make
make install
```

#### cython-hidapi
```
git clone https://github.com/trezor/cython-hidapi
cd cython-hidapi
git submodule init
git submodule update
python setup.py build
python setup.py install
```

#### btchip-python
```
git clone https://github.com/LedgerHQ/btchip-python
cd btchip-python
python setup.py install
```

#### Misc dependencies (used in the Python script)
```
pip install pretty-table
pip install ecdsa
pip install blessings
```

# Writing changes
SliTaz comes with a handy tool allowing you to save your changes to a *rootfs.gz* file (for instance).
Just run:
```
tazusb writefs gzip
```
And follow the instructions. You will then need to move the /rootfs.gz file to your flash drive (and replace the old one).