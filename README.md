# rasdaq (RASpberry pi Data AcQuisition)

`rasdaq` is a client and server code for Raspberry Pi 2 to acquire ADC Data from [MCP8208](http://www.microchip.com/wwwproducts/en/MCP3208) 12-bit ADC converter chip.
![rdgui](https://raw.githubusercontent.com/xaratustrah/rasdaq/master/rsrc/screenshot.png)


The [SPI](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface_Bus) interface is implemented using 2 methods:
* Using own SPI interface based on a python wrapper for [spidev](https://github.com/doceme/py-spidev). 
* Raspberry PI's GPIO pin, the way that is described in [this tutorial](https://www.raspiprojekt.de/machen/basics/schaltungen/26-analoge-signale-mit-dem-mcp3008-verarbeiten.html).

The underlying messaging is accomplished using [Zero MQ](http://zeromq.org/) library in PUB/SUB mode.

The code consists of a separate parts:
 
* `rdcli` is the command line interface (CLI) for client and server
* `rdcli_gpio` same as above, but with SPI emulation using GPIO.
* `rdgui` is just a GUI client (viewer) for visual inspection written in QT5 (PyQt5).

#### General installation
please refer to the more detailed [gist](https://gist.github.com/xaratustrah/4efc5001f1bbcce47e02e2343ba29b87).

#### Hardware connection **spi-dev**
First you have to enable SPI function in `raspi-config`. Here you connect the SPI interface to the MCP3208. Remember it you choose pin 24, then your device will be known as `/dev/spi0.0` and for pin 26 it will be `/dev/spi0.1`. 


| Name | Pin No. |
|------|---------|
| LED  | 31      |
| RNG0 | 11      |
| RNG1 | 13      |
| RNG2 | 15      |
| MODD | 7       |
| RDDY | 8       |
| PWWR | 10      |


As you can see, an additional LED is connected to the raspberry with a 330 ohm resistor in between.

#### Hardware connection
Follow the description on the tutorial mentioned above. Additionally what has been changed here is the following pin numbering:


| Name | Pin No. |
|------|---------|
| SCLK | 23      |
| MISO | 21      |
| MOSI | 19      |
| CS   | 29      |
| LED  | 31      |
| RNG0 | 11      |
| RNG1 | 13      |
| RNG2 | 15      |
| MODD | 7       |
| RDDY | 8       |
| PWWR | 10      |


#### Usage
You can run the server on the raspberry by:

    ./rdcli --host IP_ADRESS --port 1234 --server

and accordingly the client by:

    ./rdcli --host IP_ADRESS --port 1234 --client

It is recommended to use numerals for IP address.
To print out the help, type:

    ./rdcli --help
    
## Acknowledgements
Many thanks goes to [HoSnoopy](https://github.com/HoSnoopy) for pointing out a link to the tutorial to GPIO emulation and [carlkl](https://github.com/carlkl) for pointing out the wonderful ZeroMQ library.
