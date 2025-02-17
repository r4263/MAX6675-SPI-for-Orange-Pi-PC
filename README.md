# MAX6675 SPI for Orange Pi PC

Developed by Maycon Jung to supress a necessity to measure a datacenter temperature.

Tested in Armbian Community(6.6.72-current-sunxi)

## Connections
| MAX6675 Pin                   | Pin header number                            |
| ----------------------------- | -------------------------------------------- |
| VCC                           | 17(Or any 3.3V supply pin. Not tested at 5V) |
| GND                           | 20(Or any GND/0V pin)                        |
| SCK(Serial clock)             | 23                                           |
| CS(Chip select)               | 24                                           |
| MISO/SO(Master In, Slave Out) | 21                                           |

## Installation
### Verify the existence of a SPI device
In the Armbian shell, run: 
```c
ls /dev/spidev
```
And if the output is not something like that: 
```c
/dev/spidev0.0
```

Add the following code to `/boot/armbianEnv.txt` (using root or sudo):
```c
overlays=spi-spidev
param_spidev_spi_bus=0
```

Or you can just run: 
```c
echo -e "overlays=spi-spidev\nparam_spidev_spi_bus=0" | sudo tee -a /boot/armbianEnv.txt
```
to add the content to this file automatically. And then reboot the OS to the changes take effects.

After the reboot, install the packages and dependencies with:
```c
apt update
apt install python3-spidev
```

Move the file `max6675.py` into `/opt` folder and then test it with:
```c
python3 /opt/max6675.py
```

If everythins has been installed corectly, you should see the following message at the shell:
```c
usage: max6675.py [-h] samples total_time
max6675.py: error: the following arguments are required: samples, total_time
```

## Usage
`python3 /opt/max6675.py <samples> <total_sample_time>`

Example: if everything was been wired correctly, the command: `python3 /opt/max6675.py 10 5` should output something like this:
```c
32.975
```

where the `<samples>` is the number of samples taken in `<total_sample_time>` time window.

## Zabbix and zabbix_agentd.d

The file inside `zabbix_agentd.d` folder is a ready to use additional conf that can be put inside `/etc/zabbix/zabbix_agentd.d/` to be used as supplemental config. Note that to this config file works, it must be enabled at the Zabbix Agent config file(default: enabled) and the service must be restarted.

## Possible issues

Sometimes, you'll get a "permission denied" in the first lines od the cod. It's caused by the permissions in the spi device, which you can fix by running the following command:

```c
chmod +rw /dev/spidev0.0

OR

chmod 666 /dev/spidev0.0
```

Even though, sometimes the SPI device keeps mounting/remounting itself after a couple of minutes, and has been fixed adding the following code to `/etc/rc.local`:

```c
chmod 666 /dev/spidev0.0
```

or add automatically with:

```c
echo -e "chmod 666 /dev/spidev0.0" | sudo tee -a /etc/rc.local
```

### This last resolution(adding the chmod to rc.local) IS NOT recommended as a definitive solution, this is an open issue that needs some time to fix it definitively.