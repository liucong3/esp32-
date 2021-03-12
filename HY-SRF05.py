# NOT WORKING !

# HC-SR04 Ultrasound Sensor
import time
from machine import Pin

# WeMos D4 maps GPIO2 machine.Pin(2) = TRIGGER
# WeMos D2 maps GPIO4 machine.Pin(4) = ECHO
triggerPort = 2
echoPort = 4
out_of_range_distance = 1 # m
# 1m / sound-speed * 2-trips
out_of_range_duration = out_of_range_distance / 340.29 * 2 * 1000 # ms

def loop():
    trigger = Pin(triggerPort, Pin.OUT)
    echo = Pin(echoPort, Pin.IN)
    print("Ultrasonic Sensor. Trigger Pin=%d and Echo Pin=%d" % (triggerPort, echoPort))
    trigger.off()
    while True:
      # short impulse 10 microsec to trigger
      trigger.on()
      time.sleep_us(10)
      trigger.off()
      count = 0
      start = time.ticks_us() # get time in usec
      # Now loop until echo goes high
      while not echo.value():
          time.sleep_us(10)
          count += 1
          if count > 100:
              print("Counter exceeded")
              break
      duration = time.ticks_diff(start, time.ticks_us()) # compute time difference
      print("Duration: %f" % duration)

      # After 38ms is out of range of the sensor
      if duration > out_of_range_duration:
          print("Out of range")
          continue

      # distance is speed of sound [340.29 m/s = 0.034029 cm/us] per half duration
      distance = duration / 2 / 1000 * 340.29
      print("Distance: %fm" % distance)
      time.sleep(1)

loop()