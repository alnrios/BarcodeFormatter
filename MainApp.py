import csv
import os
from sys import exit

os.system("mode con cols=100 lines=40")

source_file = 'C:\Source File\SourceFile.csv'
storex_file = 'C:\ProgramData\Tecan\EVOware\output\StoreX_PosList.txt'
plate_batch_count_file = 'C:\ProgramData\Tecan\EVOware\input\Plate batches\PlateBatchCount.csv'
gen_file_list = ['C:\ProgramData\Tecan\EVOware\input\Plate batches\Inc0_48well_A.csv',
                    'C:\ProgramData\Tecan\EVOware\input\Plate batches\Inc0_48well_B.csv',
                    'C:\ProgramData\Tecan\EVOware\input\Plate batches\Inc15_48well_A.csv',
                    'C:\ProgramData\Tecan\EVOware\input\Plate batches\Inc15_48well_B.csv',
                    'C:\ProgramData\Tecan\EVOware\input\Plate batches\Inc25_48well_A.csv',
                    'C:\ProgramData\Tecan\EVOware\input\Plate batches\Inc25_48well_B.csv']

def append_to_dict(a_dict, value, iterator):
    if isinstance(value, list):
        for n in a_dict:
            a_dict[n].append(value[iterator])
            iterator += 1
    else:
        a_dict[iterator].append(value)

def check_for_gen_plate(storex_row):
    if 'gen' in storex_row.lower():
        print('StoreX File Error: ' + storex_row)

def display_header():
    print('\nT E C A N   S C A N   A S S I S T')
    print('-' * 34)
    print('\n')

def display_results():
    print('\n')
    print('*' * 30)
    print('\n')
    print("Tecan Scanning Results")
    print("-" * 22)
    print("\nThis run has {0} suspension plates, {1} 15-min plates, and {2} 25-min plates".format(num_of_0A_incs,
                                                                                                  num_of_15A_incs,
                                                                                                  num_of_25A_incs))
    print("\n{} plates total".format((num_of_0A_incs + num_of_15A_incs + num_of_25A_incs)))
    if len(rack_list) == 10:
        print('*' * 25)
        print('* All racks being used  *')
        print('*' * 25)
    else:
        print('\nNumber of racks being used: {0}'.format(len(rack_list)))
        print('\n******************')
        for rack in rack_list:
            print('* Rack #{0} in use *'.format(rack))
        print('******************')
    input('\nYour script has finished successfully, press Enter to exit.')

def double_checker(plate_list1, plate_list2):
    move_on = True
    position = 1000
    list_id1 = ''
    list_id2 = ''
    if plate_list1 is csv_barcode_list:
        list_id1 = 'CSV file'
        list_id2 = 'StoreX file'
    elif plate_list1 is storex_list_mod:
        list_id1 = 'StoreX file'
        list_id2 = 'CSV file'
    print('\n' + list_id1 + " results: ")
    if list_id1 == 'CSV file':
        print('-' * 17)
    else:
        print('-' * 20)
    for plate_num in plate_list1:
        if plate_list1 is csv_barcode_list:
            position = barcode_dict[plate_num][1]
        elif plate_list1 is storex_list_mod:
            position = storex_file_dict[plate_num]
        if plate_num not in plate_list2 and 'gen' not in plate_num.lower():
            print('{0} from your {1} (line {2}) not found in your {3}.'.format(plate_num, list_id1, position, list_id2))
            move_on = False
    if len(gen_list) > 0 and list_id1 == 'StoreX file':
        move_on = False
        print('Gen barcodes detected in StoreX file')
    if move_on:
        printing_string = '{0} looks good!\n'.format(list_id1)
    else:
        printing_string = 'Error(s) while processing.'
    print(printing_string)
    return move_on

def gen_disabler(list):
    finish = True
    for g in list:
        if 'gen' in g.lower():
            finish = False
    return finish

def pos_file_creator(file, type_num, incubtime):
    with open(file, 'w', newline='', encoding='utf-8-sig') as workingfile:
        if type_num == 0:
            pass
        else:
            writer2 = csv.writer(workingfile, delimiter='|')
            for n in barcode_dict:
                if incubtime == 0 and barcode_dict[n][0] == '0':
                    writer2.writerow(['{0},{1}'.format(n, barcode_dict[n][2])])
                elif incubtime == 15 and barcode_dict[n][0] == '15':
                    writer2.writerow(['{0},{1}'.format(n, barcode_dict[n][2])])
                elif incubtime == 25 and barcode_dict[n][0] == '25':
                    writer2.writerow(['{0},{1}'.format(n, barcode_dict[n][2])])

def rack_selector(counter):
    rack_num = 0
    if counter in range(1, 18):
        rack_num = 1
    elif counter in range(18, 35):
        rack_num = 2
    elif counter in range(35, 52):
        rack_num = 3
    elif counter in range(52, 69):
        rack_num = 4
    elif counter in range(69, 86):
        rack_num = 5
    elif counter in range(86, 103):
        rack_num = 6
    elif counter in range(103, 120):
        rack_num = 7
    elif counter in range(120, 137):
        rack_num = 8
    elif counter in range(137, 154):
        rack_num = 9
    elif counter in range(154, 171):
        rack_num = 10
    return rack_num

display_header()

try:
    with open(source_file, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        copied_csv_list = []
        csv_counter = 1
        csv_duplicates = False
        for row in reader:
            if row in copied_csv_list:
                print("SourceFile.csv - Duplicate found on line " + str(csv_counter) + ": " + row[0][:8])
                csv_duplicates = True
            else:
                copied_csv_list.append(list(row))
            csv_counter += 1
        if csv_duplicates:
            print("\nDeleting duplicate barcodes...")
except FileNotFoundError:
    input('CSV File not found. Import and restart the program. Press Enter to exit...')
    exit()

with open(source_file, 'w', newline='', encoding='utf-8-sig') as new_csvfile:
    writer = csv.writer(new_csvfile, delimiter=' ')
    for rows in copied_csv_list:
        writer.writerow(rows)

csv_barcode_list = []
incub_time_list = []
csv_pos_list = []

for i in range(1, len(copied_csv_list)):
    csv_pos_list.append(i + 1)
    csv_barcode_list.append(copied_csv_list[i][0][0:8])
    if len(copied_csv_list[i][0]) < 13:
        incub_time_list.append(copied_csv_list[i][0][9:10])
    else:
        incub_time_list.append(copied_csv_list[i][0][9:11])

barcode_dict = {}

for barcode, incub_time in zip(csv_barcode_list, incub_time_list):
    barcode_dict.setdefault(barcode, []).append(incub_time)

append_to_dict(barcode_dict, csv_pos_list, 0)

try:
    with open(storex_file, newline='', encoding='utf-8-sig') as txt_file:
        gen_list = []
        storex_file_dict = {}
        storex_file_list = []
        ext_counter = 1
        txt_file_counter = 1
        rack_number = 1
        print('\nChecking for "Gen" Plates...\n')
        for row in txt_file:
            check_for_gen_plate(row)
            if 'gen' in row.lower():
                gen_list.append(row)
            if len(row) < 13:
                row_value = ''
                storex_file_dict[row_value] = ext_counter
                storex_file_list.append(row_value)
            elif len(row) == 14:
                row_value = row[4:12]
                storex_file_dict[row_value] = ext_counter
                storex_file_list.append(row_value)
            elif len(row) == 15:
                row_value = row[5:13]
                storex_file_dict[row_value] = ext_counter
                storex_file_list.append(row_value)
            elif len(row) == 16:
                row_value = row[6:14]
                storex_file_dict[row_value] = ext_counter
                storex_file_list.append(row_value)
            ext_counter += 1
        storex_file_dict.pop('')
        storex_file_list.pop(0)
        for item in storex_file_list:
            rack_number = rack_selector(txt_file_counter)
            if item in barcode_dict:
                append_to_dict(barcode_dict, txt_file_counter, item)
                append_to_dict(barcode_dict, rack_number, item)
            txt_file_counter += 1
except FileNotFoundError:
    input('StoreX file not found. Press Enter to exit...')
    exit()

storex_list_mod = []
for storex_item in storex_file_list:
    if storex_item != '':
        storex_list_mod.append(storex_item)

csv_check = double_checker(csv_barcode_list, storex_list_mod)
store_x_check = double_checker(storex_list_mod, csv_barcode_list)
gen_check = gen_disabler(gen_list)
if not csv_check or not store_x_check or not gen_check:
    input("\nYour CSV and StoreX files don't match up. Press Enter to exit the program and try again.")
    exit()

num_of_15A_incs = 0
num_of_0A_incs = 0
num_of_25A_incs = 0
num_of_15B_incs = 0
num_of_0B_incs = 0
num_of_25B_incs = 0

for i in barcode_dict:
    if barcode_dict[i][0] == '0':
        num_of_0A_incs += 1
    elif barcode_dict[i][0] == '15':
        num_of_15A_incs += 1
    elif barcode_dict[i][0] == '25':
        num_of_25A_incs += 1

with open(plate_batch_count_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile, delimiter='|')
    writer.writerow(["Inc0_48well_A_Count,Inc0_48well_B_Count,"
                     "Inc15_48well_A_Count,Inc15_48well_B_Count,Inc25_48well_A_Count,"
                     "Inc25_48well_B_Count,"])
    writer.writerow(["{0},0,{1},0,{2},0".format(num_of_0A_incs, num_of_15A_incs, num_of_25A_incs)])

rack_list = []
for plate in barcode_dict:
    rack_list.append(barcode_dict[plate][3])
rack_list = set(rack_list)
rack_list = list(rack_list)
rack_list.sort()

pos_file_creator(gen_file_list[0], num_of_0A_incs, 0)
pos_file_creator(gen_file_list[1], num_of_0B_incs, 0)
pos_file_creator(gen_file_list[2], num_of_15A_incs, 15)
pos_file_creator(gen_file_list[3], num_of_15B_incs, 15)
pos_file_creator(gen_file_list[4], num_of_25A_incs, 25)
pos_file_creator(gen_file_list[5], num_of_25B_incs, 25)

display_results()

# changes
'''
- If gen plate, then write function that prints out 1,1=barcode ie.
- Write code for duplicates in source file that rewrites the source file
- Implement positions for the source file and storex file checkers
- Gave StoreX file its own dictionary ^^^
- 12/4/2020... updated script to display total amount of plates. Simple modification
'''
