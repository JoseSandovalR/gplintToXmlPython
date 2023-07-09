import xml.etree.ElementTree as ET
import sys

def parse_error_line(line):
    split_line = line.split(' ', 4)
    line_col = split_line[0].split(':')

    if len(line_col) < 2:
        # La línea no tiene el formato esperado, retorna valores predeterminados.
        return "0", "0", "error", line

    severity = split_line[1]
    message = " ".join(split_line[2:]).strip()  # Une todo después de la severidad como mensaje
    return line_col[0], line_col[1], severity, message

def create_error_element(line):
    line_num, col_num, severity, message = parse_error_line(line)
    error = ET.Element("error")
    error.set("line", line_num)
    error.set("column", col_num)
    error.set("severity", severity)
    error.set("message", message)
    error.set("source", "gplint")
    return error

def main():
    checkstyle = ET.Element("checkstyle")
    checkstyle.set("version", "4.3")

    with open(sys.argv[1], "r") as file:
        lines = file.readlines()
        for i in range(0, len(lines), 2):
            file_elem = ET.SubElement(checkstyle, "file")
            file_elem.set("name", lines[i].strip())
            error_elem = create_error_element(lines[i+1])
            file_elem.append(error_elem)

    tree = ET.ElementTree(checkstyle)
    tree.write("report.xml")

if __name__ == "__main__":
    main()
