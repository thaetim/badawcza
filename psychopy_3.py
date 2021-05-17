from psychopy import visual, core, event
import random
import csv
# import time


def reactions(key_list):
    event.clearEvents()
    keys = event.waitKeys(keyList=key_list)
    return keys[0]


def show_text(info, win, keys=["space"]):
    info.draw()
    win.flip()
    reactions(keys)


def part_of_experiment(n_trials, keys, experiment, fix_time, fix_stim):
    for i in range(n_trials):
        stim_type = random.choice(list(stim.keys()))
        print(stim_type)

        fix_stim.draw()
        window.flip()
        core.wait(fix_time)

        stim[stim_type].draw()
        window.callOnFlip(clock.reset)
        window.flip()

        key = reactions(keys)
        rt = clock.getTime()

        acc = stim_type == key
        RESULTS.append([i+1, experiment, acc, rt, stim_type, key])


if __name__ == "__main__":
    # initialization
    N_TRIALS_TRAINING = 1
    N_TRIALS_EXPERIMENT = 4
    REACTION_KEYS = ["left", "right"]
    RESULTS = [
        ["NR", "EXPERIMENT", "ACC", "RT", "TRIAL_TYPE", "REACTION"]
    ]

    window = visual.Window(
        units="pix",
        color="gray",
        fullscr=False
    )
    window.setMouseVisible(False)

    clock = core.Clock()

    stim = {
        "left": visual.TextStim(win=window, text="L", height=40),
        "right": visual.TextStim(win=window, text="R", height=40)
    }
    stim_fixation = visual.TextStim(win=window, text="+", height=40)

    inst_tr = visual.TextStim(win=window, text="instrukcja", height=20)
    inst_exp = visual.TextStim(win=window, text="eksperyment", height=20)
    inst_end = visual.TextStim(win=window, text="THE END", height=20)

    # TRAINING
    show_text(info=inst_tr, win=window)
    part_of_experiment(
        N_TRIALS_TRAINING,
        REACTION_KEYS,
        experiment=False,
        fix_stim=stim_fixation,
        fix_time=2
    )

    # EXPERIMENT
    show_text(info=inst_exp, win=window)
    part_of_experiment(
        N_TRIALS_EXPERIMENT,
        REACTION_KEYS,
        experiment=True,
        fix_stim=stim_fixation,
        fix_time=2
    )

    # THE END
    show_text(info=inst_end, win=window)

    # RESULTS
    with open("result.csv", 'w', newline="") as f:
        write = csv.writer(f)
        write.writerows(RESULTS)
