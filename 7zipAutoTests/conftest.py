import random
import string

import pytest
import yaml
from datetime import datetime
from checkers import getout, ssh_checkout, ssh_get

from tests.sshcheckers import upload_files

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture(autouse=True, scope="module")
def make_folders():
    return ssh_checkout("0.0.0.0", "user2", "11",
                        "mkdir -p {} {} {} {}".format(data["tst"], data["out"],
                                                      data["folder1"], data["folder2"]), "")


@pytest.fixture()
def clear_folders():
    return ssh_checkout("0.0.0.0", "user2", "11", "rm -rf {}/* {}/* {}/* {}/*".format(data["tst"],
                                                                                      data["out"], data["folder1"],
                                                                                      data["folder2"]), "")


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout("0.0.0.0", "user2", "11",
                        "cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["tst"],
                                                                                               filename,
                                                                                               data["bs"]), ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout("0.0.0.0", "user2", "11", "cd {}; mkdir {}".format(data["tst"],
                                                                           subfoldername), ""):
        return None, None
    if not ssh_checkout("0.0.0.0", "user2", "11",
                        "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["tst"],
                                                                                                  subfoldername,
                                                                                                  testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield print("Stop: {}".format(datetime.now().strftime("%H:%M:%S.%f")))


@pytest.fixture()
def make_bad_arx():
    ssh_checkout("0.0.0.0", "user2", "11", "cd {}; 7z a {}/bad_arx".format(data["tst"],
                                                                           data["out"]), "Everything is Ok")
    ssh_checkout("0.0.0.0", "user2", "11", "truncate -s 1 {}/bad_arx.7z".format(data["out"]), "")


@pytest.fixture(autouse=True)
def stat_fixture():
    time_stamp = datetime.now().strftime("%H:%M:%S.%f")
    cpu_stat = getout("cat /proc/loadavg")
    ssh_checkout("0.0.0.0", "user2", "11", f'cd {data["stat"]}; echo "time = {time_stamp},'
                                           f'files_count = {data["count"]},'
                                           f'file_size = 'f'{data["bs"]}, cpu_stat = {cpu_stat}" >> stat.txt', '')


@pytest.fixture(autouse=True, scope="module")
def deploy():
    res = []
    upload_files("0.0.0.0", "user2", "11", "/home/user/p7zip-full.deb",
                 "/home/user2/p7zip-full.deb")
    res.append(ssh_checkout("0.0.0.0", "user2", "11",
                            "echo '11' | sudo -S dpkg -i /home/user2/p7zip-full.deb", "Настраивается пакет"))
    res.append(ssh_checkout("0.0.0.0", "user2", "11",
                            "echo '11' | sudo -S dpkg -s p7zip-full.deb", "Status: install ok installed"))
    return all(res)


@pytest.fixture(autouse=True, scope="module")
def start_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def safe_log(stat, statdate):
    with open(stat, "w") as f:
        f.write(ssh_get("0.0.0.0", "user2", "11", "journalctl --since {}".format(statdate)))


