import xml.etree.ElementTree as ET
import re

root = ET.ElementTree('checkstyle', version="4.3")

with open('lint_output.txt', 'r') as f:
    file_elem = None
    for line in f:
        line = line.strip()  # Remove leading/trailing whitespaces

        if line.startswith("/"):
            # It's a file path line
            file_elem = ET.SubElement(root, 'file', name=line)
        elif re.search(r'\d+:\d+\s+error', line):
            # It's an error line
            pattern = r'(?P<line_number>\d+):(?P<column_number>\d+)\s+(?P<severity>\w+)\s+(?P<message>.*)'
            match = re.match(pattern, line)
            if match:
                data = match.groupdict()
                ET.SubElement(file_elem, 'error', line=data['line_number'], column=data['column_number'], severity=data['severity'], message=data['message'], source="gplint")
        elif line.startswith("✖"):
            # It's a summary line
            pattern = r'✖\s+(?P<problems>\d+)\s+problems\s+\((?P<errors>\d+)\s+errors,\s+(?P<warnings>\d+)\s+warnings\)'
            match = re.match(pattern, line)
            if match:
                data = match.groupdict()
                file_elem = ET.SubElement(root, 'file', name="✖")
                ET.SubElement(file_elem, 'error', line=data['problems'], column="0", severity="problems", message=f'({data["errors"]} errors, {data["warnings"]} warnings)', source="gplint")

tree = ET.ElementTree(root)
tree.write('output.xml')
