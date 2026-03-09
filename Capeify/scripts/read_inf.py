import csv
from os import read


def read_strings(path):
    with open(path, "r") as f:
        strings = {}
        in_strings = False
        for line in f.readlines():
            line = line.strip()

            if in_strings and line.strip() != "":
                key, val = line.split("=")
                key, val = key.strip(), val.strip()

                strings[key] = val[1:-1]

            if line != "" and len(line) >= 2:
                if line[0] == "[" and line[-1] == "]" and in_strings:
                    break

            if line == "[Strings]":
                in_strings = True

    return strings


def read_defaultInstall(path):
    dict_ = {}
    in_defaultInstall = False
    with open(path, "r") as f:
        for line in f.readlines():
            if line != "" and len(line) >= 2:
                if (
                    line.strip()[0] == "["
                    and line.strip()[-1] == "]"
                    and in_defaultInstall
                ):
                    break

            if in_defaultInstall and line.strip() != "":
                key, val = line.strip().split("=")
                key, val = key.strip().replace(",", ""), val.strip().replace(",", "")

                dict_[key] = val

            if "[DefaultInstall" in line.strip():
                in_defaultInstall = True

    return dict_


def read_reg(path, reg_sect):
    in_reg = False
    with open(path, "r") as f:
        for line in f.readlines():
            stripped = line.strip()

            if in_reg and stripped != "" and not stripped.startswith(";"):
                read_csv = csv.reader([stripped])
                read_csv = next(read_csv)
                reg_str = read_csv[-1]

                curs = reg_str.split(",")
                # Handle both quoted ("pointer") and unquoted (pointer) formats
                # Also handle escaped paths like "%10%\%CUR_DIR%\%pointer%"
                cleaned = []
                for cur in curs:
                    cur = cur.strip()
                    # Remove quotes if present
                    if cur.startswith('"') and cur.endswith('"'):
                        cur = cur[1:-1]
                    # Take last component after backslash
                    cur = cur.split("\\")[-1]
                    # Remove surrounding % if variable reference
                    if cur.startswith("%") and cur.endswith("%"):
                        cur = cur[1:-1]
                    cleaned.append(cur)

                return cleaned

            if stripped == f"[{reg_sect}]":
                in_reg = True
