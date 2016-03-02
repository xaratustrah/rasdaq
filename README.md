# rasdaq (RASpberry pi Data AcQuisition)

`rasdaq` is a client and server code for Raspberry Pi 2 to acquire ADC Data from [MCP8208](http://www.microchip.com/wwwproducts/en/MCP3208) 12-bit ADC converter chip. The [SPI](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface_Bus) interface is emulated using Raspberry PI's GPIO pin, the way that is described in [this tutorial](https://www.raspiprojekt.de/machen/basics/schaltungen/26-analoge-signale-mit-dem-mcp3008-verarbeiten.html). An alternative would be to use raspberry pi's processor's own SPI interface, which is not applied here in this code. The underlying messaging is accomplished using [Zero MQ](http://zeromq.org/) library in PUB/SUB mode. 

![rdgui](https://raw.githubusercontent.com/xaratustrah/rasdaq/master/rsrc/screenshot.png)

The code consists of a separate parts:
 
* `rdcli` is the command line interface (CLI) for client and server
* `rdgui` is just a GUI client (viewer) for visual inspection written in QT5 (PyQt5).


#### Hardware connection
Follow the description on the tutorial mentioned above. Additionally what has been changed here is the following pin numbering:


| Name | Pin No. |
|------|---------|
| SCLK | 23      |
| MISO | 21      |
| MOSI | 19      |
| CS   | 29      |
| LED  | 31      |


As you can see, an additional LED is connected to the raspberry with a 330 ohm resistor in between.

#### Installation of Raspbian

It is recommended to download the full `raspbian` version, since the full python is included, from [here](https://www.raspbian.org/). You can check the `shasum` before installation to make sure it is the original file.

Later you can use `dd` to copy the image. The procedure on OSX would be e.g.: Identify the name of the SD Card:

    diskutil list

in my case it was `/dev/disk2`. The unmount it:

    diskutil unmountDisk /dev/disk2
    
then use the `dd` to copy:

    sudo dd bs=1m if=2015-11-21-raspbian-jessie.img of=/dev/rdiskN

you can use `ctrl-T` to check the progress. After booting if you have a HDMI television and keyboard attached then you can see your IP address of course, but if you like me are only connected to internet without any display then you need to find out the IP address just by connecting to a router. Open router's own web page and find out the IP or MAC address. There are also other methods available under linux.


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
To print out the help, type:

    ./rdcli --help
    
## Acknowledgements
Many thanks goes to [HoSnoopy](https://github.com/HoSnoopy) for pointing out a link to the tutorial and [carlkl](https://github.com/carlkl) for pointing out the wonderful ZeroMQ library.
