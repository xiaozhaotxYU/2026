# st7735.py - 精简 ST7735 写入（仅示例，建议用成熟库替换）
import time
from machine import Pin

class ST7735:
    def __init__(self, spi, cs, dc, reset, width=160, height=128):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.reset = reset
        self.width = width
        self.height = height
        self.init_display()

    def write_cmd(self, cmd):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytes([cmd]))
        self.cs(1)

    def write_data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(data)
        self.cs(1)

    def init_display(self):
        # 简化初始化序列，实际请用完整初始化
        self.reset(0)
        time.sleep_ms(50)
        self.reset(1)
        time.sleep_ms(50)
        # 省略具体命令——请替换为你模块所需初始化序列
        # 进入帧缓冲准备
        self.write_cmd(0x36)  # MADCTL
        self.write_data(bytes([0x70]))
        self.write_cmd(0x3A)  # COLMOD
        self.write_data(bytes([0x05]))  # RGB565
        self.write_cmd(0x29)  # DISP ON

    def set_window(self, x0, y0, x1, y1):
        # Column addr set
        self.write_cmd(0x2A)
        self.write_data(bytes([0x00, x0, 0x00, x1]))
        # Row addr set
        self.write_cmd(0x2B)
        self.write_data(bytes([0x00, y0, 0x00, y1]))
        # RAM write
        self.write_cmd(0x2C)

    def blit_buffer(self, buf, x, y, w, h):
        # buf must be bytes object of size w*h*2 in RGB565
        self.set_window(x, y, x + w - 1, y + h - 1)
        self.write_data(buf)
