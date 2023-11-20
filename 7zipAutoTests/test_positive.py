import yaml

from checkers import checkout, getout


with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:

    def test_step1(self, clear_folders, make_files):
        # test1
        result1 = checkout("cd {}; 7z a {}/arx2".format(data["tst"], data["out"]), "Everything is Ok")
        result2 = checkout("cd {}; ls".format(data["out"]), "arx2.7z")
        assert result1 and result2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files):
        # test2
        res = []
        res.append(checkout("cd {}; 7z a {}/arx2".format(data["tst"], data["out"]), "Everything is Ok"))
        res.append(checkout("cd {}; 7z e arx2.7z -o{} -y".format(data["out"], data["folder1"]), "Everything is Ok"))
        for item in make_files:
            res.append(checkout("cd {}; ls".format(data["folder1"]), item))
        assert all(res), "test2 FAIL"

    def test_step3(self):
        # test3
        assert checkout("cd {}; 7z t arx2.7z".format(data["out"]), "Everything is Ok"), "test1 FAIL"

    def test_step4(self):
        # test4
        assert checkout("cd {}; 7z u {}/arx2.7z".format(data["tst"], data["out"]), "Everything is Ok"), "test1 FAIL"

    def test_step5(self, clear_folders, make_files):
        # test5
        res = []
        res.append(checkout("cd {}; 7z a {}/arx2".format(data["tst"], data["out"]), "Everything is Ok"))
        for item in make_files:
            res.append(checkout("cd {}; 7z l arx2.7z".format(data["out"], data["folder1"]), item))
        assert all(res), "test5 FAIL"

    def test_step6(self, clear_folders, make_files, make_subfolder):
        # test6
        res = []
        res.append(checkout("cd {}; 7z a {}/arx".format(data["tst"], data["out"]), "Everything is Ok"))
        res.append(checkout("cd {}; 7z x arx.7z -o{} -y".format(data["out"], data["folder2"]), "Everything is Ok"))

        for item in make_files:
            res.append(checkout("ls {}".format(data["folder2"]), item))

        res.append(checkout("ls {}".format(data["folder2"]), make_subfolder[0]))
        res.append(checkout("ls {}/{}".format(data["folder2"], make_subfolder[0]), make_subfolder[1]))
        assert all(res), "test6 FAIL"

    def test_step7(self, clear_folders, make_files):
        # test7
        res = []
        for item in make_files:
            res.append(checkout("cd {}; 7z h {}".format(data["tst"], item), "Everything is Ok"))
            hash = getout("cd {}; crc32 {}".format(data["tst"], item)).upper()
            res.append(checkout("cd {}; 7z h {}".format(data["tst"], item), hash))
        assert all(res), "test8 FAIL"

    def test_step8(self):
        # test8
        assert checkout("cd {}; 7z d arx.7z".format(data["out"]), "Everything is Ok"), "test8 FAIL"
