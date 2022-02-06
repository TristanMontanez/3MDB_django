import csv

with open('pricelist.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    price_table = []
    for row in csv_reader:
        price_table.append(row[0:3])

    for row in price_table:
        row[0] = 'product_'+row[0]
        row[1] = row[1].strip()
        row[2] = row[2].strip()
        row[2] = row[2].split('.')[0]
        print(row[2])

with open('new_pricelist.csv', 'w', newline='') as new_csv:
    write = csv.writer(new_csv)
    for row in price_table:
        write.writerow(row)
