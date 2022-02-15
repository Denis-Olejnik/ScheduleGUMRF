import datetime
import makara


weekdays = {1:"Понедельник",2:"Вторник",3:"Среда",4:"Четверг",5:"Пятница",6:"Суббота",7:"Воскресенье"}
deno_nume = {1:"Числитель",0:"Знаменатель"}
final_print = {}

reader = datetime.datetime.today().isocalendar()[2]
week = datetime.datetime.today().isocalendar()[1]


print("Сегодня:",weekdays[reader],end=", ")

final = int(week) % 2

print(deno_nume[final],"\n")

c = 1

if int(reader) == 1:
	handler = makara.numerator[reader-1]
	for i in range(0,len(makara.numerator[reader])):
		print(str(c)+")",handler[i])
		c+=1
else:
	handler = makara.denominator[reader-1]
	for i in range(0,len(makara.denominator[reader])):
		print(str(c)+")",handler[i])
		c+=1
# Any