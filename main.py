import pdfx

#reading
pdf = pdfx.PDFx("zadania_domowe_3-12.pdf")
#metadata
#print(pdf.get_metadata())

print(pdf.get_text())