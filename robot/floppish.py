from PIL import Image

flopDict = dict()

print("haha this is kinda something to force a push to my heroku shit")

def loadLetters():
    global flopDict
    people = open("dat/letters.dat", "r").read().strip().split("@")
    for i in range(len(people)):
        if len(people[i]) == 1:
            flopDict[people[i]] = people[i + 1][1:]


loadLetters()


def convertFlop(context):
    context = context.upper()

    img = Image.open('dat/flop.png', 'r')

    img = img.resize((35, 35), Image.ANTIALIAS)

    size = img.size[0]

    x, y = 0, 0
    mostRight = 0
    previous_right = 0
    coordinates = list()
    for letter in context:

        if letter == " ":
            previous_right += size * 2
            mostRight += size * 2
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
        y = 0

    background = Image.new('RGBA', (max(coordinates)[0] + size, 13 * 35), (0, 0, 0, 0))

    for i in coordinates:
        background.paste(img, i)

    background.save('dat/out.png')