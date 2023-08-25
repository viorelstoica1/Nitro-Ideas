import select
import sys
import time
import machine

led = machine.Pin("LED", machine.Pin.OUT)

# Set up the poll object
poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)

# Loop indefinitely
while True:
    # Wait for input on stdin
    poll_results = poll_obj.poll(1000) # the '1' is how long it will wait for message before looping again (in microseconds)
    if poll_results:
        # Read the data from stdin (read data coming from PC)
        data = sys.stdin.readline().strip()
        if(data == "on"):
            led.on()
        elif(data == "off"):
            led.off()
        # Write the data to the input file
        sys.stdout.write(data + "\n\r")
    else:
        # do something if no message received (like feed a watchdog timer)
        #sys.stdout.write("No data\n\r")
        continue

