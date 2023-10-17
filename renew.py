import xml.etree.ElementTree as ET

# 尝试使用不同的编码方式打开文件
encodings = ['utf-8', 'latin-1']

for encoding in encodings:
    try:
        with open(r"C:\Users\ohaiyo\Desktop\license.dat", "r", encoding=encoding) as file:
            xml_data = file.read()
        print("Using encoding:", encoding)
        print("Raw data:", xml_data)
        root = ET.fromstring(xml_data)
        print("Parsed XML:")
        print(ET.tostring(root, encoding='utf-8').decode('utf-8'))
        break
    except (UnicodeDecodeError, ET.ParseError):
        continue









