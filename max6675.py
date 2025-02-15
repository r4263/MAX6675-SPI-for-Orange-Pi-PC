import spidev

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 50000
spi.mode = 0b00

def read_temperature():
    raw = spi.xfer2([0x00, 0x00])
    value = ((raw[0] << 8) | raw[1])
    
    if value & 0x4:
        return 0
    
    value >>= 3
    return value * 0.25

try:
    print(read_temperature())
except:
    spi.close()
