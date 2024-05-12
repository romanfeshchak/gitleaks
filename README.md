# Gitleaks pre-commit hook

This script sets up a pre-commit hook for Git that automatically checks for secrets in your code using Gitleaks.

## Prerequisites

- Python 3
- Git
- Curl (for installation)
- tar/zip

## Installation

```curl pipe
cd to git repository
curl -sSL https://raw.githubusercontent.com/romanfeshchak/gitleaks/main/pipegitleaks.py

```
OR
```
git clone https://github.com/romanfeshchak/gitleaks.git
cd gitleaks directory 
```

Run the Python script pre-commit.py to install Gitleaks and enable the pre-commit hook.
```shell
python3 pipegitleaks.py
```

## Usage

After the installation, the pre-commit hook will automatically run before each commit. If any secrets or sensitive information are detected by Gitleaks, the commit will be rejected and an error message will be displayed.

To disable the pre-commit hook, you can set the gitleaks.enabled configuration option to false and rerun python script:

```shell
git config gitleaks.enabled false
```

To enable the pre-commit hook, run the following command:

```shell
git config gitleaks.enabled true
```
