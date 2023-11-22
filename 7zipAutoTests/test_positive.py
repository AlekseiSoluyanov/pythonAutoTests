import yaml

from checkers import ssh_getout, ssh_checkout, getout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:

    def save_log(self, start_time, name):
        with open(name, 'a') as f:
            f.write(ssh_getout("0.0.0.0", "user2", "11", "journalctl --since {}".format(start_time)))

    def test_step1(self, clear_folders, make_files, start_time):
        # test1
        result1 = ssh_checkout("0.0.0.0", "user2", "11", "cd {}; 7z a {}/arx2".format(data["tst"],
                                                                                      data["out"]), "Everything is Ok")
        result2 = ssh_checkout("0.0.0.0", "user2", "11", "cd {}; ls".format(data["out"]), "arx2.7z")
        self.save_log(start_time, "stat.txt")
        assert result1 and result2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files, start_time):
        # test2
        res = []
        res.append(ssh_checkout("0.0.0.0", "user2", "11", "cd {}; 7z a {}/arx2".format(data["tst"],
                                                                                       data["out"]),
                                "Everything is Ok"))
        res.append(ssh_checkout("0.0.0.0", "user2", "11", "cd {}; 7z e arx2.7z -o{} -y".format(data["out"],
                                                                                               data["folder1"]),
                                "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout("0.0.0.0", "user2", "11", "cd {}; ls".format(data["folder1"]), item))
        self.save_log(start_time, "stat.txt")
        assert all(res), "test2 FAIL"

    def test_step3(self, start_time):
        # test3
        self.save_log(start_time, "stat.txt")
        assert ssh_checkout("0.0.0.0", "user2", "11", "cd {}; 7z t arx2.7z".format(data["out"]),
                            "Everything is Ok"), "test1 FAIL"

    def test_step4(self, start_time):
        # test4
        self.save_log(start_time, "stat.txt")
        assert ssh_checkout("0.0.0.0", "user2", "11", "cd {}; 7z u {}/arx2.7z".format(data["tst"],
                                                                                      data["out"]),
                            "Everything is Ok"), "test1 FAIL"

    def test_step5(self, clear_folders, make_files, start_time):
        # test5
        res = []
        res.append(ssh_checkout("0.0.0.0", "user2", "11", "cd {}; 7z a {}/arx2".format(data["tst"],
                                                                                       data["out"]),
                                "Everything is Ok"))
        for item in make_files:
            res.append(
                ssh_checkout("0.0.0.0", "user2", "11", "cd {}; 7z l arx2.7z".format(data["out"], data["folder1"]),
                             item))
        self.save_log(start_time, "stat.txt")
        assert all(res), "test5 FAIL"

    def test_step6(self, clear_folders, make_files, make_subfolder, start_time):
        # test6
        res = []
        res.append(ssh_checkout("0.0.0.0", "user2", "11", "cd {}; 7z a {}/arx".format(data["tst"], data["out"]),
                                "Everything is Ok"))
        res.append(
            ssh_checkout("0.0.0.0", "user2", "11", "cd {}; 7z x arx.7z -o{} -y".format(data["out"], data["folder2"]),
                         "Everything is Ok"))

        for item in make_files:
            res.append(ssh_checkout("0.0.0.0", "user2", "11", "ls {}".format(data["folder2"]), item))

        res.append(ssh_checkout("0.0.0.0", "user2", "11", "ls {}".format(data["folder2"]), make_subfolder[0]))
        res.append(ssh_checkout("0.0.0.0", "user2", "11", "ls {}/{}".format(data["folder2"], make_subfolder[0]),
                                make_subfolder[1]))
        self.save_log(start_time, "stat.txt")
        assert all(res), "test6 FAIL"

    def test_step7(self, clear_folders, make_files, start_time):
        # test7
        res = []
        for item in make_files:
            res.append(
                ssh_checkout("0.0.0.0", "user2", "11", "cd {}; 7z h {}".format(data["tst"], item), "Everything is Ok"))
            hash = getout("cd {}; crc32 {}".format(data["tst"], item)).upper()
            res.append(ssh_checkout("0.0.0.0", "user2", "11", "cd {}; 7z h {}".format(data["tst"], item), hash))
        self.save_log(start_time, "stat.txt")
        assert all(res), "test8 FAIL"

    def test_step8(self, start_time):
        # test8
        self.save_log(start_time, "stat.txt")
        assert ssh_checkout("0.0.0.0", "user2", "11", "cd {}; 7z d arx.7z".format(data["out"]),
                            "Everything is Ok"), "test8 FAIL"
