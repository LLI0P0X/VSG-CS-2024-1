from bs4 import BeautifulSoup

soup = BeautifulSoup(open("temp.html", "r", encoding="utf-8"), features="html.parser")  # htmp parser
table = soup.find_all('table', {'class': "tbl tbl-1-pre tbl-2-pre"})
data_list = []
data = {}
for row in table:
    for q in row.find_all('td'):
        data_list.append(q.text)

keys = data_list[::2]
values = data_list[1::2]
for key in keys:
    data[key] = values.pop(0)
print(data)
