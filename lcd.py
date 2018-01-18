import Adafruit_CharLCD as LCD
from time import *

lcd_rs        = 26
lcd_en        = 19
lcd_d4        = 13
lcd_d5        = 6
lcd_d6        = 5
lcd_d7        = 12
#lcd_backlight = 4
lcd_columns = 16
lcd_rows =2
#row1 = ""
#row2 = ""
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows)
class LcdDisplay:

    def __init__(self):
        pass
    def RadioScreen(self, x):
        pass

    def ChunkString(self, string, length):
        return (string[0+i:length+i] for i in range(0, len(string), length))

    def LeftShift(self):
        for i in range(40):
            lcd.move_left()
            sleep(.25)

    def Display(self,x):
        lst = []
        if len(x.split(': ')) == 1:
            lcd.message(x)
            if len(x) > 16:
                self.LeftShift()
        elif len(x.split(': ')) >=2:
            row1 = x.split(': ')[0]
            row2 = x.split(': ')[1]
            print(row1)
            print(row2)
            if len(row2) > 40:
                print('inside len')
                lines = (i.strip() for i in row2.splitlines())
                for line in lines:
                    for chuck in self.ChunkString(row2, 40):
                        lst.append(chuck)
                print(lst[0])
                print('row 1')
                print(row1)
                print('row 2')
                print(lst[0])
                lcd.message(row1+'\n')
                lcd.message(lst[0])
                self.LeftShift()
            lcd.message(row1+'\n')
            lcd.message(row2)
            if len(row1) | len(row2) > 16:
                self.LeftShift()
        
        
        

##lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
##                           lcd_columns, lcd_rows)
###lcd.create_char(1, [0b11111,0b10001,0b01110,0b00100,0b01010,0b10001,0b11111,0b00000])
###lcd.create_char(2, [31,17,14,4,4,14,17,31])
##lcd.clear()
##lcd.set_cursor(0,0)
##lcd.message("Hello")
##lcd.set_cursor(0,1)
##lcd.message("Paul")
