# rasdaq (RASpberry pi Data AcQuisition)

`rasdaq` is a client and server code for Raspberry Pi 2. It consists of a two codes:
 
* `rdcli` is the command line interface (CLI) for client and server
* `rdgui` is just a GUI client for visual purposes written in PyQt5.

#### Installation of Raspbian

It is recommended to download the full `raspbian` version, since the full python is included, from [here](https://www.raspbian.org/). You can check the `shasum` before installation to make sure it is the original file.

Later you can use `dd` to copy the image. E.g. on OSX you would type: 

    sudo dd bs=1m if=2015-11-21-raspbian-jessie.img of=/dev/rdisk4

After booting you need to find out the IP address just by connecting to a router. The router's own web page and find out the IP or MAC address. There are also other methods available under linux.


#### Installation on Raspi
After the first boot, you need to install a couple of things for the server part. Please note, that you do not need to install PyQt5 or any other GUI elements on the Raspberry PI, as these are only needed for the GUI on the client machine (OSX, Win, Lin, etc...). 

    sudo apt-get install python3-pip
    sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.4 2
    sudo update-alternatives --install /usr/bin/pip pip /usr/bin/pip-3.2 2
    sudo pip install RPi.GPIO
    sudo pip install pyzmq


#### Connection
From then on you can connect using SSH and screen:

    ssh -t pi@IP_ADDRESS screen -D -R

The defulat username and password should be `pi` and `raspberry`.


#### Usage
You can run the server on the raspberry by:

    ./rdcli ./--host IP_ADRESS --port 1234 --server

and accordingly the client by:

    ./rdcli ./--host IP_ADRESS --port 1234 --client

It is recommended to use numerals for IP address.
