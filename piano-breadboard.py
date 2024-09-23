import RPi.GPIO as GPIO
import time
import musicpy as mp
import sf2_loader as sf
import concurrent.futures

sf2_file = "path_to_sf2_file" # https://freepats.zenvoid.org/Piano/acoustic-grand-piano.html

reaction_time = .06  # time it should take to press down all chord keys

buttonList = {
	"C4": 10, 
	"E4": 8, 
	"G4": 12, 
	"F4": 7
}

def buttonCheck(name):
	if GPIO.input(buttonList.get([item for item in buttonList][name])) == 1:
		activeButtons.append([item for item in buttonList][name])

try:
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)

	for button in buttonList:
		GPIO.setup(buttonList[button],GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

	loader = sf.sf2_loader(sf2_file)
	activeButtons = []

	while True:
		buttonHistory = activeButtons
		activeButtons = []

		with concurrent.futures.ThreadPoolExecutor(max_workers=len(buttonList)) as executor:
			executor.map(buttonCheck, range(len(buttonList)))

		time.sleep(reaction_time)

		if len(activeButtons) == 0:
			continue
		else:
			if len(activeButtons) - len(buttonHistory) > 1:
				loader.play_chord(mp.chord(','.join(activeButtons)))
			elif len(activeButtons) - len(buttonHistory) == 1:
				loader.play_note(mp.note(str(set(activeButtons) - set(buttonHistory))[2],int(str(set(activeButtons) - set(buttonHistory))[3])))
finally:
	GPIO.cleanup()
