import RPi.GPO as GPIO
import time
import os
import subprocess
import sys

GPIO.setmode(GPIO.BCM) # setam modul de numerotare al pinilor: BCM (Broadcom SOC channel)
                       
# numim pinii
PIR_PIN_1 = 21
PIR_PIN_2 = 19
RED_LED_PIN = 6
GREEN_LED_PIN = 5

# setam pinii ca intrari sau iesiri
GPIO.setup(PIR_PIN_1, GPIO.IN)
GPIO.setup(PIR_PIN_2, GPIO.IN)
GPIO.setup(RED_LED_PIN, GPIO.OUT)
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)

# testul propriu-zis
try:
    print("started detection test")
    GPIO.output(GREEN_LED_PIN, GPIO.HIGH) # LED-ul verde semnaleaza ca script-ul a pornit 
                                          # si ca PI-ul asculta pe terminalele 19 si 21 semnalul de la senzori
    while True:

        # variabile pentru a stoca raspunsul senzorilor
        response_1 = GPIO.input(PIR_PIN_1)
        response_2 = GPIO.input(PIR_PIN_2)

        # raspunsul pozitiv al senzorilor este LOW si nu HIGH
        if response_1 == GPIO.LOW:  
            print("presence detected by sensor 1")

        if response_2 == GPIO.LOW:
            print("presence detected by sensor 2")

        if GPIO.input(PIR_PIN_1) or GPIO.input(PIR_PIN_2):
            GPIO.output(RED_LED_PIN, GPIO.HIGH) # aprindem LED-ul rosu daca am detectat o intrare
            subprocess.run(["fswebcam", "suspect_1.jpg"], check = True) # se fac pozele si se salveaza ca suspect_x.jpg
            subprocess.run(["fswebcam", "suspect_2.jpg"], check = True) 
            subprocess.run(["fswebcam", "suspect_3.jpg"], check = True) 
            subprocess.run(["mpg321", "alarm.mp3"]) 

            GPIO.output(GREEN_LED_PIN, GPIO.LOW) # stingem LED-ul verde daca am detectat o intrare
            sys.exit() # si iesim din executie
            
            
        GPIO.output(RED_LED_PIN, GPIO.LOW) # stingem LED-ul rosu dupa fiecare ciclu de ascultat senzorii
        time.sleep(0.1) 

except KeyboardInterrupt:
    print("stopped detection test")
    GPIO.output(GREEN_LED_PIN, GPIO.LOW) # oprim LED-ul verde
    GPIO.cleanup()
        