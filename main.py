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

# INSTRUCTIONS
instr_trn1 = """Twoim zadaniem jest jak najszybsze naciśnięcie klawisza A, gdy zobaczysz strzałkęw lewo, lub klawisza L, gdy zobaczysz strzałkę w prawo. Czasu na decyzję jest niewiele, test wymaga skupienia, szybkich i trafnych reakcji.\n\nPrzed Tobą sesja treningowa, składająca się z 15 prób.\nNaciśnij klawisz SPACJA aby rozpocząć trening."""
instr_trn2 = """Czas na kolejny etap. Zasady pozostają te same, z tym że gdy zobaczysz kwadratową obwódkę wokół strzałki, Twoim zadaniem jest NIE naciśnięcie żadnego z klawiszy. Jest to spore utrudnienie.\n\nPrzed Tobą ostatnia sesja treningowa, składająca sięz 20 prób.\nNaciśnij klawisz SPACJA aby rozpocząć trening."""
instr_exp1 = """To już koniec etapu treningowego. Przed Tobą właściwa część eksperymentu, składają się z 6 bloków po 120 prób każdy. Między każdym z bloków możliwa jest przerwa. Powodzenia!\nNaciśnij klawisz SPACJA aby rozpocząć test."""
instr_exp2 = """Przerwa nr n (jescze 6-n bloków testowych).\nNaciśnij klawisz SPACJA aby kontynuować."""
instr_end = """Dziękujemy za udział w badaniu."""

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
