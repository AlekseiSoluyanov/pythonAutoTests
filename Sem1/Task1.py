import subprocess

if __name__ == '__main__':
    result = subprocess.run("cat /etc/os-release", shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    out = result.stdout
    if "22.04.1" in out and "jammy" in out and result.returncode == 0:
        print("SUCCES")
    else:
        print("FAIL")