import sys
import xml.etree.ElementTree as ET

def parse_error_line(line):
    split_line = line.split(' ', 3)
    line_col = split_line[0].split(':')

    if len(line_col) < 2:
        # La línea no tiene el formato esperado, retorna valores predeterminados.
        return "0", "0", "error", line

    severity = split_line[1]
    message = split_line[2].strip()
    return line_col[0], line_col[1], severity, message

def main():
    checkstyle = ET.Element('checkstyle', version='4.3')

    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('/'):
            filename = line

            file = ET.SubElement(checkstyle, 'file', name=filename)
            i += 1

            while i < len(lines) and not lines[i].strip().startswith('/'):
                line_num, col_num, severity, message = parse_error_line(lines[i])

                ET.SubElement(file, 'error',
                              line=line_num,
                              column=col_num,
                              severity=severity,
                              message=message,
                              source='gplint')
                i += 1
        else:
            i += 1

    tree = ET.ElementTree(checkstyle)
    tree.write('report.xml')

if __name__ == "__main__":
    main()
