import RPi.GPIO as GPIO
import time

def beep(amt, tm):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    BUZZER = 23
    buzzState = False
    GPIO.setup(BUZZER, GPIO.OUT)

    for x in range(amt * 2):
        buzzState = not buzzState
        GPIO.output(BUZZER, buzzState)
        time.sleep(tm)
    GPIO.cleanup()
    return

if __name__ == "__main__":
    beep(2, 0.05)