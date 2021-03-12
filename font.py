# draw the array for the character bit-map in max7219.py

from PIL import Image,ImageDraw,ImageFont

ch_bits = {}

def text_bits(ch, font_file='DejaVuSans.ttf', size=10):
	global ch_bits
	font = ImageFont.truetype(font_file, size, encoding="unic")
	text_width, text_height = font.getsize(ch)
	canvas = Image.new('1', (text_width, text_height), 'black')
	draw = ImageDraw.Draw(canvas)
	draw.text((0, 0), ch, 'white', font)
	# canvas.save('1/%d-%d.png' % (text_width, text_height), 'png')
	bits = [(x, y) for y in range(text_height) 
					for x in range(text_width) 
					if canvas.getpixel((x, y)) != 0]
	ch_bits[ch.strip()] = bits

def init_ch_bits():
	digit = '0123456789'
	letter = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	for ch in digit:
		text_bits(' '+ch, size=9)
	for ch in letter:
		text_bits(' '+ch, size=8)
	for ch in letter.lower():
		text_bits(' '+ch, size=9)

def all_zeros(bits, row=None, col=None):
	for x, y in bits:
		if x == col or y == row: return False
	return True


def clip_ch_bits1(m, bits):
	row = max([y for x, y in bits]) + 1
	col = max([x for x, y in bits]) + 1
	while row > m:
		if not all_zeros(bits, row=row-1): break
		bits = [(x,y) for (x,y) in bits if y != row-1]
		row -= 1
	while row > m:
		bits = [(x,y-1) for (x,y) in bits if y != 0]
		row -= 1
	while True:
		if not all_zeros(bits, col=col-1): break
		bits = [(x,y) for (x,y) in bits if x != col-1]
		col -= 1
	while True:
		if not all_zeros(bits, col=0): break
		bits = [(x-1,y) for (x,y) in bits if x != 0]
		col -= 1
	return row, col+1, bits

def clip_ch_bits(max):
	global ch_bits
	ch_bits = {ch:clip_ch_bits1(max, bits) for ch, bits in ch_bits.items()}

def print_ch_bits():
	print('{')
	for ch, (h, w, bits) in ch_bits.items():
		print("'%s':%s,"%(ch, str([(h, w)] + bits).replace(' ','')))
	print('}')

init_ch_bits()
clip_ch_bits(8)
print_ch_bits()