from config import N_LEDS
import neopixel
import board
import lib.oled.SSD1331 as SSD1331

pixels = neopixel.NeoPixel(board.D18, N_LEDS, brightness=1.0/32, auto_write=False)
pixels.fill((0,0,0))
pixels.show()

disp = SSD1331.SSD1331()
disp.Init()
 # Clear display.
disp.clear()
disp.reset()