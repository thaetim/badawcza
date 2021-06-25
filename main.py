# PROJEKT PROCEDURY BADAWCZEJ
# wybor procedury, np Stroop, Posner, Go-No-Go, stop-signal itp
# opis do czego to ma być (po krotce), do czego sluzyc, co badac, jak
# specyfikacja: dokladny opis procedury, ile triali, jaka kolejnosc, co przez ile trwa wyswietla
# pisanie procedury miesko projektu glowna czesc
# test na dwoch trzech osobach - czy zwraca dobre pliki dane i dziala
# obrona projektu - wylumaczyc jak dla czego dziala, specka i kod, kto za co odpowiadal

# krotki opis i temat: zaakceptowany do piatku (wyslac propo we wt albo sr) do 23:59 14.05
# 31.05 specyfikacja skonczona
#   pisanie proceur, testowanie

# obrona projektu do konca czerwca (sami ustalic termin) (trwa 30min okolo)
# 24h przed obrona - dostarczyc podzial pracy i projekt

# https://www.psytoolkit.org/experiment-library/stopsignal.html
# https://www.millisecond.com/download/library/stopsignaltask/

from psychopy import visual, core, event
import random
import csv


def reactions(key_list, max_reaction_time=float("inf")):
    event.clearEvents()
    keys = event.waitKeys(max_reaction_time, keyList=key_list.append("escape"))
    if keys and keys[0] == "escape":
        exit()
    if keys:
        print(keys[0])
    return keys[0] if keys else None


def show_text(text, win, keys=["space"]):
    visual.TextStim(win=window, text=text, height=20).draw()
    win.flip()
    reactions(keys)


def experiment_block(n_trials, keys, experiment, fix_time, fix_stim, win, stop_trials_fraction=0):

    stop_delay = INITIAL_STOP_DELAY

    trials_stop_types = [None] * int((1-stop_trials_fraction)*n_trials)
    for stop_key in (stim_stop.keys()):
        trials_stop_types += [stop_key] * int((stop_trials_fraction/len(stim_stop)*n_trials))
    random.shuffle(trials_stop_types)

    for i, stop_type in enumerate(trials_stop_types):
        stim_type_go = random.choice(list(stim_go.keys()))
        print(stim_type_go)

        # FIXATION STIMULUS
        fix_stim.draw()
        win.flip()
        core.wait(fix_time/1000)

        # GO STIMULUS
        stim_go[stim_type_go].draw()
        win.callOnFlip(clock.reset)
        win.flip()

        # STOP STIMULUS
        if stop_type:
            core.wait(stop_delay/1000)
            stim_go[stim_type_go].draw()
            stim_stop[stop_type].draw()
            win.flip()

        key = reactions(keys, MAX_REACTION_TIME/1000)
        rt = clock.getTime() if key else None

        acc = (stim_type_go == key)

        if stop_type:
            if acc:
                stop_delay = max(MIN_STOP_DELAY, stop_delay-STOP_DELAY_STEP)
            else:
                stop_delay = min(MAX_STOP_DELAY, stop_delay+STOP_DELAY_STEP)

        RESULTS.append([i + 1, stim_type_go, stop_delay if stop_type else None, rt, key, acc, experiment])


if __name__ == "__main__":

    # CONFIGURATION
    FIX_TIME = 2000
    MAX_REACTION_TIME = 1000

    MIN_STOP_DELAY = 150
    MAX_STOP_DELAY = 400
    STOP_DELAY_STEP = 50
    INITIAL_STOP_DELAY = 150

    N_TRN_A_TRIALS = 15
    N_TRN_B_TRIALS = 27
    N_EXP_A_BLOCKS = 6
    N_EXP_A_TRIALS = 120

    REACTION_KEYS = ["a", "l"]
    RESULTS = [
        ["NR", "DIRECTION", "DELAY", "RT", "REACTION", "ACC", "EXPERIMENT"]
    ]

    # INSTRUCTION TEXTS
    instr_trn_A = f"""Twoim zadaniem jest jak najszybsze naciśnięcie klawisza {REACTION_KEYS[0]}, gdy zobaczysz strzałkę w lewo, lub klawisza {REACTION_KEYS[1]}, gdy zobaczysz strzałkę w prawo. Czasu na decyzję jest niewiele, test wymaga skupienia, szybkich i trafnych reakcji.\n\nPrzed Tobą sesja treningowa, składająca się z {N_TRN_A_TRIALS} prób.\nNaciśnij klawisz SPACJA aby rozpocząć trening."""
    instr_trn_B = f"""Czas na kolejny etap. Zasady pozostają te same, z tym że gdy zobaczysz kwadratową obwódkę wokół strzałki, Twoim zadaniem jest NIE naciśnięcie żadnego z klawiszy. Jest to spore utrudnienie.\n\nPrzed Tobą ostatnia sesja treningowa, składająca się z {N_TRN_B_TRIALS} prób.\nNaciśnij klawisz SPACJA aby rozpocząć trening."""
    instr_exp_pre = f"""To już koniec etapu treningowego. Przed Tobą właściwa część eksperymentu, składają się z {N_EXP_A_BLOCKS} bloków po {N_EXP_A_TRIALS} prób każdy. Między każdym z bloków możliwa jest przerwa. Powodzenia!\nNaciśnij klawisz SPACJA aby rozpocząć test."""
    instr_exp_inter = f"""Przerwa nr <BREAK_NUMBER> (jeszcze <N_OF_BLOCKS_LEFT> bloków testowych).\nNaciśnij klawisz SPACJA aby kontynuować."""
    instr_end = """Dziękujemy za udział w badaniu."""

    # INITIALIZATION
    window = visual.Window(
        units="pix",
        color="gray",
        fullscr=False
    )
    window.setMouseVisible(False)
    clock = core.Clock()
    stim_go = {
        "left": visual.TextStim(win=window, text="←", height=40),
        "right": visual.TextStim(win=window, text="→", height=40)
    }
    stim_stop = {
        "red": visual.rect.Rect(win=window, units='pix', pos=(0, -5), size=60, lineColor="red", lineWidth=2.0),
        "green": visual.rect.Rect(win=window, units='pix', pos=(0, -5), size=60, lineColor="green", lineWidth=2.0),
        "black": visual.rect.Rect(win=window, units='pix', pos=(0, -5), size=60, lineColor="black", lineWidth=2.0)
    }
    stim_fix = visual.TextStim(win=window, text="+", height=40)

    # # TRAINING BLOCK 1 - GO trials
    show_text(text=instr_trn_A, win=window)
    experiment_block(
        n_trials=N_TRN_A_TRIALS,
        keys=REACTION_KEYS,
        experiment=False,
        fix_stim=stim_fix,
        fix_time=FIX_TIME,
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
        win=window,
        stop_trials_fraction=1/3
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
            experiment=False,
            fix_stim=stim_fix,
            fix_time=FIX_TIME,
            win=window,
            stop_trials_fraction=1/3
        )

    # FINISH
    show_text(text=instr_end, win=window)

    # SAVE RESULTS
    with open("result.csv", 'w', newline="") as f:
        write = csv.writer(f)
        write.writerows(RESULTS)
