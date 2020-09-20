# PyMCRTPC
Python Minecraft Resource to Texture Pack Converter.  
**Because I suck at names.**  
<sup>Try pronouncing it.</sup>

### Features
- Takes any minecraft 1.6> resource pack.
- Puts any textures that exist in 1.4.7< into various stitched texture files.
- These can then be used as a texturepack for 1.4.7<.  
- Supports HD texturepacks!

Thats it.

### Caveats
- 1.5.* is not supported due to weird texture madness.
- If you want to convert a texturepack into a resourcepack, you will want to use [TextureEnder](http://s3.amazonaws.com/Minecraft.Download/utilities/TextureEnder.jar).
- The bed and head items cannot be generated automatically due to discrepancies between items in these versions.

### Requirements
- Python 3 or above.
- A toaster that doesnt overheat.
- 10 minutes of time.

### Usage
1. Extract your resourcepack into a folder named `resourcepack`.
2. Install `pillow` onto your python 3 install (`pip`|`pip3 install pillow`).
3. Run main.py with python 3.
4. Output will be in `items.png` and `terrain.png`.