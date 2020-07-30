import csv

held_rows = []

with open('/Users/allanrios/Desktop/BarcodeProtocol.csv', newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ')
    for row in reader:
        new_row = row
        held_rows.append("".join(new_row))

if len(held_rows) < 170:
    for i in range(len(held_rows), 170):
        held_rows.append('')

final_list = []

counter = 0
for x in range(1, 11):
    for y in range(1, 18):
        final_list.append(["{0},{1}={2}".format(x, y, held_rows[counter])])
        counter += 1

with open('/Users/allanrios/Desktop/FinalProtocol.csv', 'w', newline='', encoding='utf-8-sig') as csvfile2:
    writer = csv.writer(csvfile2, delimiter=' ')
    for i in range(len(final_list)):
        writer.writerows([final_list[i]])

