import xml.etree.ElementTree as ET

def process_file(file_name):
    root = ET.Element("checkstyle", version="4.3")

    with open(file_name, "r") as f:
        lines = f.readlines()

    file_elem = None
    for line in lines:
        line = line.strip()
        if line.startswith("/"):
            if file_elem is not None:
                root.append(file_elem)
            file_elem = ET.Element("file", name=line)
        elif line.startswith("✖"):
            problems_line = line.split(" ")[1:]
            problems_count = problems_line[0]
            problems_message = " ".join(problems_line[1:])
            root.set("errors", problems_count)
            root.set("warnings", "0")
            root.set("version", "4.3")
            root.set("timestamp", "")
            root.set("severity", "")
            root.set("name", "")
            root.set("totalerrors", problems_count)
            root.set("totalwarnings", "0")
            root.set("totalfixes", "")
            root.set("fixableerrors", "")
            root.set("fixablewarnings", "")
            root.set("fixable", "")
            root.set("configlocation", "")

            if file_elem is not None:
                root.append(file_elem)
            break
        else:
            parts = line.split("  ", 1)
            if len(parts) == 2:
                loc, message = parts
                if ":" in loc:
                    line, column = loc.split(":")
                    error_elem = ET.Element("error", line=line.strip(), column=column.strip(), severity="error", message=message.strip(), source="gplint")
                    file_elem.append(error_elem)

    tree = ET.ElementTree(root)
    tree.write("output.xml", xml_declaration=True, encoding="utf-8")

process_file("lint_output.txt")
