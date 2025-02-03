# Noob-Wasi Help File

## Overview
**Noob-Wasi** is a URL fuzzing tool created by Muhammad Waseem to find critical backup files by creating a dynamic wordlist based on the domain. It is designed to be user-friendly and efficient for security researchers and enthusiasts.

## Installation
To install the required dependencies, run:
```bash
pip install -r requirements.txt
```

## Usage
You can run the tool using the following command:
```bash
python fuzzuli.py -f <input_file> -pt <paths> -mt <methods> -ex <extensions> -t <tags>
```

### Options:
- `-f`, `--file`: Input file containing a list of host/domain (one per line).
- `-pt`, `--paths`: Paths. Separate with commas to use multiple paths (e.g., /,/db/,/old/).
- `-mt`, `--method`: Methods. Available methods: regular, withoutdots, withoutvowels, reverse, mixed, withoutdv, shuffle.
- `-ex`, `--extension`: File extension. Default (rar, zip, tar.gz, tar, gz, jar, 7z, bz2, sql, backup, war).
- `-p`, `--print`: Print URLs that are sent requests.
- `-sl`, `--silent`: Silent mode.
- `-jw`, `--just_wordlist`: Just generate wordlist, do not HTTP request.
- `-t`, `--tags`: Comma-separated list of tags to filter wordlists.

## Example Commands
1. **Basic Usage**:
   ```bash
   python fuzzuli.py -f sample_domains.txt -pt / -mt regular
   ```

2. **Using Tags**:
   ```bash
   python fuzzuli.py -f sample_domains_with_tags.txt -pt / -mt regular -t backup,old
   ```

3. **Custom Extensions**:
   ```bash
   python fuzzuli.py -f sample_domains.txt -pt / -ex .zip,.tar
   ```

## Contributing
We welcome contributions from the community! If you have suggestions, improvements, or bug fixes, please feel free to submit a pull request or open an issue.

## License
This project is licensed under the MIT License.
