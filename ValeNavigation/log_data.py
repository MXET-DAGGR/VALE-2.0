#this script contains functions to log route datas.

import xlsxwriter

#create a function that logs list of points into an .xlsx file
def pointsToExcel(points, fileName):

    workbook = xlsxwriter.Workbook('/Users/allenliu/CapstoneCode/TempFiles/'+fileName+'.xlsx')
    worksheet = workbook.add_worksheet()

    column = 0
    for x in range(2):
        row = 0
        for item in points:             #going through each pair of points in "points". First going thru first value, then second
            worksheet.write(row, column, item[column])
            row+=1 
        column+=1

    workbook.close()


if __name__ == "main":
    test_item = [[1,2],[3,4],[5,6],[7,8],[9,10],[11,10]]
    pointsToExcel(test_item)

