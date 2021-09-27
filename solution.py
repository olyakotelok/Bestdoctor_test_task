import csv
import re
import statistics
from statistics import mode

#идея решения - выдвинем гипотезы о данных, проверим их
#на основании результатов будем искать ответ

#cчитаем данные из файла
with open('test_data.csv') as f:
    reader = list(csv.reader(f))


#1. проверим, совпадает ли общая сумма по всем чекам клиентов из реестра
#с суммой  чеков по всем месяцам из отчета
#проверили - совпадает

#2. проверим распределение сумм чеков по месяцам
# Результат - суммы чеков по месяцам январь-июнь меньше, чем суммы в отчете.
#при этом встречаются месяца не только январь-июнь, но и другие
#номера некоторых  месяцов не корректны - 29, 16
#рассуждаем далее в предположении, что все чеки с корректным номером месяца от 1 до 6
#сохранились в реестре без ошибок
#значит, нужно исправить номера месяцев в ошибочных чеках 
#3.заметим, что клиенты записаны в реестре по порядку - выведем список id 
#так же номера месяцев в целом упорядочены, т.е. сначала идет много чеков от 1 месяца, потом от 2-го и тд
#среди них встречаются ошибочные чеки


    #общая cумма чеков по отчету
    summa_report = 0
    sum_for_months_report = {1:[],2:[],3:[], 4:[], 5:[], 6:[]}

    for j in range(2,8):
        a = reader[j][6]
        summa_report += float(a)
        sum_for_months_report[j-1]= float(a)

    #общая cумма чеков по реестру
    summa_table = 0

    #суммы чеков по месяцам из реестра
    sum_for_months_table = dict.fromkeys([i for i in range(50)], 0)

    #дни в каждом месяце, когда были клиенты
    month_days = dict.fromkeys([i for i in range(50)], 0)
    for k,v in month_days.items():
        month_days[k] = []

    #упорядоченный список месяцев по чекам
    arr_month = []

    #упорядоченный список сумм по чекам
    arr_money = []

    #упорядоченнный список id пациентов по чекам
    arr_id = []
    

    for i in range(2, len(reader)):
        row = reader[i]
        arr = row[1].split()

        id_client = arr[1]
        money = float(arr[3])
        date = arr[len(arr)-1].split('.')

        summa_table += money

        month = int(date[1])
        day  = int(date[0])

        sum_for_months_table[month] += money
    
        month_days[month].append(day)

        arr_id.append(id_client)
        arr_month.append(month)
        arr_money.append(money)
        


    #печать результата
    def print_result_table(dictionary, header_table, header_data):
        
        print(header_table)
        print(header_data)
        for k, v in dictionary.items():
            print(k, " - ", v)

    print("Итого по чекам из отчета: ", summa_report)
    print("Итого по чекам из реестра: ", summa_table)
    print()
    print_result_table(sum_for_months_report, "Суммы чеков по месяцам из отчета", "Номер месяца - сумма")
    print()
    print_result_table(sum_for_months_table, "Суммы чеков по месяцам из реестра", "Номер месяца - сумма")
    print()
    print("Список id пациентов")
    print(arr_id)
        



#4. исходя из упорядоченности данных, найдем границы месяцев - id пациентов, которые последние в списке для каждого месяца
    #формируем выходные данные
    #correct_data = [["patient_id", "month", "price"]]
    
    print("сумма за текущий месяц  -   id последнего клиента в текущем месяце")
    s=0
    m=1
    for k in range(len(arr_money)):
        s+=arr_money[k]
        arr_month[k] = m
        if abs(s - sum_for_months_report[m])<0.1:
            #correct_data.append([arr_id[k], m, arr_money[k]])
            m+=1
            print(s, "-", arr_id[k])
            s=0
    
    

#запишем данные в итоговый файл
    
    with open("correct_data.csv", "w", newline='') as answer:
        #writer = csv.writer(answer, delimiter=' ')
        
        writer = csv.DictWriter(answer, fieldnames = ["id", "month", "price"])
        writer.writerow({"id": "id","month":"month","price":"price"})
        for k in range(len(arr_month)):
            writer.writerow({"id": arr_id[k], "month": arr_month[k], "price": float(arr_money[k])})
    print()
    print("data corrected in correct_data.csv")
    
