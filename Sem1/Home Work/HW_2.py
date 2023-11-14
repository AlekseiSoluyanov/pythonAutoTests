# Доработать функцию из предыдущего задания таким образом, чтобы у неё появился дополнительный режим работы,
# в котором вывод разбивается на слова с удалением всех знаков пунктуации
# (их можно взять из списка string.punctuation модуля string).
# В этом режиме должно проверяться наличие слова в выводе.

import subprocess
import string


def check_output(command, text):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    check_str = result.stdout.translate(str.maketrans('', '', string.punctuation)).split("\n")
    if result.returncode == 0:
        for el in check_str:
            print(el)
            if text in el:
                return True
        return False
    else:
        return f'error command: {command}'


command = "ls -la"
text = "HW"

print(check_output(command, text))
