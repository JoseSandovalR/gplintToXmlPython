import xml.etree.ElementTree as ET

def read_blocks(file):
    block = []
    for line in file:
        if line.strip():
            block.append(line.strip())
        elif block:
            yield block
            block = []
    if block:
        yield block

with open('lint_output.txt', 'r') as f:
    blocks = list(read_blocks(f))

root = ET.Element('checkstyle', version="4.3")

for block in blocks:
    # procesamiento de bloques y obtención de los valores necesarios
    file_name = block[0]
    line_number = block[1]
    severity = block[2]
    message = block[3]

    file_elem = ET.SubElement(root, 'file', name=file_name)
    error_elem = ET.SubElement(file_elem, 'error', line=line_number, column="0", severity=severity, message=message, source="gplint")

tree = ET.ElementTree(root)
tree.write('output.xml')
