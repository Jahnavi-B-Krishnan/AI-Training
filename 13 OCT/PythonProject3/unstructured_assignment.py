with open('unstructured_data.txt') as f:
    txt= f.read()
# print(txt)

# words= txt.split()
# print("total no of words:",len(words))

# lines = txt.split('\n')
# print("total no of line:",len(lines))

# if "maintenance" in txt:
#     print("The word 'maintenance' appears in the report.")
# else:
#     print("The word 'maintenance' does not appear in the report.")

# if "conveyor" in txt:
#     print("The word conveyor appears in the report")
# else:
#     print("The word conveyor does not appear in the report")

with open('unstructured_data.txt') as f:
    lines= f.readlines()
# for line in lines:
#     if "team" in line.lower():
#         print(line.strip())

# for i in lines:
#     if "incident" in i:
#         print(i.strip())

# for d in lines:
#     if "damaged" in d:
#         print(d.strip())

# lowercase_data = txt.lower()
#
# with open("lowercase_report.txt", "w") as file:
#     file.write(lowercase_data)

kw=['maintenance','injuries','inspection','replacement','operations']
for w in kw:
    if w in txt:
        print(w,": Found")
    else:
        print(w,": Not Found")