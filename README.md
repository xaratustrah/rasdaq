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
First you have to enable SPI function in `raspi-config`. Here you connect the SPI interface to the MCP3208. Since SPI interface can handle 2 devices, remember if you choose pin 24 as CS, then your device will be known as `/dev/spi0.0` and for pin 26 it will be `/dev/spi0.1`. 


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

For accessing different channels on **MCP3208** you may choose the following commands. The reason is that you have to keep talking to the device in order to keep the clock running while the chip select signal is low, so that the device can respond accordingly. In the current implementation of the `spidev` is such that the chipselect is taken down per `xfer` command, and released afterwards. So unfortunately it seems that chip select can not be released from within the `xfer` command. This means you can not access different channels of MCP3208 at once, but need to send one `xfer` command for each channel.

| channel | command                     |
|---------|-----------------------------|
| 0       |spi.xfer([0x06, 0x00, 0x00]) |
| 1       |spi.xfer([0x06, 0x40, 0x00]) |
| 2       |spi.xfer([0x06, 0x80, 0x00]) |
| 3       |spi.xfer([0x06, 0xC0, 0x00]) |
| 4       |spi.xfer([0x07, 0x00, 0x00]) |
| 5       |spi.xfer([0x07, 0x40, 0x00]) |
| 6       |spi.xfer([0x07, 0x80, 0x00]) |
| 7       |spi.xfer([0x07, 0xC0, 0x00]) |

These values can be sent as binary or decimal of course.


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
