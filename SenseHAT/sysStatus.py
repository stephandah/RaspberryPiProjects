import psutil # pip3 install psutils
from sense_hat import SenseHat

black = [0,0,0]
green = [0,255,0]
red = [255,0,0]
yellow = [255,255,0]
orange = [255,128,0]
 
def perc_leds(perc):
    """Convert the percentage value into the number of LEDs to light up"""
    if perc == 0.0 : 
        return 0
    elif perc < 11.0:
        return 1
    elif perc < 26.0:
        return 2
    elif perc < 36.0:
        return 3
    elif perc < 51.0:
        return 4
    elif perc < 61.0:
        return 5
    elif perc < 76.0:
        return 6
    elif perc < 91.0:
        return 7
    else : 
        return 8

def led_color(idx):
    """Return the color of LED with index idx"""     
    if idx < 2:
        return green
    if idx < 4:
        return yellow
    if idx < 6:
        return orange
    return red

def show_leds(sense, idx, perc):
    """Display the percentage value in column idx of the LED matrix"""
    leds = perc_leds(perc)
    for led in range(8):
        if led < leds:
            col = led_color(led)
        else:
            col = black
        sense.set_pixel(idx, led, col)
        
sense = SenseHat()
prev_sent = 0
prev_recv = 0
cpus = psutil.cpu_count()
try:        
    while True:
        load = psutil.cpu_percent(interval=1, percpu=True)
        for cpu, i in zip(load, range(cpus)):
            show_leds(sense, i, cpu)
            #print("{0} cpu has load {1}".format(i, cpu))
        mem = psutil.virtual_memory()
        show_leds(sense, cpus, mem.percent)
        disk = psutil.disk_usage('/')
        show_leds(sense, cpus+1, disk.percent)
        net = psutil.net_io_counters()
        sent = (net.bytes_sent - prev_sent) / 80
        show_leds(sense, cpus+2, sent)
        recv = (net.bytes_recv - prev_recv) / 80
        show_leds(sense, cpus+3, recv)
        prev_sent = net.bytes_sent
        prev_recv = net.bytes_recv
        print('sent: {0}, recv: {1}'.format(sent, recv))
finally:
    sense.clear()
