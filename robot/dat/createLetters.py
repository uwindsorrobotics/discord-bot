import subprocess

a = list("abcdefghijklmnopqrstuvwxyz1234567890?.,/%(){}[]<>_-=+*&^%$#@!~".upper())

writingFile = open("letters.dat", 'w')
for alpha in a:
    p = subprocess.Popen("banner '%s'" % alpha, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()

    x = str(output)[2:-1].split("\\n")

    letter = alpha
    string = ""
    for i in x:
        for n in range(len(i) - 2):
            if i[n] == "*":
                string += "flop/"
            else:
                string += "blank/"
        string += "\n"
    writingFile.write(f'@{letter}@\n{string}')
