import pandas as pd
from PIL import Image
from math import sqrt

# create a map that associates the name of the state
# to its adjusted size in cm^2
#  - from that, the filepath where its image is located can be computed,
#    as well as the size (in pixels) that it should be
data = pd.read_excel("spreadsheet.xlsx")
states_info: map[str, float] = {
	name.strip().lower().replace(" ", "-"): size for name, size in zip(data["STATE"], data["SIZE OF STATE ON MAP (cm²)"])
}

def main():
	# go through all of the states in the map
	for name, target_area in states_info.items():
		img = Image.open(f"states/{name}.png") # open the path as an Image object

		# find new dimensions by converting cm^2 to pixel width/height
		og_width, og_height = img.size
		og_area = og_width * og_height;

		target_area_inches = target_area / 6.4516 # the 2.45 squared, the conversion factor from cm to in
		target_area_pixels = target_area_inches * 90000 # DPI of 300, square it

		multiplier = sqrt(target_area_pixels / og_area)

		new_width = round(og_width * multiplier)
		new_height = round(og_height * multiplier)

		print(f"{name} -> ({new_width}, {new_height})")

		# resize the image and then save as "adjusted/state-name.png"
		resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS) # upscaler CV model??
		resized.save(f"adjusted_state_images/{name}.png", dpi=(300, 300))


# actually run the thing
if __name__ == "__main__":
	main()
