import xml.etree.ElementTree as ET
import re

root = ET.Element('checkstyle', version="4.3")

with open('lint_output.txt', 'r') as f:
    file_elem = None
    for line in f:
        line = line.strip()  # Remove leading/trailing whitespaces

        if line.startswith("/"):
            # It's a file path line
            file_elem = ET.SubElement(root, 'file', name=line)
        elif re.search(r'\d+:\d+\s+error', line):
            # It's an error line
            line_number, column_number, severity, message = re.search(r'(\d+):(\d+)\s+(\w+)\s+(.*)', line).groups()
            ET.SubElement(file_elem, 'error', line=line_number, column=column_number, severity=severity, message=message, source="gplint")
        elif line.startswith("✖"):
            # It's a summary line
            problems, errors, warnings = re.search(r'✖ (\d+) problems \((\d+) errors, (\d+) warnings\)', line).groups()
            file_elem = ET.SubElement(root, 'file', name="✖")
            ET.SubElement(file_elem, 'error', line=problems, column="0", severity="problems", message=f'({errors} errors, {warnings} warnings)', source="gplint")

tree = ET.ElementTree(root)
tree.write('output.xml', xml_declaration=True, encoding='utf-8')
