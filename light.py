from machine import Pin, ADC, I2C
import utime
import dht

# Button setup
button = Pin(15, Pin.IN, Pin.PULL_DOWN)

# Motion sensor setup
motion_sensor = Pin(14, Pin.IN)

# LED setup
led = Pin(13, Pin.OUT)

# LDR setup
ldr = ADC(26)

# DHT22 sensor setup (for humidity and temperature)
dht_sensor = dht.DHT22(Pin(12))

# OLED display setup (assuming SSD1306 display)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

def check_motion():
    if motion_sensor.value() == 1:
        led.on()
        check_led()
    else:
        led.off()

def check_led():
    ldr_value = ldr.read_u16()
    if ldr_value < 10000:  # Adjust this threshold as needed
        display_message("LED not working!")

def read_dht():
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        return temp, hum
    except:
        return None, None

def display_message(message):
    oled.fill(0)
    oled.text(message, 0, 0)
    oled.show()

def main():
    system_active = False
    
    while True:
        if button.value() == 1:
            system_active = not system_active
            utime.sleep_ms(200)  # Debounce delay
        
        if system_active:
            check_motion()
            
            temp, hum = read_dht()
            if temp is not None and hum is not None:
                display_message(f"Temp: {temp}C Hum: {hum}%")
            
        utime.sleep(0.1)

if __name__ == "__main__":
    main()
