# to-moodle-html

**to-moodle-html** is a command-line tool that converts Markdown documents into Moodle-compatible HTML. It is especially useful for educators and developers who work with Moodle and need to integrate rich text content with formatted code blocks, tables, and mathematical equations.

## Features

- **Markdown to HTML Conversion:**  
  Transforms Markdown files into HTML using the Python Markdown library with support for fenced code blocks and tables.

- **LaTeX Math to MathML Conversion:**  
  Automatically converts both inline (`$...$`) and block (`$$...$$`) LaTeX math expressions into MathML using the `latex2mathml` converter, ensuring mathematical content is displayed properly.

- **Enhanced HTML Styling:**  
  Utilizes BeautifulSoup to:
  - Add a border to all tables.
  - Apply a background color and padding to `<pre>` tags for better readability of code blocks.

- **Error Checking:**  
  Validates the correct pairing of math delimiters (`$` and `$$`) and reports errors if mismatches are found.

## Installation

You can install **to-moodle-html** easily using pipx:

```bash
pipx install git+http://github.com/tos-kamiya/to-moodle-html
```

Alternatively, clone the repository and install with pip:

```bash
git clone http://github.com/tos-kamiya/to-moodle-html
cd to-moodle-html
pip install .
```

## Usage

After installation, use the command-line tool to convert Markdown to HTML. The tool supports two options for specifying the output file:

**Specify an output file manually:**  

Use the `-o` option followed by the desired file name.
  
  ```bash
  to-moodle-html input.md -o output.html
  ```

**Automatically set the output file name:**  

Use the `--auto-out` option to have the tool automatically replace the input file's extension with `.html`.  

  **Note:** This option cannot be used when reading from standard input.
  
  ```bash
  to-moodle-html input.md --auto-out
  ```

If no output option is specified, the resulting HTML is printed to standard output:

```bash
to-moodle-html input.md > output.html
```

For standard input usage:

```bash
cat input.md | to-moodle-html -
```

## Requirements

- **Python:** Version 3.10 or higher.
- **Dependencies:**
  - [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
  - [Markdown](https://python-markdown.github.io/)
  - [latex2mathml](https://github.com/martinrusev/latex2mathml)  

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
