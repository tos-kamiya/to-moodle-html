import sys
import argparse
import re

from bs4 import BeautifulSoup
from markdown import markdown
from latex2mathml.converter import convert as l2m_convert

try:
    from .__about__ import __version__
except:
    __version__ = "(unknown)"


def split_code_block_iter(lines):
    in_code_block = False
    for line in lines:
        m = re.match(r"^```\s*(.*)", line)
        if m:
            additional_desc = m.group(1)
            if additional_desc:
                in_code_block = True
                yield None, line
            else:
                if not in_code_block:
                    in_code_block = True
                    yield None, line
                else:
                    in_code_block = False
                    yield None, line
        else:
            if not in_code_block:
                yield line, None
            else:
                yield None, line


def format_latex_math_blocks(text):
    """
    Align the format of LaTeX equations.
    Convert inline math `$...$` and block math `$$...$$` in to MathML.
    """

    double_dollar_count = text.count("$$")
    if double_dollar_count % 2 != 0:
        raise ValueError("The number of '$$' symbols is odd.")

    def replace_block_math(match):
        s = match.group(1)
        return l2m_convert(s, display="block")

    text = re.sub(r"\$\$(.+?)\$\$", replace_block_math, text, flags=re.DOTALL | re.MULTILINE)

    it = split_code_block_iter(text.split("\n"))
    r = []
    for i, (line, code_block_line) in enumerate(it):
        if line is None:
            assert code_block_line is not None
            r.append(code_block_line)
            continue

        single_dollar_count = line.count("$")
        if single_dollar_count % 2 != 0:
            raise ValueError("The number of '$' symbols is odd: {line}")

        # Convert inline math $...$
        def replace_inline_math(match):
            s = match.group(1)
            return l2m_convert(s, display="inline")

        line = re.sub(r"\$(.+?)\$", replace_inline_math, line)
        r.append(line)

    return "\n".join(r)


def main():
    import os
    parser = argparse.ArgumentParser(description="Convert markdown to Moodle-ish html")
    parser.add_argument(
        "inputmd",
        type=str,
        help='Markdown file to process. "-" for read from the standard input)',
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-o", dest="output", type=str, help="Specify output file name")
    group.add_argument(
        "-O",
        dest="auto_out",
        action="store_true",
        help="Automatically set output file name by replacing input file's extension with .html (cannot be used with standard input)",
    )
    parser.add_argument("--version", action="version", version="%(prog)s " + __version__)

    args = parser.parse_args()

    if args.inputmd == "-":
        text = sys.stdin.read()
    else:
        with open(args.inputmd, "r", encoding="utf-8") as inp:
            text = inp.read()

    if args.output:
        output_filename = args.output
    elif args.auto_out:
        if args.inputmd == "-":
            print("Error: -O option cannot be used with standard input", file=sys.stderr)
            sys.exit(1)
        base, _ = os.path.splitext(args.inputmd)
        output_filename = base + ".html"
    else:
        output_filename = "-"

    # Properly convert the format of LaTeX equations
    try:
        text = format_latex_math_blocks(text)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Convert Markdown to HTML
    html = markdown(text, extensions=["fenced_code", "tables"])
    soup = BeautifulSoup(html, "html.parser")

    # Add border attribute to tables
    tables = soup.find_all("table")
    for t in tables:
        t.attrs["border"] = "1"

    # Add style to <pre> tags
    pres = soup.find_all("pre")
    for t in pres:
        s = t.attrs.setdefault("style", "")
        s = s.rstrip()
        if s and not s.endswith(";"):
            s = s + ";"
        t.attrs["style"] = s + "background-color: #e8e8e8; padding: 10px;"

    output_text = soup.prettify()

    if output_filename != "-":
        with open(output_filename, "w", encoding="utf-8") as out:
            out.write(output_text)
    else:
        print(output_text)


if __name__ == "__main__":
    main()
