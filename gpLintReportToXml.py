import xml.etree.ElementTree as ET

def process_line(line):
    if line.startswith('/'):
        return 'file', line.strip()
    elif line.startswith('✖'):
        return 'summary', line.strip()
    elif line:
        parts = line.strip().split('  ', maxsplit=2)
        loc, severity, message = parts[0], parts[1], parts[2]
        line_num, col_num = map(int, loc.split(':'))
        return 'error', (line_num, col_num, severity, message)
    else:
        return 'empty', None

def process_file(filename):
    root = ET.Element('checkstyle', version="4.3")
    current_file = None
    with open(filename, 'r') as f:
        for line in f:
            line_type, content = process_line(line)
            if line_type == 'file':
                current_file = ET.SubElement(root, 'file', name=content)
            elif line_type == 'error':
                ET.SubElement(current_file, 'error',
                              line=str(content[0]),
                              column=str(content[1]),
                              severity=content[2],
                              message=content[3],
                              source="gplint")
            elif line_type == 'summary':
                summary_file = ET.SubElement(root, 'file', name="✖")
                error_line, error_column = content.count('error'), content.count('warning')
                ET.SubElement(summary_file, 'error',
                              line=str(error_line),
                              column=str(error_column),
                              severity='problems',
                              message=content,
                              source="gplint")
    tree = ET.ElementTree(root)
    tree.write('output.xml', encoding='utf-8', xml_declaration=True)

# Run the function
process_file('lint_output.txt')
