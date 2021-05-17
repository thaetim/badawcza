from psychopy import visual, core, event
import random
# import time

N_TRIALS = 2
REACTION_KEYS = ["left", "right"]

window = visual.Window(
    units="pix",
    color="gray",
    fullscr=False
)
window.setMouseVisible(False)

stim = {
    "left": visual.TextStim(win=window, text="L", height=40),
    "right": visual.TextStim(win=window, text="R", height=40)
}


def reactions():
    event.clearEvents()
    keys = event.waitKeys(keyList=REACTION_KEYS)
    return keys[0]


for i in range(N_TRIALS):
    stim_type = random.choice(list(stim.keys()))
    print(stim_type)
    stim[stim_type].draw()
    window.flip()
    # time.sleep(2)
    key = reactions()
    acc = stim_type == key
    print(stim_type, key, acc)
