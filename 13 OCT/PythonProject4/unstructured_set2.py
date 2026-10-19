with open("airport_operations_report.txt","r") as f:
    txt=f.read()

# print("Total words:",len(txt.split()))
# print("Total line:",len(txt.splitlines()))
# print("Total characters:",len(txt))

txt_lower=txt.lower()
# words=['flight','runway','operations','reported']
# for w in words:
#     count = txt_lower.split().count(w)
#     print(f"{w}: {count}")

with open("airport_operations_report.txt") as f:
    lines= f.readlines()
# for line in lines:
#     if "runway" in line.lower():
#         print(line.strip())

keywords = ["delay", "delayed", "delays"]
# for line in lines:
#     if any(word in line.lower() for word in keywords):
#         print(line.strip())

# for line in lines:
#     if "reported" in line.lower():
#         print(line.strip())

# wd=["emergency","inspection","weather","passengers","maintenance"]
# for w in wd:
#     if w in txt_lower:
#         print(w,": Found")
#     else:
#         print(w,": Not Found")

words =txt_lower.split()
# word_counts = {
#     "flight": words.count("flight"),
#     "runway": words.count("runway"),
#     "operations": words.count("operations")
# }
# print(word_counts)

# print(max(lines, key=len))

filtered_lines = [
    line for line in lines
    if any(keyword in line.lower() for keyword in keywords)
]

with open("filtered_airport_report.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(filtered_lines))




