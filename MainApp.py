import csv
"""
The overall purpose of this project was to reformat scanned barcodes from a csv file into another csv file.
This was needed as an alternative to a failed database we were dealing with. This app pretty much automates
copying and pasting the barcodes into the desired format. This format was needed as part of a Tecan automation
system, being that the system is particular on how it accepts input from a barcode scanner.
"""

held_rows = []   # This list will be used to copy the barcode values from the original barcode sheet

with open('/Users/allanrios/Desktop/BarcodeProtocol.csv', newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ')
    for row in reader:
        new_row = row
        held_rows.append("".join(new_row))

# The amount of barcodes will never surpass 170
# These 3 lines of code assign no value to any remaining spots that are scanned through the Tecan system
# The format calls for exactly 170 values, and if no barcode is associated, then it needs to show up with a blank value
if len(held_rows) < 170:
    for i in range(len(held_rows), 170):
        held_rows.append('')

final_list = [] # List that will be written to the needed source file

# The exact format is "rackNumber,slotNumber=barcode"
counter = 0
for x in range(1, 11): # Represents 10 racks
    for y in range(1, 18): # Represents 17 slots per rack
        final_list.append(["{0},{1}={2}".format(x, y, held_rows[counter])])
        counter += 1
# Accesses the file needed to be read by Tecan automation system and writes to it
with open('/Users/allanrios/Desktop/FinalProtocol.csv', 'w', newline='', encoding='utf-8-sig') as csvfile2:
    writer = csv.writer(csvfile2, delimiter=' ')
    for i in range(len(final_list)):
        writer.writerows([final_list[i]])

