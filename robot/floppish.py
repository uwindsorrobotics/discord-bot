from PIL import Image

flopDict = dict()


def loadLetters():
    global flopDict
    characters = open("dat/letters.dat", "r").read().strip().split("!     !")
    for i in range(len(characters)):
        if len(characters[i]) == 1:
            flopDict[characters[i]] = characters[i + 1][1:]


loadLetters()


def convertFlop(context, image):
    img = Image.open(f'dat/{image}', 'r')

    img = img.resize((35, 35), Image.ANTIALIAS)

    size = img.size[0]

    x, y = 0, 0
    mostRight = 0
    mostDown = 0
    previous_right = 0
    coordinates = list()
    for letter in context:

        if previous_right >= 4500 and letter == " ":
            x = mostRight = previous_right = 0
            mostDown += size * 12
            y = mostDown
            continue
        elif letter == " ":
            previous_right += size * 4
            mostRight += size * 4
            x = previous_right
            continue

        for line in flopDict[letter].split("\n"):

            for key in line.split("/"):
                if key == "flop":
                    coordinates.append((x, y))
                x += size
            y += size
            mostRight = x if mostRight < x else mostRight
            x = previous_right

        previous_right = mostRight
        x = previous_right
        y = mostDown

    background = Image.new('RGBA', (max(coordinates)[0] + size, (mostDown + size * 12) if mostDown != 0 else (13 * size)),
                           (0, 0, 0, 0))

    for i in coordinates:
        background.paste(img, i)

    background.save('dat/out.png')
