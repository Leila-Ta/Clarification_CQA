import xlrd

Dict_overlap = {}
out = open("/Users/leila/PycharmProjects/StackExchange/Result/Culture-Recreation/english.stackexchange.com/Analyse/overlap(asker-responder).txt", "w")
loc = ("/Users/leila/PycharmProjects/StackExchange/Result/Culture-Recreation/english.stackexchange.com/Analyse/ClarqMainUser67_labelled.xlsx")

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

for i in range(sheet.nrows):
    print(sheet.cell_value(i, 1))
    z = (sheet.cell_value(i,1)).lower()
    Dict_overlap[z]=1

locsec = ("/Users/leila/PycharmProjects/StackExchange/Result/Culture-Recreation/english.stackexchange.com/Analyse/SecondaryUser66_labelled.xlsx")

wb = xlrd.open_workbook(locsec)
sheet = wb.sheet_by_index(0)

for i in range(sheet.nrows):
    print(sheet.cell_value(i, 1))
    z = (sheet.cell_value(i, 1)).lower()
    if (z in Dict_overlap.keys()):
        out.write(sheet.cell_value(i, 1))
        out.write('\n')

out.close()
