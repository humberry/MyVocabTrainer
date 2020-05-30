MyVocabTrainer
==============

![alt text](https://img.shields.io/badge/iOS-11.x-lightgrey.svg?style=plastic "iOS 13.x")
![alt text](https://img.shields.io/badge/Pythonista-3.2-green.svg?style=plastic "Pythonista 3.3")
![alt text](https://img.shields.io/badge/Python-3.6-blue.svg?style=plastic "Python 3.6")

- choose font, fontsize and color
- choose direction: first language </> second language or mixed
- automatically sorted to less learned words
- randomize 100 words (no alphabetical learning)
- with ( a new line starts, e.g. hints, notice, pronunciation
- add new words with category and two keyboard layouts (Latin / Cyrillic)
- sqlite3 database
- export to csv

Todos:
- import from csv

If there's no need for a second keyboard layout, you can easily comment the line
#russian_keyboard.SetTextFieldPad(self.view['textfield2'])
out. 
