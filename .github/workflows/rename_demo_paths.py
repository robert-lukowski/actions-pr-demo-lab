from pathlib import Path


SCHEMA_PATTERN = "tools/**/schema.yaml"


def leading_spaces(line):
    return len(line) - len(line.lstrip(" "))


def rename_paths_in_schema(path):
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    changed = False
    in_paths = False
    paths_indent = None
    path_key_indent = None

    for index, line in enumerate(lines):
        stripped = line.lstrip(" ")

        if not stripped or stripped.startswith("#"):
            continue

        indent = leading_spaces(line)

        key_name = stripped.partition(":")[0]

        if indent == 0 and key_name == "paths":
            in_paths = True
            paths_indent = indent
            path_key_indent = None
            continue

        if in_paths and indent <= paths_indent and key_name != "paths":
            in_paths = False
            paths_indent = None
            path_key_indent = None

        if not in_paths:
            continue

        if indent <= paths_indent:
            continue

        if path_key_indent is None:
            path_key_indent = indent

        if indent != path_key_indent:
            continue

        if not stripped.startswith("/demo-"):
            continue

        key, separator, rest = stripped.partition(":")
        if not separator:
            continue

        new_key = key.replace("/demo-", "/release-", 1)
        lines[index] = f"{line[:indent]}{new_key}:{rest}"
        changed = True

    if changed:
        path.write_text("".join(lines), encoding="utf-8")

    return changed


def main():
    modified_files = []

    for schema_path in sorted(Path(".").glob(SCHEMA_PATTERN)):
        if rename_paths_in_schema(schema_path):
            modified_files.append(schema_path.as_posix())

    if modified_files:
        print("Modified files:")
        for modified_file in modified_files:
            print(f"- {modified_file}")
    else:
        print("No schema path changes were needed.")


if __name__ == "__main__":
    main()
