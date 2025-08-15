import re


barcode = "M:019923303151P:5501901700D:VS-2334S:000070C:PWB ASSY MB WDQ031-MRKI 04X"

barcode = "M:01992330315501901700D:VS-2334S:000070C:PWB ASSY MB WDQ031-MRKI 04X"
match = re.search(r'([Mm]:(?P<wo_no>[A-Z0-9]+)P.+[Ss]:(?P<no>[0-9]+))|(?P<barcode_09>\d{16,18}[Pp]:\d{10})', barcode)
escape.group("wo_no")
code_9_split_item = match.fullmatch(barcode)
barcode_09 = '{}{}'.format(code_9_split_item[0][1], code_9_split_item[0][2])

