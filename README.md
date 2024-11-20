I created this to have a couple of simple command line applications for printing labels with my DYMO label printer.  They are quite handy.  I had been using an application called gLabels to accomplish this, however, an update to that application completely changed the way it works.  My old templates would cause the application to crash when loaded, and it completely changed all the command line parameters such that my command line options no longer worked.

So I attempted to have ChatGPT generate some applications that would just do what I wanted.  This project represents the result of a lenghty converstaion with ChatGPT.  It was able to generate an almost complete application of this complexity.  There were several bugs, but it was able to fix most of them simply by me mentioning the error it was producing.  Others I had to troubleshoot myself and tell it exactly what to change.  But it took on those changes and improved upon them.  

I've only modified a few names and default values from the generated code.  Otherwise every bit of this is the product of generative AI, including the rest of this README.  

# Label Printing Applications

This repository contains two applications for printing labels to a DYMO label printer:

1. **`filelabeler`** - Prints custom labels based on text input.
2. **`addresslabeler`** - Prints address labels from input containing multiple addresses.

Both applications can automatically detect a DYMO printer if one is available or allow you to specify a printer manually.

## Installation

After building the executables with `build.sh`, the applications will be available in `~/.local/bin`. Ensure this directory is in your `PATH` environment variable:

```bash
export PATH=$PATH:~/.local/bin
```

## Applications

### 1. `filelabeler`

This application prints labels using custom text provided via command-line arguments or `stdin`.

#### Usage

```bash
filelabeler "Label Text"
```

#### Options

- **Text Input**: 
  - Provide text directly as a command-line argument:
    ```bash
    filelabeler "Sample Label Text"
    ```
  - Or pass text via `stdin`:
    ```bash
    echo "Sample Label Text" | filelabeler
    ```

- **Printer**: Use the `--printer` option to specify the printer:
  ```bash
  filelabeler "Label Text" --printer DYMO_LabelWriter
  ```

- **Font Size**: Use `--font_size` to specify the font size (default is 200):
  ```bash
  filelabeler "Label Text" --font_size 150
  ```
  - If no font_size is specified, the application will find the maximum font_size that will fit the text on the label up to 200
  - font_size is specified as height in pixels
#### Example

```bash
echo "Hello, World!" | filelabeler --font_size 100 --printer DYMO_LabelWriter
```

---

### 2. `addresslabeler`

This application prints address labels from a file or `stdin`. Each address is separated by a blank line.

#### Usage

```bash
addresslabeler [file]
```

#### Options

- **File Input**: 
  - Provide a file containing addresses:
    ```bash
    addresslabeler addresses.txt
    ```
  - Or pass addresses via `stdin`:
    ```bash
    cat addresses.txt | addresslabeler
    ```

- **Printer**: Use the `--printer` option to specify the printer:
  ```bash
  addresslabeler addresses.txt --printer DYMO_LabelWriter
  ```

#### Address File Format

The file should contain one or more addresses, with each address separated by a blank line. For example:

```
John Doe
123 Main St
Springfield, IL 62701

Jane Smith
456 Elm St
Shelbyville, IL 61501
```

#### Example

```bash
addresslabeler addresses.txt --printer DYMO_LabelWriter
```

Or, using `stdin`:

```bash
cat addresses.txt | addresslabeler
```

---

## DYMO Printer Detection

Both applications automatically detect the first DYMO printer available using the `lpstat` command. If no printer is detected, you can specify a printer manually using the `--printer` option.

---

## Building the Applications

To build the applications, use the provided `build.sh` script:

```bash
./build.sh
```

This script uses `pyinstaller` to create standalone executables for `filelabeler` and `addresslabeler`. The executables will be copied to `~/.local/bin`.

---

## Troubleshooting

- **Missing Fonts**: Ensure the Courier font (`FreeMono.ttf`) is installed on your system.

```bash
sudo apt install fonts-freefont-ttf
```

- **DYMO Printer Detection Fails**: Verify the printer is properly set up in your system. Check with:
  ```bash
  lpstat -p
  ```