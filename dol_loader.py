import idaapi
import ida_segment
from idc import *
import struct

DolFormatName = 'Nintendo GC\Wii DOL'

# ---------------------------------------------------------
def read_int(li):
	s = li.read(4)
	return struct.unpack('>I', s)[0]

# ---------------------------------------------------------
def accept_file(li, filename):
	if filename.endswith('.dol'):
		return {'format': DolFormatName, 'processor': 'ppc'}
	
	return 0

# ---------------------------------------------------------
def load_file(li, neflags, format):
	li.seek(0);
	
	text_offset = []
	text_addr = []
	text_size = []
	
	data_offset = []
	data_addr = []
	data_size = []
	
	print('Reading offsets...')
	
	for x in range(0, 7):
		text_offset.append(read_int(li))
		print(hex(text_offset[x]))
	
	for x in range(0, 11):
		data_offset.append(read_int(li))
		print(hex(data_offset[x]))
	
	print('Reading addresses...')
	
	for x in range(0, 7):
		text_addr.append(read_int(li))
	
	for x in range(0, 11):
		data_addr.append(read_int(li))
	
	print('Reading sizes...')
	
	for x in range(0, 7):
		text_size.append(read_int(li))
	
	for x in range(0, 11):
		data_size.append(read_int(li))
	
	print('Reading bss info...')
	
	bss_addr = read_int(li)
	bss_size = read_int(li)
	
	print('Reading entry point...')
	
	entry_point = read_int(li)
	
	print('Setting processor type...')
	
	idaapi.set_processor_type('ppc', SETPROC_LOADER)
	
	print('Adding text segments...')
	
	for x in range(0, 7):
		if text_size[x] == 0:
			continue
		end_addr = text_addr[x] + text_size[x]
		ida_segment.add_segm(0, text_addr[x], end_addr, 'Text' + str(x), 'CODE')
		li.file2base(text_offset[x], text_addr[x], end_addr, 1)
	
	print('Adding data segments...')
	
	for x in range(0, 11):
		if data_size[x] == 0:
			continue
		end_addr = data_addr[x] + data_size[x]
		ida_segment.add_segm(0, data_addr[x], end_addr, 'Data' + str(x), 'DATA')
		li.file2base(data_offset[x], data_addr[x], end_addr, 1)
	
	print('Adding bss segment...')
	
	if bss_size != 0:
		ida_segment.add_segm(0, bss_addr, bss_addr + bss_size, 'bss', 'BSS')
	
	ida_entry.add_entry(entry_point, entry_point, 'entry', 1)
	
	return 1
	
