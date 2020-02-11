from PIL import Image

flopDict = dict()


def loadLetters():
    global flopDict
    people = open("dat/letters.dat", "r").read().strip().split("@")
    for i in range(len(people)):
        if len(people[i]) == 1:
            flopDict[people[i]] = people[i + 1][1:]


loadLetters()


def convertFlop(context):
    context = context.upper()

    spaces = map(lambda x: True if x == " " else False, context)
    num = sum(spaces)

    img = Image.open('dat/flop.png', 'r')
    img = img.resize((35, 35), Image.ANTIALIAS)
    size = img.size[0]
    letterspaces = (len(context) - num) * 7 * 35
    inbetweenspaces = (len(context) - num) * 2 * 35
    spacesspace = (num - (1 if num > 0 else 0)) * 3 * 35
    print(letterspaces, inbetweenspaces, spacesspace)
    background = Image.new('RGBA', (letterspaces + inbetweenspaces + spacesspace, 7 * 35), (0, 0, 0, 0))

    x, y = 0, 0
    xMax = 0
    for i in context:
        if i == " ":
            xMax += size * 2
            x = xMax + size
            continue
        baseX = xMax + size if xMax != 0 else 0
        for n in flopDict[i].split("\n"):
            for f in n.split("/"):
                if f == 'flop':
                    background.paste(img, (x, y))
                x += size
            xMax = x if x > xMax else xMax
            x = baseX
            y += size

        x = xMax + size
        y = 0

    background.save('out.png')
