'''

get_byte_index_offset(x, y) returns the byte index and bit offset of the given pixel (x, y) in the byte array.

'''

LEDSCREEN_W = 40
LEDSCREEN_H = 32


dev_per_row = LEDSCREEN_W // 8
num_dev = LEDSCREEN_H * LEDSCREEN_W // 64

def get_byte_index_offset(x, y):
    r = y // 8          # which row of devices is this pixel in
    flip = r % 2 == 1       # does this row need to be flipped?
    
    # ypos in the row (ypos is the byte index in the device)
    ypos = y % 8
    if flip:
        ypos = 7 - ypos
        
    # which device in the row is this pixel in
    dev_no_in_row = x // 8
    if flip:
        dev_no_in_row = dev_per_row - 1 - dev_no_in_row
    
    # which device in all devices is this pixel in
    dev_no = r * dev_per_row + dev_no_in_row
    
    # calculate index and offset
    index = ypos * num_dev + dev_no
    offset = 7 - x % 8
    if flip:
        offset = 7 - offset

    return (index, offset)


if __name__ == '__main__':
    
  for y in range(LEDSCREEN_H):
      for x in range(LEDSCREEN_W):
          index, offset = get_byte_index_offset(x, y)
          print(f'{index:3d},{offset:1d}', end=' ')
          if x % 8 == 7:
              print('', end=' ')
      print()
      
      if y % 8 == 7:
          print()