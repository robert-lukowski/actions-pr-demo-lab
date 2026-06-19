from pathlib import Path


SCHEMA_PATTERN = "tools/**/schema.yaml"


def leading_spaces(line):
    return len(line) - len(line.lstrip(" "))


def update_schema_paths(path):
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

        key, separator, rest = stripped.partition(":")
        if not separator or "nprod" not in key:
            continue

        new_key = key.replace("nprod", "prod")
        if new_key == key:
            continue

        lines[index] = f"{line[:indent]}{new_key}:{rest}"
        changed = True

    if changed:
        path.write_text("".join(lines), encoding="utf-8")

    return changed


def main():
    updated_files = []

    for schema_path in sorted(Path(".").glob(SCHEMA_PATTERN)):
        if update_schema_paths(schema_path):
            updated_files.append(schema_path.as_posix())

    if updated_files:
        print("Updated files:")
        for updated_file in updated_files:
            print(f"- {updated_file}")
    else:
        print("No schema path changes were needed.")


if __name__ == "__main__":
    main()
