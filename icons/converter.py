import os

addons = [
['folder',''],
['folder-documents','_documents'],
['folder-downloads','_downloads'],
['folder-music','_music'],
['folder-pictures','_pictures'],
['folder-publicshare','_public'],
['folder-templates','_templates'],
['folder-videos','_videos'],
['user-desktop','_desktop']
]

colors = [
['blue', '#2980b9', '#3498db', '#3c2f1b'],
['brown', '#6A220B', '#B64926', '#3c2f1b'],
['custom', '#2c3e50', '#34495e', '#ecf0f1'],
['green', '#27ae60', '#2ecc71', '#3c2f1b'],
['grey', '#95a5a6', '#bdc3c7', '#3c2f1b'],
['orange', '#d35400', '#e67e22', '#3c2f1b'],
['pink', '#EA2E49', '#FF4B66', '#3c2f1b'],
['purple', '#8e44ad', '#9b59b6', '#3c2f1b'],
['red', '#c0392b', '#e74c3c', '#3c2f1b'],
['yellow', '#f39c12', '#f1c40f', '#3c2f1b']
]

folders = [
'16x16',
'22x22',
'24x24',
'32x32',
'48x48',
'64x64',
'128x128',
'256x256'
]

if not os.path.isdir('hicolor'):
	os.mkdir('hicolor')

		
for folder in folders:

	if not os.path.isdir('hicolor/' + folder):
		os.mkdir('hicolor/' + folder)

	if not os.path.isdir('hicolor/' + folder + '/places'):
		os.mkdir('hicolor/' + folder + '/places')


	directory = '/usr/share/icons/Numix/' + folder + '/places'
	for svg in os.listdir(directory):
		if svg[-3:] != 'svg':
			continue

		for addon in addons:
			f = open(directory + '/' + addon[0] + '.svg', 'r')
			data = f.read()
			f.close()

			for color in colors:
				name = color[0]
				color1 = color[1]
				color2 = color[2]
				color3 = color[3]

				changed = data.replace('#e9a439', color1)
				changed = changed.replace('#f5c14e', color2)
				changed = changed.replace('#3c2f1b', color3)


				f = open('hicolor/' + folder + '/places/folder_color_' + name + addon[1] + '.svg', 'w')
				f.write(changed)
				f.close()



