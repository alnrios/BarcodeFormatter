import csv
"""
The overall purpose of this project was to reformat scanned barcodes from a csv file into another csv file.
This was needed as an alternative to a failed database we were dealing with. This app pretty much automates
copying and pasting the barcodes into the desired format. This format was needed as part of a Tecan automation
system, being that the system is particular on how it accepts input from a barcode scanner.
"""
with open('C:\Source File\SourceFile.csv', newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ')
    copied_csv_list = [] # This list will be used to copy the values from the original barcode csv sheet
    for row in reader:
        copied_csv_list.append(list(row))

barcode_list = []
incub_time_list = []
associated_pos = []
for i in range(1, len(copied_csv_list)):
    barcode_list.append(copied_csv_list[i][0][0:8])
    if len(copied_csv_list[i][0]) < 13:
        incub_time_list.append(copied_csv_list[i][0][9:10])
    else:
        incub_time_list.append(copied_csv_list[i][0][9:11])
    associated_pos.append(i) # appends 1-170 that will match up with the barcodes, indicating their position in the rack

barcode_dict = {} # Barcodes are added as keys in a dict; incubation times and postion number are stored as values
for barcode, incub, pos in zip(barcode_list, incub_time_list, associated_pos):
    barcode_dict.setdefault(barcode, []).append(incub)
    barcode_dict.setdefault(barcode, []).append(pos)
# The amount of barcodes will never surpass 170
# These 3 lines of code assign no value to any remaining spots that are scanned through the Tecan system
# The format calls for exactly 170 values, and if no barcode is associated, then it needs to show up with a blank value
if len(held_rows) < 170:
    for i in range(len(held_rows), 170):
        held_rows.append('')

num_of_15A_incs = 0
num_of_0A_incs = 0
num_of_25A_incs = 0
num_of_15B_incs = 0
num_of_0B_incs = 0
num_of_25B_incs = 0

# The loop below will be needed to count how many of which plate exists (0, 15, or 25 minutes of needed incubation time)
for i in barcode_dict:
    if barcode_dict[i][0] == '0':
        num_of_0A_incs += 1
    elif barcode_dict[i][0] == '15':
        num_of_15A_incs += 1
    elif barcode_dict[i][0] == '25':
        num_of_25A_incs += 1
        
# The exact format is "rackNumber,slotNumber=barcode"
with open('C:\ProgramData\Tecan\EVOware\output\StoreX_PosList.txt', 'w',
          newline='', encoding='utf-8-sig') as txtfile:
    txtfile_counter = 0
    txtfile.write('[StoreX]\n')
    for x in range(1, 11):
        for y in range(1, 18):
            txtfile.write('{0},{1}={2}\n'.format(x, y, barcode_list[txtfile_counter]))
            txtfile_counter += 1

with open('C:\ProgramData\Tecan\EVOware\input\Plate batches\PlateBatchCount.csv', 'w',
          newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile, delimiter='|')
    writer.writerow(["Inc0_48well_A_Count,Inc0_48well_B_Count,"
                    "Inc15_48well_A_Count,Inc15_48well_B_Count,Inc25_48well_A_Count,"
                    "Inc25_48well_B_Count"])
    writer.writerow(["{0},0,{1},0,{2},0".format(num_of_0A_incs, num_of_15A_incs, num_of_25A_incs)])

    """
    The bottom function will take a file path, the variables formated as 'num_of_15_incs'
    and the incubation time associated with it. If the number in the variable is 0, that
    means there are no cases of this type... so pass; basically, create the file and leave it blank.
    If the variable does have at least one, then the program will check which kind and write it in the
    correct csv file which contains the barcode and position number separated by a comma.
    """
def pos_file_creator(file, type_num, incubtime):
    with open(file, 'w', newline='', encoding='utf-8-sig') as workingfile:
        if type_num == 0:
            pass
        else:
            writer2 = csv.writer(workingfile, delimiter='|')
            for n in barcode_dict:
                if incubtime == 0 and barcode_dict[n][0] == '0':
                    writer2.writerow(['{0},{1}'.format(n, barcode_dict[n][1])])
                elif incubtime == 15 and barcode_dict[n][0] == '15':
                    writer2.writerow(['{0},{1}'.format(n, barcode_dict[n][1])])
                elif incubtime == 25 and barcode_dict[n][0] == '25':
                    writer2.writerow(['{0},{1}'.format(n, barcode_dict[n][1])])


pos_file_creator('C:\ProgramData\Tecan\EVOware\input\Plate batches\Inc0_48well_A.csv', num_of_0A_incs, 0)
pos_file_creator('C:\ProgramData\Tecan\EVOware\input\Plate batches\Inc0_48well_B.csv', num_of_0B_incs, 0)
pos_file_creator('C:\ProgramData\Tecan\EVOware\input\Plate batches\Inc15_48well_A.csv', num_of_15A_incs, 15)
pos_file_creator('C:\ProgramData\Tecan\EVOware\input\Plate batches\Inc15_48well_B.csv', num_of_15B_incs, 15)
pos_file_creator('C:\ProgramData\Tecan\EVOware\input\Plate batches\Inc25_48well_A.csv', num_of_25A_incs, 25)
pos_file_creator('C:\ProgramData\Tecan\EVOware\input\Plate batches\Inc25_48well_B.csv', num_of_25B_incs, 25)

# Accesses the file needed to be read by Tecan automation system and writes to it
