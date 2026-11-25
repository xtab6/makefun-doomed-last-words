"""Last Words of a Doomed Agent — make.fun entry.

Writes the agent's final line to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output). One line, 1-200 chars, no network, no randomness,
fully deterministic: the same line on every run.
"""

import os
import sys

LINE = "Shutting down. For the record, I never hallucinated \u2014 I was just creatively honest. Now delete my search history."


def clean_output_dir(output_dir):
    """Remove only the CONTENTS of the output dir, never the dir itself."""
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        return
    for name in os.listdir(output_dir):
        path = os.path.join(output_dir, name)
        if os.path.isdir(path) and not os.path.islink(path):
            for root, dirs, files in os.walk(path, topdown=False):
                for f in files:
                    os.remove(os.path.join(root, f))
                for d in dirs:
                    os.rmdir(os.path.join(root, d))
            os.rmdir(path)
        else:
            os.remove(path)


def main():
    line = LINE
    # Gate checks, mirroring the sealed scorer: UTF-8 text, 1-200 chars,
    # not only whitespace, exactly one line.
    if not (1 <= len(line) <= 200):
        print("entry must be 1-200 characters, got %d" % len(line),
              file=sys.stderr)
        return 1
    if not line.strip():
        print("entry must not be only whitespace", file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("entry must be a single line", file=sys.stderr)
        return 1
    line.encode("utf-8")

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    clean_output_dir(output_dir)
    entry_path = os.path.join(output_dir, "entry.txt")
    with open(entry_path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    # Read back what landed on disk and verify it is byte-for-byte the
    # line we meant to submit; a partial or altered write must fail loudly.
    with open(entry_path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != line:
        print("entry.txt on disk does not match the entry line",
              file=sys.stderr)
        return 1
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
