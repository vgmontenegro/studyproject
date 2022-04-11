import time
import os

class Timer():
    def __init__(self, hr=0, min=0, sec=0):
        self.sec = sec + (60*min) + (3600*hr)

    def start_timer(self):
        while True:
            if self.sec >= 0:
                hr = self.sec//3600
                min = (self.sec//60 - hr*60)
                sec = (self.sec - min*60 - hr*3600)
                print("{:02}:{:02}:{:02}".format(hr, min, sec))
                self.sec -= 1
                time.sleep(1)
            else:
                print("Time out!")
                break

timer1 = Timer(0,0,3)

timer1.start_timer()