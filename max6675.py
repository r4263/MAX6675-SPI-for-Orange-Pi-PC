import spidev
import time
import argparse

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 50000
spi.mode = 0b00

def read():
    raw = spi.xfer2([0x00, 0x00])
    value = ((raw[0] << 8) | raw[1])
    
    if value & 0x4:
        return 0
    
    value >>= 3
    return value * 0.25

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reads MAX6675 temperature.")
    parser.add_argument("samples", type=int, help="Number of collection samples.")
    parser.add_argument("total_time", type=float, help="Total collection time(seconds).")
    args = parser.parse_args()

    interval = args.total_time / args.samples
    temperatures = []
    
    try:
        for _ in range(args.samples):
            temp = read()
            temperatures.append(temp)
            time.sleep(interval)
        
        print(sum(temperatures) / len(temperatures) if temperatures else 0)
    
    except KeyboardInterrupt:
        print(0)
    finally:
        spi.close()
