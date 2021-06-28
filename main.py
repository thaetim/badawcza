# PROJEKT PROCEDURY BADAWCZEJ
# https://github.com/thaetim/badawcza

from typing import Optional
from psychopy import visual, core, event
from psychopy.visual.text import TextStim
from psychopy.visual.window import Window
import random
import csv
import yaml
import os.path


def load_config(yaml_file: str = './config.yaml') -> dict:
    """Loads the configuration values from a YAML file. If there is no such file or the configuration file is empty, a file with default values (as in specification) is created and loaded.

    Args:
        yaml_file (str): Path to the YAML configuration file. Defaults to './config.yaml'

    Returns:
        dict: A dictionary with configuration values.
    """

    def default_config():
        config = {
            "FIX_TIME": 1000,
            "MAX_REACTION_TIME": 1000,
            "MIN_STOP_DELAY": 100,
            "MAX_STOP_DELAY": 400,
            "STOP_DELAY_STEP": 50,
            "INITIAL_STOP_DELAY": 150,
            "N_TRN_A_TRIALS": 15,
            "N_TRN_B_TRIALS": 27,
            "N_EXP_A_BLOCKS": 6,
            "N_EXP_A_TRIALS": 120,
            "REACTION_KEYS": ["a", "l"]
        }
        with open(yaml_file, 'w') as f:
            f.write(yaml.dump(config))

    if os.path.isfile(yaml_file):
        with open(yaml_file, 'r') as f:
            config = yaml.load(f.read())
        if not config:
            config = default_config()
    else:
        config = default_config()

    return config


def reactions(key_list: "list[str]", max_reaction_time: float = float("inf")) -> Optional[str]:
    """Waits for one of the keys in a list and returns the first one pressed. Exits the program if Escape pressed.

    Args:
        key_list (list[str]): List of keys to wait for.
        max_reaction_time (float, optional): Timeout in ms. Defaults to infinite.

    Returns:
        Optional[str]: First pressed key or None if timeouts.
    """
    event.clearEvents()
    keys = event.waitKeys(max_reaction_time, keyList=key_list.append("escape"))
    if keys and keys[0] == "escape":
        exit()
    if keys:
        print(keys[0])
    return keys[0] if keys else None


def show_text(text: str, win: Window, keys: "list[str]" = ["space"]) -> None:
    """Display a text on the screen and waits for a key press.

    Args:
        text (str): Text to show.
        win (Window): Window object to display the text on.
        keys (list[str], optional): List of keys to wait for. Defaults to ["space"].
    """
    visual.TextStim(win=window, text=text, height=20).draw()
    win.flip()
    reactions(keys)


def experiment_block(
    n_trials: int,
    keys: "list[str]",
    experiment: bool,
    fix_time: int,
    fix_stim: TextStim,
    err_stim: TextStim,
    win: Window,
    stop_trials_fraction: float = 0
) -> None:
    """Conducts a single block of the experiment, handling user input and output.

    Args:
        n_trials (int): Number of trials in the block.
        keys (list[str]): List of reaction keys.
        experiment (bool): True if block is an experiment block.
        fix_time (int): Fixation display time in ms.
        fix_stim (TextStim): TextStim of the fixation symbol.
        err_stim (TextStim): TextStim of the error screen.
        win (Window): Window object to draw on.
        stop_trials_fraction (float, optional): Fraction of trials that are to be STOP trials. Maximum 0.5. Defaults to 0.
    """

    stop_delay = INITIAL_STOP_DELAY

    trials_stop_types_tmp = [None] * int((0.5 - stop_trials_fraction) * n_trials)
    for stop_key in (stim_stop.keys()):
        trials_stop_types_tmp += [stop_key] * int((stop_trials_fraction / len(stim_stop) * n_trials))
    random.shuffle(trials_stop_types_tmp)
    trials_stop_types = []
    for tst in trials_stop_types_tmp:
        trials_stop_types.append(tst)
        trials_stop_types.append(None)

    for i, stop_type in enumerate(trials_stop_types):
        stim_type_go = random.choice(list(stim_go.keys()))
        print(stim_type_go)

        # FIXATION STIMULUS
        fix_stim.draw()
        win.flip()
        core.wait(fix_time / 1000)

        # GO STIMULUS
        stim_go[stim_type_go].draw()
        win.callOnFlip(clock.reset)
        win.flip()

        # STOP STIMULUS
        if stop_type:
            core.wait(stop_delay / 1000)
            stim_go[stim_type_go].draw()
            stim_stop[stop_type].draw()
            win.flip()

        key = reactions(keys, MAX_REACTION_TIME / 1000)
        rt = clock.getTime() if key else None

        acc = (stop_type is None and stim_type_go == key) or (stop_type is not None and key is None)

        # ERROR MESSAGE
        if not acc:
            err_stim.draw()
            win.flip()
            core.wait(1)

        # # EMPTY SCREEN #FIXME:
        # win.flip()
        # core.wait(random.randrange(900, 1100) / 1000)

        # STOP DELAY ADAPTATION
        if stop_type:
            if acc:
                stop_delay = max(MIN_STOP_DELAY, stop_delay - STOP_DELAY_STEP)
            else:
                stop_delay = min(MAX_STOP_DELAY, stop_delay + STOP_DELAY_STEP)

        RESULTS.append([i + 1, stim_type_go, stop_delay if stop_type else None, stop_type, rt, key, acc, experiment])


if __name__ == "__main__":

    # CONFIGURATION
    cfg = load_config('./config.yaml')
    FIX_TIME = cfg["FIX_TIME"]
    MAX_REACTION_TIME = cfg["MAX_REACTION_TIME"]
    MIN_STOP_DELAY = cfg["MIN_STOP_DELAY"]
    MAX_STOP_DELAY = cfg["MAX_STOP_DELAY"]
    STOP_DELAY_STEP = cfg["STOP_DELAY_STEP"]
    INITIAL_STOP_DELAY = cfg["INITIAL_STOP_DELAY"]
    N_TRN_A_TRIALS = cfg["N_TRN_A_TRIALS"]
    N_TRN_B_TRIALS = cfg["N_TRN_B_TRIALS"]
    N_EXP_A_BLOCKS = cfg["N_EXP_A_BLOCKS"]
    N_EXP_A_TRIALS = cfg["N_EXP_A_TRIALS"]
    REACTION_KEYS = cfg["REACTION_KEYS"]
    RESULTS = [
        ["NR", "DIRECTION", "DELAY", "COLOR", "RT", "REACTION", "ACC", "EXPERIMENT"]
    ]

    # INSTRUCTION TEXTS
    instr_trn_A = f"""Twoim zadaniem jest jak najszybsze naciśnięcie klawisza {REACTION_KEYS[0].upper()}, gdy zobaczysz strzałkę w lewo, lub klawisza {REACTION_KEYS[1].upper()}, gdy zobaczysz strzałkę w prawo. Czasu na decyzję jest niewiele, test wymaga skupienia, szybkich i trafnych reakcji.\n\nPrzed Tobą sesja treningowa, składająca się z {N_TRN_A_TRIALS} prób.\nNaciśnij klawisz SPACJA aby rozpocząć trening."""
    instr_trn_B = f"""Czas na kolejny etap. Zasady pozostają te same, z tym że gdy zobaczysz kwadratową obwódkę wokół strzałki, Twoim zadaniem jest NIE naciśnięcie żadnego z klawiszy. Jest to spore utrudnienie.\n\nPrzed Tobą ostatnia sesja treningowa, składająca się z {N_TRN_B_TRIALS} prób.\nNaciśnij klawisz SPACJA aby rozpocząć trening."""
    instr_exp_pre = f"""To już koniec etapu treningowego. Przed Tobą właściwa część eksperymentu, składają się z {N_EXP_A_BLOCKS} bloków po {N_EXP_A_TRIALS} prób każdy. Między każdym z bloków możliwa jest przerwa. Powodzenia!\nNaciśnij klawisz SPACJA aby rozpocząć test."""
    instr_exp_inter = f"""Przerwa nr <BREAK_NUMBER> (jeszcze <N_OF_BLOCKS_LEFT> bloków testowych).\nNaciśnij klawisz SPACJA aby kontynuować."""
    instr_end = """Dziękujemy za udział w badaniu."""

    # INITIALIZATION
    window = visual.Window(
        units="pix",
        color="gray",
        fullscr=True
    )
    window.setMouseVisible(False)
    clock = core.Clock()
    stim_go = {
        REACTION_KEYS[0]: visual.TextStim(win=window, text="←", height=40),
        REACTION_KEYS[1]: visual.TextStim(win=window, text="→", height=40)
    }
    stim_stop = {
        "red": visual.rect.Rect(win=window, units='pix', pos=(0, -5), size=60, lineColor="red", lineWidth=2.0),
        "green": visual.rect.Rect(win=window, units='pix', pos=(0, -5), size=60, lineColor="green", lineWidth=2.0),
        "black": visual.rect.Rect(win=window, units='pix', pos=(0, -5), size=60, lineColor="black", lineWidth=2.0)
    }
    stim_fix = visual.TextStim(win=window, text="+", height=40)
    stim_err = visual.TextStim(win=window, text="BŁĄD", height=40)

    # # TRAINING BLOCK 1 - GO trials
    show_text(text=instr_trn_A, win=window)
    experiment_block(
        n_trials=N_TRN_A_TRIALS,
        keys=REACTION_KEYS,
        experiment=False,
        fix_stim=stim_fix,
        fix_time=FIX_TIME,
        err_stim=stim_err,
        win=window
    )

    # TRAINING BLOCK 2 - GO + STOP trials
    show_text(text=instr_trn_B, win=window)
    experiment_block(
        n_trials=N_TRN_B_TRIALS,
        keys=REACTION_KEYS,
        experiment=False,
        fix_stim=stim_fix,
        fix_time=FIX_TIME,
        err_stim=stim_err,
        win=window,
        stop_trials_fraction=1 / 3
    )

    # EXPERIMENT BLOCKS
    show_text(text=instr_exp_pre, win=window)
    for j in range(N_EXP_A_BLOCKS):
        if j and range(1, N_EXP_A_BLOCKS - 1):
            show_text(
                instr_exp_inter
                .replace('<BREAK_NUMBER>', str(j))
                .replace('<N_OF_BLOCKS_LEFT>', str(N_EXP_A_BLOCKS - j)),
                win=window
            )
        experiment_block(
            n_trials=N_EXP_A_TRIALS,
            keys=REACTION_KEYS,
            experiment=True,
            fix_stim=stim_fix,
            fix_time=FIX_TIME,
            err_stim=stim_err,
            win=window,
            stop_trials_fraction=.25
        )

    # FINISH
    show_text(text=instr_end, win=window)

    # SAVE RESULTS
    with open("result.csv", 'w', newline="") as f:
        write = csv.writer(f)
        write.writerows(RESULTS)
