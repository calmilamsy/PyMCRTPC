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
            if file.endswith(".png") and os.path.isfile(file):
                img = PIL.Image.open(file)
                x, y = img.size
                if x == size["in"] and y == size["in"]:
                    if len(fileargs) > 2 and fileargs[1] == "lastfalse":
                        fileargs[2] = int(fileargs[2])
                        if all(not elem for elem in history[:fileargs[2]]):
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
                    elif fileargs != "lastfalse":
                        terrain.paste(img, (size["x"], size["y"]))
                    else:
                        print("Skipping \"" + file + "\": Not needed.")
                        size["x"] -= size["in"]
                elif len(fileargs) > 2 and fileargs[1] == "bed":
                    rel = size["in"] / 16
                    if fileargs[2] == "top":
                        pos = (rel*6, rel*6, rel*21, rel*21)
                    elif fileargs[2] == "bottom":
                        pos = (rel*6, rel*28, rel*21, rel*43)
                        pass
                    else:
                        pos = (6,6,21,21)
                    img = img.crop(pos)
                    img = img.rotate(-90)
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

stitchfiles("terrain.json", "terrain.png", sizedict)

sys.exit(0)
