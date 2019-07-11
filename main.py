import utils
import config
#import images

import sys
import os
import shutil
import PIL.Image

size = {
    "in": 16,
    "x": 0,
    "y": 0
}
size["out"] = 16 * size["in"]

terrain = PIL.Image.new("RGBA", (size["out"], size["out"]))

for file in os.scandir("test"):
    name = "test/" + file.name
    if os.path.isdir(file.name):
        pass
    elif name.lower().endswith(".png"):
        img = PIL.Image.open(name)
        x, y = img.size
        if x == size["in"] and y == size["in"]:
            terrain.paste(img, (size["x"], size["y"]))#

            if size["y"] > size["out"]:
                break
            elif size["x"] > size["out"]:
                size["x"] = 0
                size["y"] += size["in"]
            else:
                size["x"] += size["in"]
        else:
            print("Skipped \"" + name + "\": Wrong dimensions.")
    else:
        print("Skipped \"" + name + "\": Wrong filetype.")

terrain.save("terrain.png")
