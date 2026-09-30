"""CLI for the Definition Editor.

Usage:
    py definition_editor/cli.py --dir <application_definitions_path> <command> [args]

Commands:
    list [--prefix webflux|react]           List definition files
    aliases [--prefix wf|rx]                List available aliases
    get <file> [path]                       Read a value
    set <file> <path> <value_json>          Set a value
    update <file> <path|-> <updates_json>   Merge updates (use - for root)
    delete <file> <path>                    Delete a value
    append <file> <path|-> <value_json>     Append to array (use - for root array)
    find <file> <path|-> <predicate_json>   Find first match in array
    filter <file> <path|-> <predicate_json> Filter matches in array
    exists <file> [path]                    Check existence
    diff <file> [path] --other <dir>        Compare with another definitions dir
    backup <file>                           Create timestamped backup
    restore <backup_file>                   Restore from backup
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from definition_editor.editor import DefinitionEditor


def _parse_json_arg(s: str) -> any:
    """Parse a CLI argument as JSON, falling back to string."""
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        return s


def _print_json(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description="Definition Editor — JSON CRUD for webflux + react application definitions"
    )
    parser.add_argument("--dir", required=True, help="Path to application_definitions/ folder")
    sub = parser.add_subparsers(dest="command")

    # list
    p_list = sub.add_parser("list", help="List definition files")
    p_list.add_argument("--prefix", default=None, help="Filter: webflux or react")

    # aliases
    p_aliases = sub.add_parser("aliases", help="List aliases")
    p_aliases.add_argument("--prefix", default=None, help="Filter: wf or rx")

    # get
    p_get = sub.add_parser("get", help="Read a value")
    p_get.add_argument("file", help="File name or alias (e.g. rx:theme)")
    p_get.add_argument("path", nargs="?", default=None, help="Dot/bracket path")

    # set
    p_set = sub.add_parser("set", help="Set a value")
    p_set.add_argument("file")
    p_set.add_argument("path")
    p_set.add_argument("value", help="JSON value")

    # update
    p_upd = sub.add_parser("update", help="Merge updates into an object")
    p_upd.add_argument("file")
    p_upd.add_argument("path", help="Dot path or - for root")
    p_upd.add_argument("updates", help="JSON object to merge")

    # delete
    p_del = sub.add_parser("delete", help="Delete a value")
    p_del.add_argument("file")
    p_del.add_argument("path")

    # append
    p_app = sub.add_parser("append", help="Append to an array")
    p_app.add_argument("file")
    p_app.add_argument("path", help="Dot path to array or - for root")
    p_app.add_argument("value", help="JSON value to append")

    # find
    p_find = sub.add_parser("find", help="Find first match in array")
    p_find.add_argument("file")
    p_find.add_argument("path", help="Dot path to array or - for root")
    p_find.add_argument("predicate", help="JSON predicate object")

    # filter
    p_filt = sub.add_parser("filter", help="Filter matches in array")
    p_filt.add_argument("file")
    p_filt.add_argument("path", help="Dot path to array or - for root")
    p_filt.add_argument("predicate", help="JSON predicate object")

    # exists
    p_ex = sub.add_parser("exists", help="Check existence")
    p_ex.add_argument("file")
    p_ex.add_argument("path", nargs="?", default=None)

    # diff
    p_diff = sub.add_parser("diff", help="Compare with another definitions dir")
    p_diff.add_argument("file")
    p_diff.add_argument("path", nargs="?", default=None)
    p_diff.add_argument("--other", required=True, help="Other application_definitions/ path")

    # backup
    p_bak = sub.add_parser("backup", help="Create timestamped backup")
    p_bak.add_argument("file")

    # restore
    p_res = sub.add_parser("restore", help="Restore from backup")
    p_res.add_argument("backup_file")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    editor = DefinitionEditor(args.dir)

    try:
        if args.command == "list":
            for f in editor.list_files(args.prefix):
                print(f"  {f}")

        elif args.command == "aliases":
            for alias, fname in editor.list_aliases(args.prefix).items():
                print(f"  {alias:25s} → {fname}")

        elif args.command == "get":
            _print_json(editor.get(args.file, args.path))

        elif args.command == "set":
            editor.set(args.file, args.path, _parse_json_arg(args.value))
            print(f"  ✅ Set {args.file} → {args.path}")

        elif args.command == "update":
            path = None if args.path == "-" else args.path
            editor.update(args.file, path, json.loads(args.updates))
            print(f"  ✅ Updated {args.file} → {args.path}")

        elif args.command == "delete":
            editor.delete(args.file, args.path)
            print(f"  ✅ Deleted {args.file} → {args.path}")

        elif args.command == "append":
            path = "" if args.path == "-" else args.path
            editor.append(args.file, path, _parse_json_arg(args.value))
            print(f"  ✅ Appended to {args.file} → {args.path}")

        elif args.command == "find":
            path = "" if args.path == "-" else args.path
            result = editor.find(args.file, path, json.loads(args.predicate))
            if result:
                _print_json(result)
            else:
                print("  Not found")

        elif args.command == "filter":
            path = "" if args.path == "-" else args.path
            results = editor.filter(args.file, path, json.loads(args.predicate))
            _print_json(results)
            print(f"  ({len(results)} matches)")

        elif args.command == "exists":
            if editor.exists(args.file, args.path):
                print(f"  ✅ Exists")
            else:
                print(f"  ❌ Not found")
                sys.exit(1)

        elif args.command == "diff":
            result = editor.diff(args.file, args.path, args.other)
            if result["equal"]:
                print("  ✅ Equal")
            else:
                print("  LEFT:")
                _print_json(result["left"])
                print("  RIGHT:")
                _print_json(result["right"])

        elif args.command == "backup":
            bak = editor.backup(args.file)
            print(f"  ✅ Backup: {bak}")

        elif args.command == "restore":
            restored = editor.restore(args.backup_file)
            print(f"  ✅ Restored: {restored}")

    except FileNotFoundError as e:
        print(f"  ❌ {e}", file=sys.stderr)
        sys.exit(1)
    except (KeyError, IndexError, ValueError) as e:
        print(f"  ❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
