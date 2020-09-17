import json
import sys
import os
import shutil
import traceback
import PIL.Image

# Yes, I know there are better ways to do this, but I wanted this to to be a quick easy script.
sizedict = {
    "in": 16,
    "x": 0,
    "y": 0
}
domanually = False


# https://gist.github.com/alexras/4720743
def scale_to_width(dimensions, width):
    height = (width * dimensions[1]) / dimensions[0]

    return (int(width), int(height))


def stitchfiles(jsonfile, outfile, size):
    terrain = PIL.Image.new("RGBA", (size["out"], size["out"]))
    history = []
    with open(jsonfile, "r") as files:
        for file in json.loads(files.read()):
            if size["x"] >= size["out"]-1:
                size["x"] = 0
                size["y"] += size["in"]

            fileargs = file.split(":")
            file = fileargs[0]
            chistory = True
            file = "textures" + file
            if file.endswith(".png") and os.path.isfile(file):
                img = PIL.Image.open(file)
                x, y = img.size
                if x == size["in"] and y == size["in"]:
                    if len(fileargs) > 2 and fileargs[1] == "lastfalse":
                        fileargs[2] = int(fileargs[2])
                        if all(not elem for elem in history[:fileargs[2]]):
                            if fileargs[2] == 2:
                                print("Splitting texture \"" + file + "\"...")
                                size["x"] -= size["in"] * 2
                                left = PIL.Image.open(file)
                                left = left.crop((0, 0, x/2, y))
                                print("Appending first part to first slot.")
                                terrain.paste(left, (int((x/2)/2) + size["x"], size["y"]))
                                size["x"] += size["in"]
                                img = img.crop((x/2, 0, x, y))
                                print("Appending second part to second slot.")
                                terrain.paste(img, (int((x/2)/2) + size["x"], size["y"]))
                            else:
                                size["x"] -= size["in"]
                                terrain.paste(img, (size["x"], size["y"]))

                    elif len(fileargs) > 2 and fileargs[1] == "rot":
                        print("Rotating \"" + fileargs[0] + "\" " + fileargs[2] + " degrees.")
                        img = img.rotate(int(fileargs[2]))
                        terrain.paste(img, (size["x"], size["y"]))
                    else:
                        terrain.paste(img, (size["x"], size["y"]))
                elif len(fileargs) > 2 and fileargs[1] == "bed":
                    print("Applying bed workaround. Textures might be slightly stretched.")
                    rel = int(size["in"] / 16)
                    if fileargs[2] == "top":
                        pos = (rel*6, rel*6, rel*21, rel*21)
                    elif fileargs[2] == "bottom":
                        pos = (rel*6, rel*28, rel*21, rel*43)
                    elif fileargs[2] == "foot":
                        pos = (rel*22, rel*22, rel*37, rel*27)
                    elif fileargs[2] == "backboard":
                        pos = (rel*6, 0, rel*21, rel*5)
                    elif fileargs[2] == "bottomside":
                        pos = (0, rel*28, rel*5, rel*43)
                    elif fileargs[2] == "topside":
                        pos = (0, rel*6, rel*5, rel*21)
                    else:
                        pos = (6,6,21,21)
                    tmpimg = img.crop(pos)
                    img = PIL.Image.new("RGBA", (size["in"]-rel, size["in"]-rel))
                    img.paste(tmpimg, (0, 0))
                    if fileargs[2] in ["topside", "bottomside"]:
                        img = img.rotate(90)
                    if fileargs[2] in ["foot", "backboard"]:
                        img = img.rotate(180)
                    if fileargs[2] in ["top", "bottom"]:
                        terrain.paste(img, (size["x"]+rel, size["y"]))
                        terrain.paste(img, (size["x"]+rel, size["y"]+rel))
                        terrain.paste(img, (size["x"], size["y"]+rel))
                        img = img.rotate(-90)
                    elif fileargs[2] in ["foot", "backboard", "topside", "bottomside"]:
                        terrain.paste(img, (size["x"]+rel, size["y"]))
                    terrain.paste(img, (size["x"], size["y"]))
                elif x == y and not len(fileargs) > 1:
                    img.resize(scale_to_width(img.size, size["x"]), PIL.Image.NEAREST)
                    terrain.paste(img, (size["x"], size["y"]))
                elif x >= size["in"] and y >= size["in"]:
                    print("Cropping \"" + file + "\": Wrong dimensions. This can cause some weird textures.")
                    img = img.crop((0, 0, size["in"], size["in"]))
                    terrain.paste(img, (size["x"], size["y"]))
                else:
                    print("Skipping \"" + file + "\": Wrong dimensions.")
                    chistory = False
            elif file == "blank":
                pass
            else:
                print("Skipped \"" + file + "\": Wrong filetype.")
                if len(fileargs) > 1 and fileargs[1] == "lastfalse":
                    size["x"] -= size["in"]
                chistory = False

            history.insert(0, chistory)


            size["x"] += size["in"]
    terrain.save(outfile)


try:
    with PIL.Image.open("resourcepack/assets/minecraft/textures/block/dirt.png") as img:
        x, y = img.size
        if x == y:
            sizedict["in"] = x
except:
    domanually = True

if domanually:
    print("Could not detect texture size. What size are your textures?")
    sizedict["in"] = int(input(": "))

sizedict["out"] = 16 * sizedict["in"]


sizedictt = dict(sizedict)
stitchfiles("terrain.json", "terrain.png", sizedictt)
sizedicti = dict(sizedict)
stitchfiles("items.json", "items.png", sizedicti)

sys.exit(0)
