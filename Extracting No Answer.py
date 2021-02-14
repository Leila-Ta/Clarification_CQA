import xlrd

Dict_responder = {}

out = open("./english.stackexchange.com/Analyse/No_answer.txt", "w")
loc = ("./english.stackexchange.com/Analyse")
wb = xlrd.open_workbook(loc+"/SecondaryUser66_labelled.xlsx")

sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)
i = 0
for i in range(sheet.nrows):
    Dict_responder[sheet.cell_value(i,1)] = 1

wb = xlrd.open_workbook(loc+"/No Answer68_labelled.xlsx")
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)

for i in range(sheet.nrows):
    if (sheet.cell_value(i , 3)) not in Dict_responder.keys():
        print(sheet.cell_value(i,0))
        print(sheet.cell_value(i,1))
        print(sheet.cell_value(i, 2))
        print(sheet.cell_value(i, 3))
        print(sheet.cell_value(i, 4))
        print(sheet.cell_value(i, 5))
        out.write(str(sheet.cell_value(i, 0))+'\t'+str(sheet.cell_value(i, 1))+'\t'+str(sheet.cell_value(i, 2))+'\t'+str(sheet.cell_value(i, 3))+'\t'+str(sheet.cell_value(i, 4))+'\t'+str(sheet.cell_value(i, 5)))
        out.write('\n')

out.close()



