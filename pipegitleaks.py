import os
import platform
import subprocess
import tarfile
import zipfile

def download_extract_install_gitleaks(os_type):
    gitleaks_urls = {
        "Linux": "https://github.com/gitleaks/gitleaks/releases/download/v8.18.0/gitleaks_8.18.0_linux_x64.tar.gz",
        "Darwin": "https://github.com/gitleaks/gitleaks/releases/download/v8.18.0/gitleaks_8.18.0_darwin_arm64.tar.gz",
        "Windows": "https://github.com/gitleaks/gitleaks/releases/download/v8.18.0/gitleaks_8.18.0_windows_x64.zip"
    }
    if os_type in gitleaks_urls:
        file_name = gitleaks_urls[os_type].split('/')[-1]
        file_path = os.path.join(os.getcwd(), file_name)
        subprocess.run(['curl', '-L', '-o', file_path, gitleaks_urls[os_type]])
        
        if file_path.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extract('gitleaks', path=os.getcwd())
        elif file_path.endswith('.tar.gz'):
            with tarfile.open(file_path, 'r:gz') as tar_ref:
                for member in tar_ref.getmembers():
                    if member.name.endswith('gitleaks'):
                        tar_ref.extract(member, path=os.getcwd())

        gitleaks_binary = os.path.join(os.getcwd(), 'gitleaks')
        os.chmod(gitleaks_binary, 0o755)
        os.remove(file_path)

        print("Gitleaks installed successfully.")
    else:
        print("Unsupported OS.")

def setup_git_hooks():
    current_dir = os.getcwd()
    git_hooks_dir = os.path.join(current_dir, '.git', 'hooks')
    pre_commit_hook_path = os.path.join(git_hooks_dir, 'pre-commit')
    gitleaks_path = os.path.join(current_dir, 'gitleaks')
    if os.path.exists(gitleaks_path):
        gitleaks_cmd = f'set -e\n{gitleaks_path} protect --staged --verbose\n'
        with open(pre_commit_hook_path, 'w') as hook_file:
            hook_file.write(gitleaks_cmd)
        os.chmod(pre_commit_hook_path, 0o755)
        print("Pre-commit hook set up successfully.")
    else:
        print("Gitleaks binary not found.")

def check_repository_for_secrets():
    gitleaks_path = os.path.join(os.getcwd(), 'gitleaks')
    if os.path.exists(gitleaks_path):
        subprocess.run([gitleaks_path, 'protect', '--staged', '--source', '.', '--verbose'], cwd=os.getcwd())
    else:
        print("Gitleaks binary not found.")
def main():
    os_type = platform.system()

    download_extract_install_gitleaks(os_type)
    gitleaks_path = os.path.join(os.getcwd(), 'gitleaks')
    if os.path.exists(gitleaks_path):
        setup_git_hooks()
        check_repository_for_secrets()
    else:
        print("Gitleaks binary not found.")

if __name__ == "__main__":
    main()
