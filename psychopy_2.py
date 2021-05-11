from psychopy import visual, core, event  # import some Libraries from Psychopy

# create a window
win = visual.Window([800, 600], monitor="testMonitor", units='deg')

text = visual.TextStim(win=win, text="Hello, psychopy", pos=[0, 2])
# draw the stats and update the window
while True:  # this creates a never-ending loop
    text.draw()
    win.flip()

    if len(event.getKeys()) > 0:
        break
    event.clearEvents()

text.setAutoDraw(True)

text.setText("3...")
win.flip()
core.wait(1)

text.setText("2...")
win.flip()
core.wait(1)

text.setText("1...")
win.flip()
core.wait(1)
