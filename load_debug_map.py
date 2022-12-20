import sys
from idautils import *
from idaapi import *

def parse_symbol_line(symbol_line, symbol_addresses, symbol_names):
    symbol_address = None
    symbol_name = None

    split = symbol_line.split(' ')

    for word in split:
        if(len(word) <= 1):
            continue

        int_address = 0

        try:
            int_address = int('0x' + word, 16)
        except Exception:
            pass

        if(symbol_address == None and int_address >= 0x80003100 and int_address <= 0x8040ed60):
            symbol_address = int_address
        elif(not symbol_address == None and not word[0].isdigit()):

            if(word.startswith('.')):
                return symbol_addresses, symbol_names

            symbol_name = word

            break

        # print('symbol address = 0x%x symbol name = %s' % (symbol_address, symbol_name))

    if(not symbol_address == None and not symbol_name == None):
        print('symbol address = 0x%x symbol name = %s' % (symbol_address, symbol_name))

        symbol_addresses.append(symbol_address)
        symbol_names.append(symbol_name)

    return symbol_addresses, symbol_names


all_symbol_addresses = []
all_symbol_names = []

file_to_open = "/Volumes/PRO-G40/Nintendo/RE/dolphin-games/super-mario-sunshine/files/marioEU.MAP" # **PATH TO YOUR MAP FILE GOES HERE**

with open(file_to_open, "r") as ins:
    array = []
    found_entry_point = False
    
    for line in ins:
        if len(line) < 3:
            continue

        all_symbols_addresse, all_symbol_names = parse_symbol_line(line, all_symbol_addresses, all_symbol_names)
        
        array.append(line)

# print(len(all_symbol_addresses))

ea = ida_ida.inf_get_min_ea()

for funcea in Functions(idc.get_segm_start(ea), idc.get_segm_end(ea)):
    functionName = idc.get_func_name(funcea)
    # print(functionName)

matched_symbols = 0

index = 0

for funcea in all_symbol_addresses:
    new_name = all_symbol_names[index]

    found = False

    for segea in Segments():
        if funcea in Functions(segea, idc.get_segm_end(segea)):
            functionName = idc.get_func_name(funcea)

            print("Oldname:",functionName, "NewName:", new_name)
                
            idc.set_name(funcea, new_name)

            found = True

    if(not found):
        ida_funcs.add_func(funcea)

        print("NewName:", new_name)

        idc.set_name(funcea, all_symbol_names[index])

    matched_symbols += 1

    index += 1

print("Complete - matched %d symbols" % (matched_symbols))


