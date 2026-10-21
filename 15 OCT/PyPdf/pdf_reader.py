import fitz
doc = fitz.open("EY_Digital_PDF_Practice.pdf")
# print("Pages:", len(doc))

#print(doc[0].get_text())

# for page in doc:
#     print(page.get_text())

all_text = ""
for page in doc:
    all_text += page.get_text()
# if "maintenance" in all_text.lower():
#     print("The word maintenance is present")
# else:
#     print("The word maintenance is not present")

# print("Count of V303:",all_text.count("V303"))

with open("digital_pdf_text.txt", "w") as f:
    f.write(all_text)