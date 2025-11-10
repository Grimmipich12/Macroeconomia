#Librerie
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

import matplotlib 
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt

import numpy as np

import sys

import subprocess


def riavvia_programma():
    subprocess.Popen([sys.executable] + sys.argv)
    sys.exit()
    


#Introduzione
print(colorama.Fore.BLUE + "Modello reddito-spesa")



#Definizione funzioni
def value(messaggio):
    while True:
        input_utente = input(messaggio)
        try:
            valore = float(input_utente)
            return valore
        except ValueError:
            print(colorama.Fore.RED + f"{input_utente} non valido. Per favore, inserisci un numero.")

def parameter(messaggio):
    while True:
        input_utente = input(messaggio)
        try:
            parametro = float(input_utente)
            if 0 <= parametro <= 1:
                return parametro
            else:
                print(colorama.Fore.RED + "Input non valido. Per favore, inserisci un numero compreso tra 0 e 1 (es. 0.8).")
        except ValueError:
            print(colorama.Fore.RED + "Input non valido. Per favore, inserisci un numero compreso tra 0 e 1 (es. 0.8).")



#setup
while True:
    RM = str(input("desideri considerare un'economia chiusa o aperta? (C/A): "))
    if RM.lower() == "c" or RM.lower() == "a":
        break
    else:
        print(colorama.Fore.RED + f"{RM} non è valido, indicare C o A.")

while True:
    Occ = str(input("desideri considerare il livello di occupazione? (S/N): "))
    if Occ.lower() == "s" or Occ.lower() == "n":
        break
    else:
        print(colorama.Fore.RED + f"{Occ} non è valido, indicare S o N.")

if RM.lower() == "c":
    while True:
        SP = str(input("desideri considerare il settore pubblico? (S/N): "))
        if SP.lower() == "s" or SP.lower() == "n":
            pass
            if SP.lower() == "s":
                while True:
                    Tasse = str(input("desideri considerare le tasse esogene oppure endogene? (Es/En): "))
                    if Tasse.lower() == "es" or Tasse.lower() == "en":
                        break
                    else:
                        print(colorama.Fore.RED + f"{Tasse} non è valido, indicare Es o En.")
                break
            else:
                break
        else:
            print(colorama.Fore.RED + f"{SP} non è valido, indicare S o N.")



#Economia aperta
if RM.lower() == "a":
    while True:
        #inputs
        C_ = value("A quanto ammontano i consumi fissi? ")
        I_ = value("A quanto ammontano gli investimenti delle imprese? ")
        c = parameter("A quanto ammonta la propensione al consumo delle famiglie (inserire un valore tra 0 e 1)? ")
        G_ = value("A quanto ammonta la spesa pubblica? ")
        t = parameter("Qual è l'entità della pressione fiscale (inserire un valore tra 0 e 1)? ")
        TR_ = value("A quanto ammontano i trasferimenti pubblici alle famiglie? ")
        qw = parameter("A quanto ammonta la propensione ad importare del resto del mondo (inserire un valore tra 0 e 1)? ")
        q = parameter("A quanto ammonta la propensione ad importare dell'economia nazionale (inserire un valore tra 0 e 1)? ")
        Y_w = value("A quanto ammonta il PIL del resto del mondo? ")

        #Equations
        Z_ = C_+I_+G_+c*TR_+qw*Y_w
        z = 1/(1-(c*(1-t)-q))
        Y = z*Z_
        Yd = Y*(1-t)+TR_
        C = C_+c*Yd
        Sn = Yd-C
        BS = t*Y-(TR_+G_)
        NX = qw*Y_w-q*Y

        #disoccupazione
        if Occ.lower() == "s":
            η = value("A quanto ammonta la produttività del lavoro? ")
            N_ = value("A quanto ammonta la popolazione attiva (offerta di lavoro)? ")
            N = Y/η
            U = N_-N
            u = U/N_
            Y_ = η*N_
        else:
            pass

        #space
        print("---")
        print("")

        #Macro values
        print(f"La domanda autonoma ammonta a: {round(Z_,2)}")
        print(f"Il moltiplicatore keynesiano è: {round(z,2)}")
        print(f"Il PIL ammonta a: {round(Y,2)}")
        print(f"Il reddito disponibile ammonta a: {round(Yd,2)}")
        print(f"I consumi ammontano a: {round(C,2)}")
        if Sn > 0:
            print(f"Il risparmio delle famiglie ammonta a: {round(Sn,2)}")
        elif Sn == 0:
            print(f"Le famiglie consumano tutto il reddito a loro disposizione")
        elif Sn < 0:
            print(f"Le famiglie si indebitano per un ammontare pari a: {round(abs(Sn))}")
        if Occ.lower() == "s":
            print(f"La domanda di lavoro ammonta a {round(N,2)}")
            if U > 0:
                print(f"il numero di disoccupati ammonta a {round(U,2)}")
                print(f"la disoccupazione è al {round(u*100, 2)}%")
                print(f"Il reddito di pieno impiego sarebbe {round(Y_,2)}")
            elif U == 0:
                print(f"Non c'è disoccupazione")
            elif U < 0:
                print(f"C'è piena occupazione con un eccesso di domanda di lavoro di {abs(round(U,2))}")
        else:
            pass

        #Analysis:
            #Bilancio dello Stato
        if BS == 0:
            print("Il bilancio dello Stato è in equilibrio")
        elif BS > 0:
            print(f"Il bilancio dello Stato è in surplus finanziario di {round(BS,2)}")
        elif BS < 0:
            print(f"Il bilancio dello Stato è in deficit finanziario di {abs(round(BS,2))}")

        #Bilancia commerciale
        if NX == 0:
            print("La bilancia commerciale è in equilibrio")
        elif NX > 0:
            print(f"La bilancia commerciale è in surplus finanziario di {round(NX,2)}")
        elif NX < 0:
            print(f"La bilancia commerciale è in deficit finanziario di {abs(round(NX,2))}")

        #space
        print("---")
        print("")

        #Graphics
        #Mercato dei beni
        Y_gr = np.linspace(0, Y*2, 1000)
        Z_eq = Y_gr
        Z_gr = Z_+(c*(1-t)-q)*Y_gr
        #Con disoccupazione
        if Occ.lower() == "s":
            N_gr = (1/η)*Y_gr

            fig, (ax1, ax2) = plt.subplots(2, 1, num="Mercato dei beni e occupazione")
            ax1.set_xlim(left=0, right=Y*2)
            ax1.set_ylim(bottom=0, top=Y*2)
            ax2.set_xlim(left=0, right=Y*2)
            ax2.set_ylim(bottom=0, top=Y*2)
            ax1.set_title("Mercato dei beni", fontsize=20, family="Arial")

            #ax1 Setup
            ax1.set_xlabel("Y", fontweight="bold", loc="right")
            ax1.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
            ax1.vlines(Y, 0, Y, linestyle="--", color="gray", alpha=0.7)

            #ax1 lines
            ax1.plot(Y_gr, Z_eq, color="blue")
            ax1.plot(Y_gr, Z_gr, color="blue")

            #ax1 Points
            ax1.plot(Y, Y, "o", color="red", markersize=2)
            ax1.annotate("E", (Y, Y), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
            ax1.plot(0, Z_, "_", color="red", markersize=10)
            ax1.annotate(rf"$\overline{{Z}}={round(Z_)}$", (0, Z_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
            ax1.plot(Y, 0, "|", color="red", markersize=10)
            ax1.annotate(f"Y*={round(Y)}", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

            #ax2 Setup
            ax2.set_xlabel("Y", fontweight="bold", loc="right")
            ax2.set_ylabel("N", fontweight="bold", loc="top", rotation=0)
            ax2.vlines(Y, 0, Y*2, linestyle="--", color="gray", alpha=0.7)
            ax2.hlines(N, 0, Y, linestyle="--", color="gray", alpha=0.7)
            ax2.vlines(Y_, 0, N_, linestyle="--", color="gray", alpha=0.7)
            ax2.hlines(N_, 0, Y_, linestyle="--", color="gray", alpha=0.7)
            #ax2 lines
            ax2.plot(Y_gr, N_gr, color="blue")
            #ax2 Points
            ax2.plot(Y, N, "o", color="red", markersize=2)
            ax2.plot(0, N, "_", color="red", markersize=10)
            ax2.plot(Y_, N_, "o", color="red", markersize=2)
            ax2.annotate(f"N*={round(N)}", (0, N), xytext=(55, 5), textcoords="offset points", fontsize=12, color="black")
            ax2.plot(0, N_, "_", color="red", markersize=10)
            ax2.annotate(rf"$\overline{{N}}={round(N_)}$", (0, N_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
            if Y_ > Y:
                ax2.plot(Y_, 0, "|", color="red", markersize=10)
                ax2.annotate(rf"$\overline{{Y}}={round(Y_)}$", (Y_, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
            else:
                ax2.plot(Y_, 0, "|", color="red", markersize=10)
                ax2.annotate(r"$\overline{Y}$", (Y_, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
            ax2.plot(Y, 0, "|", color="red", markersize=10)
            ax2.annotate("Y*", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

            pass

        #Senza disoccupazione
        if Occ.lower() == "n":
            plt.figure(num="Mercato dei beni")
            plt.xlim(left=0, right=Y*2)
            plt.ylim(bottom=0, top=Y*2)
            plt.title("Mercato dei beni", fontsize=20, family="Arial")

            #Setup
            plt.xlabel("Y", fontweight="bold", loc="right")
            plt.ylabel("Z", fontweight="bold", loc="top")
            plt.vlines(Y, 0, Y, linestyle="--", color="gray", alpha=0.7)

            #Lines
            plt.plot(Y_gr, Z_eq, color="blue")
            plt.plot(Y_gr, Z_gr, color="blue")

            #Points
            plt.plot(Y, Y, "o", color="red", markersize=2)
            plt.annotate("E", (Y, Y), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
            plt.plot(0, Z_, "_", color="red", markersize=10)
            plt.annotate(rf"$\overline{{Z}}={round(Z_)}$", (0, Z_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
            plt.plot(Y, 0, "|", color="red", markersize=10)
            plt.annotate(f"Y*={round(Y)}", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

            pass

        #Risparmio delle famiglie
        plt.figure(num="Risparmio e investimenti")
        Yd_gr = np.linspace(0, Yd*2, 1000)
        SI_gr = -C_+(1-c)*Yd_gr

        plt.xlim(left=0, right=Yd*2)
        plt.ylim(bottom=-C_*2-100, top=Yd)
        plt.hlines(0, 0, Yd*2, color="black", linewidth=0.5)
        plt.title("Risparmio e investimenti", fontsize=20, family="Arial")

        #Setup
        plt.xlabel("Yd", fontweight="bold", loc="right")
        plt.ylabel("Sn", fontweight="bold", loc="top")
        plt.vlines(Yd, 0, Sn, linestyle="--", color="gray", alpha=0.7)

        #Lines
        plt.plot(Yd_gr, SI_gr, color="blue")
        plt.hlines(Sn, 0, Yd*2, color="blue")

        #Points
        plt.plot(Yd, Sn, "o", color="red", markersize=2)
        plt.annotate("E", (Yd, Sn), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
        plt.plot(0, Sn, "_", color="red", markersize=10)
        plt.annotate(f"Sn*={round(Sn)}", (0, Sn), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
        plt.plot(Yd, 0, "|", color="red", markersize=10)
        plt.annotate(f"Yd*={round(Yd)}", (Yd, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
        plt.plot(0, -C_, "_", color="red", markersize=10)
        plt.annotate(rf"-$\overline{{C}}={round(-C_)}$", (0, -C_), xytext=(2, -15), textcoords="offset points", fontsize=12, color="black")

        #Bilancio dello Stato
        Y_gr = np.linspace(0, Y*2, 1000)
        BS_gr = -(G_+TR_)+(t*Y_gr)

        fig, (ax1, ax2) = plt.subplots(2, 1, num="Bilancio dello Stato")
        ax1.set_xlim(left=0, right=Y*2)
        ax1.set_ylim(bottom=0, top=Y*2)
        ax2.set_xlim(left=0, right=Y*2)
        ax2.set_ylim(bottom=-(G_+TR_)*3-100, top=Y*2)
        ax1.set_title("Bilancio dello Stato", fontsize=20, family="Arial")

        #ax1 Setup
        ax1.set_xlabel("Y", fontweight="bold", loc="right")
        ax1.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
        ax1.vlines(Y, 0, Y, linestyle="--", color="gray", alpha=0.7)

        #ax1 lines
        ax1.plot(Y_gr, Z_eq, color="blue")
        ax1.plot(Y_gr, Z_gr, color="blue")

        #ax1 Points
        ax1.plot(Y, Y, "o", color="red", markersize=2)
        ax1.annotate("E", (Y, Y), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
        ax1.plot(0, Z_, "_", color="red", markersize=10)
        ax1.annotate(rf"$\overline{{Z}}={round(Z_)}$", (0, Z_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
        ax1.plot(Y, 0, "|", color="red", markersize=10)
        ax1.annotate(f"Y*={round(Y)}", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

        #ax2 Setup
        ax2.set_xlabel("Y", fontweight="bold", loc="right")
        ax2.set_ylabel("BS", fontweight="bold", loc="top", rotation=0)
        ax2.vlines(Y, -(G_+TR_)+(Y*t), Y*2, linestyle="--", color="gray", alpha=0.7)
        ax2.hlines(BS, 0, Y, linestyle="--", color="gray", alpha=0.7)

        #ax2 lines
        ax2.hlines(0, 0, Y*2, color="black", linewidth=0.5)
        ax2.plot(Y_gr, BS_gr, color="blue")

        #ax2 Points
        ax2.plot(Y, -(G_+TR_)+(Y*t), "o", color="red", markersize=2)
        ax2.annotate(f"BS={round(BS)}", (0, BS), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
        ax2.plot(0, -(G_+TR_), "_", color="red", markersize=10)
        ax2.annotate(rf"-($\overline{{G}}$+" + rf"$\overline{{TR}}$)={-(G_+TR_)}", (0, -(G_+TR_)), xytext=(5, -15), textcoords="offset points", fontsize=12, color="black")
        ax2.plot(0, BS, "_", color="red", markersize=10)

        #Bilancia commerciale
        Y_gr = np.linspace(0, Y*2, 1000)
        NX_gr = (qw*Y_w)-(q*Y_gr)

        fig, (ax1, ax2) = plt.subplots(2, 1, num="Bilancia commerciale")
        ax1.set_title("Bilancia commerciale", fontsize=20, family="Arial")
        ax1.set_xlim(left=0, right=Y*2)
        ax1.set_ylim(bottom=0, top=Y*2)
        ax2.set_xlim(left=0, right=Y*2)
        ax2.set_ylim(bottom=NX*2-300, top=Y*2)

        #ax1 Setup
        ax1.set_xlabel("Y", fontweight="bold", loc="right")
        ax1.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
        ax1.vlines(Y, 0, Y, linestyle="--", color="gray", alpha=0.7)

        #ax1 lines
        ax1.plot(Y_gr, Z_eq, color="blue")
        ax1.plot(Y_gr, Z_gr, color="blue")

        #ax1 Points
        ax1.plot(Y, Y, "o", color="red", markersize=2)
        ax1.annotate("E", (Y, Y), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
        ax1.plot(0, Z_, "_", color="red", markersize=10)
        ax1.annotate(rf"$\overline{{Z}}={round(Z_)}$", (0, Z_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
        ax1.plot(Y, 0, "|", color="red", markersize=10)
        ax1.annotate(f"Y*={round(Y)}", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

        #ax2 Setup
        ax2.set_xlabel("Y", fontweight="bold", loc="right")
        ax2.set_ylabel("NX", fontweight="bold", loc="top", rotation=0)
        ax2.vlines(Y, NX, Y*2, linestyle="--", color="gray", alpha=0.7)
        ax2.hlines(NX, 0, Y, linestyle="--", color="gray", alpha=0.7)

        #ax2 lines
        ax2.hlines(0, 0, Y*2, color="black", linewidth=0.5)
        ax2.plot(Y_gr, NX_gr, color="blue")

        #ax2 Points
        ax2.plot(Y, NX, "o", color="red", markersize=2)
        ax2.annotate(f"NX={round(NX)}", (0, NX), xytext=(10, -15), textcoords="offset points", fontsize=12, color="black")
        ax2.plot(0, NX, "_", color="red", markersize=10)
        ax2.plot(0, qw*Y_w, "_", color="red", markersize=10)
        ax2.annotate(rf"qw$\overline{{Y}}$w", (0, qw*Y_w), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

        print(colorama.Fore.RED + "CHIUDERE TUTTI I GRAFICI PER POTER CONTINUARE.") 
        plt.show()

        #Variazioni
        while True:
            Variazione = str(input("Desideri variare una o più variabili per un confronto (S/N)? "))
            if Variazione.lower() == "s" or Variazione.lower() == "n":
                pass
            else:
                print(colorama.Fore.RED + f"{Variazione} non è valido, indicare S o N.")
                
            if Variazione.lower() == "s":

                while True:
                    VarC = str(input("desideri variare i consumi fissi? (S/N): "))
                    if VarC.lower() == "s" or VarC.lower() == "n":
                        break
                    else:
                        print(colorama.Fore.RED + f"{VarC} non è valido, indicare S o N.")
                if VarC.lower() == "s":
                    C_2 = value("A quanto ammontano i NUOVI consumi fissi? ")
                elif VarC.lower() == "n":
                    C_2 = C_
                else:
                    pass

                while True:
                    VarI = str(input("desideri variare gli investimenti? (S/N): "))
                    if VarI.lower() == "s" or VarI.lower() == "n":
                        break
                    else:
                        print(colorama.Fore.RED + f"{VarI} non è valido, indicare S o N.")
                if VarI.lower() == "s":
                    I_2 = value("A quanto ammontano i NUOVI investimenti? ")
                elif VarI.lower() == "n":
                    I_2 = I_
                else:
                    pass
                
                while True:
                    Varc = str(input("desideri variare la propensione al consumo delle famiglie? (S/N): "))
                    if Varc.lower() == "s" or Varc.lower() == "n":
                        break
                    else:
                        print(colorama.Fore.RED + f"{Varc} non è valido, indicare S o N.")
                if Varc.lower() == "s":
                    c2 = parameter("A quanto ammonta la NUOVA propensione al consumo (inserire un valore tra 0 e 1)? ")
                elif Varc.lower() == "n":
                    c2 = c
                else:
                    pass

                while True:
                    VarG = str(input("desideri variare la spesa pubblica? (S/N): "))
                    if VarG.lower() == "s" or VarG.lower() == "n":
                        break
                    else:
                        print(colorama.Fore.RED + f"{VarG} non è valido, indicare S o N.")
                if VarG.lower() == "s":
                    G_2 = value("A quanto ammonta la NUOVA spesa pubblica? ")
                elif VarG.lower() == "n":
                    G_2 = G_
                else:
                    pass

                while True:
                    Vart = str(input("desideri variare la pressione fiscale? (S/N): "))
                    if Vart.lower() == "s" or Vart.lower() == "n":
                        break
                    else:
                        print(colorama.Fore.RED + f"{Vart} non è valido, indicare S o N.")
                if Vart.lower() == "s":
                    t2 = parameter("A quanto ammonta la NUOVA pressione fiscale (inserire un valore tra 0 e 1)?")
                elif Vart.lower() == "n":
                    t2 = t
                else:
                    pass

                while True:
                    VarTR = str(input("desideri variare i trasferimenti pubblici alle famiglie? (S/N): "))
                    if VarTR.lower() == "s" or VarTR.lower() == "n":
                        break
                    else:
                        print(colorama.Fore.RED + f"{VarTR} non è valido, indicare S o N.")
                if VarTR.lower() == "s":
                    TR_2 = value("A quanto ammontano i NUOVI trasferimenti pubblici alle famiglie? ")
                elif VarTR.lower() == "n":
                    TR_2 = TR_
                else:
                    pass

                while True:
                    Varqw = str(input("desideri variare la propensione ad importare del resto del mondo? (S/N): "))
                    if Varqw.lower() == "s" or Varqw.lower() == "n":
                        break
                    else:
                        print(colorama.Fore.RED + f"{Varqw} non è valido, indicare S o N.")
                if Varqw.lower() == "s":
                    qw2 = parameter("A quanto ammonta la NUOVA propensione ad importare del resto del mondo (inserire un valore tra 0 e 1)? ")
                elif Varqw.lower() == "n":
                    qw2 = qw
                else:
                    pass

                while True:
                    Varq = str(input("desideri variare la propensione ad importare dell'economia nazionale? (S/N): "))
                    if Varq.lower() == "s" or Varq.lower() == "n":
                        break
                    else:
                        print(colorama.Fore.RED + f"{Varq} non è valido, indicare S o N.")
                if Varq.lower() == "s":
                    q2 = parameter("A quanto ammonta la NUOVA propensione ad importare dell'economia nazionale (inserire un valore tra 0 e 1)? ")
                elif Varq.lower() == "n":
                    q2 = q
                else:
                    pass

                while True:
                    VarYw = str(input("desideri variare il PIL del resto del mondo? (S/N): "))
                    if VarYw.lower() == "s" or VarYw.lower() == "n":
                        break
                    else:
                        print(colorama.Fore.RED + f"{VarYw} non è valido, indicare S o N.")
                if VarYw.lower() == "s":
                    Y_w2 = value("A quanto ammonta il NUOVO PIL del resto del mondo? ")
                elif VarYw.lower() == "n":
                    Y_w2 = Y_w
                else:
                    pass

                if Occ.lower() == "s":
                    while True:
                        Varη = str(input("desideri variare la produttività dei lavoratori? (S/N): "))
                        if Varη.lower() == "s" or Varη.lower() == "n":
                            break
                        else:
                            print(colorama.Fore.RED + f"{Varη} non è valido, indicare S o N.")
                    if Varη.lower() == "s":
                        η2 = value("A quanto ammonta la NUOVA produttività dei lavoratori? ")
                    elif Varη.lower() == "n":
                        η2 = η
                    else:
                        pass

                    while True:
                        VarN_ = str(input("desideri variare l'offerta di lavoro? (S/N): "))
                        if VarN_.lower() == "s" or VarN_.lower() == "n":
                            break
                        else:
                            print(colorama.Fore.RED + f"{VarN_} non è valido, indicare S o N.")
                    if VarN_.lower() == "s":
                        N_2 = value("A quanto ammonta la NUOVA offerta di lavoro? ")
                    elif VarN_.lower() == "n":
                        N_2 = N_
                    else:
                        pass

                #space
                print("---")
                print("")                

                #Equations
                Z_2 = C_2+I_2+G_2+c2*TR_2+qw2*Y_w2
                z2 = 1/(1-(c2*(1-t2)-q2))
                Y2 = z2*Z_2
                Yd2 = (1-t2)*Y2+TR_2
                C2 = C_2+c2*Yd2
                Sn2 = Yd2-C2
                BS2 = Y2*t2-(TR_2+G_2)
                NX2 = qw2*Y_w2-q2*Y2
                if Occ.lower() == "s":
                    N2 = Y2/η2
                    U2 = N_2-N2
                    u2 = U2/N_2

                #Macro values (variazioni)
                if Z_2 > Z_:
                    print(f"Ora la domanda autonoma ammonta a: {round(Z_2,2)}" + f" {Fore.GREEN}(+{round(Z_2-Z_, 2)})")
                elif Z_2 == Z_:
                    print(f"La domanda autonoma è rimasta invariata: {round(Z_2,2)}")
                elif Z_2 < Z_:
                    print(f"Ora la domanda autonoma ammonta a: {round(Z_2,2)}" + f" {Fore.RED}({round(Z_2-Z_, 2)})")

                if z2 > z:
                    print(f"Ora il moltiplicatore keynesiano è: {round(z2,2)}" + f" {Fore.GREEN}(+{round(z2-z, 2)})")
                elif z2 == z:
                    print(f"Il moltiplicatore keynesiano è rimasto invariato: {round(z2,2)}")
                elif z2 < z:
                    print(f"Ora il moltiplicatore keynesiano è: {round(z2,2)}" + f" {Fore.RED}({round(z2-z, 2)})")

                if Y2 > Y:
                    print(f"Ora il PIL ammonta a: {round(Y2,2)}" + f" {Fore.GREEN}(+{round(Y2-Y, 2)})")
                elif Y2 == Y:
                    print(f"Il PIL è rimasto invariato: {round(Y2,2)}")
                elif Y2 < Y:
                    print(f"Ora il PIL ammonta a: {round(Y2,2)}" + f" {Fore.RED}({round(Y2-Y, 2)})")

                if C2 > C:
                    print(f"Ora i consumi ammontano a: {round(C2,2)}" + f" {Fore.GREEN}(+{round(C2-C, 2)})")
                elif C2 == C:
                    print(f"I consumi sono rimasti invariati: {round(C2,2)}")
                elif C2 < C:
                    print(f"Ora i consumi ammontano a: {round(C2,2)}" + f" {Fore.RED}({round(C2-C, 2)})")

                if Sn2 > Sn:
                    print(f"Ora i risparmi delle famiglie ammontano a: {round(Sn2,2)}" + f" {Fore.GREEN}(+{round(Sn2-Sn, 2)})")
                elif Sn2 == Sn:
                    print(f"I risparmi delle famiglie sono rimasti invariati: {round(Sn2,2)}")
                elif Sn2 < Sn:
                    print(f"Ora i risparmi delle famiglie ammontano a: {round(Sn2,2)}" + f" {Fore.RED}({round(Sn2-Sn, 2)})")
                elif Sn2 == 0:
                    print(f"Le famiglie consumano tutto il reddito a loro disposizione")
                elif Sn2 < 0:
                    print(f"Le famiglie si indebitano per un ammontare pari a: {abs(round(Sn2,2))}")

                if BS2 > BS:
                    print(f"Ora il bilancio dello Stato ammonta a: {round(BS2,2)}" + f" {Fore.GREEN}(+{round(BS2-BS, 2)})")
                elif BS2 == BS:
                    print(f"Il bilancio dello Stato è rimasto invariato: {round(BS2,2)}")
                elif BS2 < BS:
                    print(f"Ora il bilancio dello Stato ammonta a: {round(BS2,2)}" + f" {Fore.RED}({round(BS2-BS, 2)})")
                if BS2 == 0:
                    print("Il bilancio dello Stato è in equilibrio")
                elif BS2 > 0:
                    print(f"Il bilancio dello Stato è in surplus finanziario di {round(BS2,2)}")
                elif BS2 < 0:
                    print(f"Il bilancio dello Stato è in deficit finanziario di {abs(round(BS2,2))}")

                if NX2 > NX:
                    print(f"Ora la bilancia commerciale ammonta a: {round(NX2,2)}" + f" {Fore.GREEN}(+{round(NX2-NX, 2)})")
                elif NX2 == NX:
                    print(f"La bilancia commerciale è rimasta invariata: {round(NX2,2)}")
                elif NX2 < NX:
                    print(f"Ora la bilancia commerciale ammonta a: {round(NX2,2)}" + f" {Fore.RED}({round(NX2-NX, 2)})")
                if NX2 == 0:
                    print("La bilancia commerciale è rimasta in equilibrio")
                elif NX2 > 0:
                    print(f"La bilancia commerciale è in surplus finanziario di {round(NX2,2)}")
                elif NX2 < 0:
                    print(f"La bilancia commerciale è in deficit finanziario di {abs(round(NX2,2))}")

                if Occ.lower() == "s":
                    if N2 > N:
                        print(f"Ora la domanda di lavoro ammonta a: {round(N2,2)}" + f" {Fore.GREEN}(+{round(N2-N, 2)})")
                    elif N2 == N:
                        print(f"La domanda di lavoro è rimasta invariata: {round(N2,2)}")
                    elif N2 < N:
                        print(f"Ora la domanda di lavoro ammonta a: {round(N2,2)}" + f" {Fore.RED}({round(N2-N, 2)})")

                    if U2 > U:
                        print(f"Ora la disoccupazione ammonta a: {round(U2,2)}" + f" {Fore.RED}(+{round(U2-U, 2)})")
                    elif U2 == U:
                        print(f"La disoccupazione è rimasta invariata: {round(U2,2)}")
                    elif U2 < U:
                        print(f"Ora la disoccupazione ammonta a: {round(U2,2)}" + f" {Fore.GREEN}({round(U2-U, 2)})")
                    if U2 > 0:
                        print(f"il numero di disoccupati ammonta a {round(U2,2)}")
                        print(f"la disoccupazione è al {round(u2*100, 2)}%")
                        print(f"Il reddito di pieno impiego sarebbe {round(η2*N_2,2)}")
                    elif U2 == 0:
                        print(f"Non c'è disoccupazione")
                    elif U2 < 0:
                        print(f"C'è piena occupazione con un eccesso di domanda di lavoro di {abs(round(U2,2))}")
                

                #Graph_Variations
                #Mercato dei beni con occupazione_Variazione
                if Occ.lower() == "s":
                    fig, axs = plt.subplots(2, 2, num="Mercato dei beni e occupazione - confronto")

                    ax11 = axs[0, 0]
                    ax21 = axs[1, 0]
                    ax12 = axs[0, 1]
                    ax22 = axs[1, 1]

                    Y_gr = np.linspace(0, Y*2, 1000)
                    Z_eq = Y_gr
                    Z_gr = Z_+(c*(1-t)-q)*Y_gr

                    N_gr = (1/η)*Y_gr

                    ax11.set_title("Mercato dei beni (t1)", fontsize=20, family="Arial")
                    ax11.set_xlim(left=0, right=Y*2)
                    ax11.set_ylim(bottom=0, top=Y*2)
                    ax21.set_xlim(left=0, right=Y*2)
                    ax21.set_ylim(bottom=0, top=Y*2)

                    Y_gr2 = np.linspace(0, Y2*2, 1000)
                    Z_eq2 = Y_gr2
                    Z_gr2 = Z_2+(c2*(1-t2)-q2)*Y_gr2
                    N_gr2 = (1/η2)*Y_gr2
                    
                    ax12.set_title("Mercato dei beni (t2)", fontsize=20, family="Arial")
                    ax12.set_xlim(left=0, right=Y*2)
                    ax12.set_ylim(bottom=0, top=Y*2)
                    ax22.set_xlim(left=0, right=Y*2)
                    ax22.set_ylim(bottom=0, top=Y*2)

                    #ax11 Setup
                    ax11.set_xlabel("Y", fontweight="bold", loc="right")
                    ax11.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
                    ax11.vlines(Y, 0, Y, linestyle="--", color="gray", alpha=0.7)

                    #ax21 Setup
                    ax21.set_xlabel("Y", fontweight="bold", loc="right")
                    ax21.set_ylabel("N", fontweight="bold", loc="top", rotation=0)
                    ax21.vlines(Y, 0, Y*2, linestyle="--", color="gray", alpha=0.7)
                    ax21.hlines(N, 0, Y, linestyle="--", color="gray", alpha=0.7)
                    ax21.vlines(Y_, 0, N_, linestyle="--", color="gray", alpha=0.7)
                    ax21.hlines(N_, 0, Y_, linestyle="--", color="gray", alpha=0.7)

                    #ax12 Setup
                    ax12.set_xlabel("Y", fontweight="bold", loc="right")
                    ax12.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
                    ax12.vlines(Y2, 0, Y2, linestyle="--", color="gray", alpha=0.7)

                    #ax22 Setup
                    ax22.set_xlabel("Y", fontweight="bold", loc="right")
                    ax22.set_ylabel("N", fontweight="bold", loc="top", rotation=0)
                    ax22.vlines(Y2, 0, Y2*2, linestyle="--", color="gray", alpha=0.7)
                    ax22.hlines(N2, 0, Y2, linestyle="--", color="gray", alpha=0.7)
                    ax22.vlines(η2*N_2, 0, N_2, linestyle="--", color="gray", alpha=0.7)
                    ax22.hlines(N_2, 0, η2*N_2, linestyle="--", color="gray", alpha=0.7)

                    #ax11 lines
                    ax11.plot(Y_gr, Z_eq, color="blue")
                    ax11.plot(Y_gr, Z_gr, color="blue")

                    #ax21 lines
                    ax21.plot(Y_gr, N_gr, color="blue")

                    #ax12 lines
                    ax12.plot(Y_gr2, Z_eq2, color="blue")
                    ax12.plot(Y_gr2, Z_gr2, color="blue")
                    
                    #ax22 lines
                    ax22.plot(Y_gr2, N_gr2, color="blue")

                    #ax11 Points
                    ax11.plot(Y, Y, "o", color="red", markersize=2)
                    ax11.annotate("E", (Y, Y), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                    ax11.plot(0, Z_, "_", color="red", markersize=10)
                    ax11.annotate(rf"$\overline{{Z}}={round(Z_)}$", (0, Z_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax11.plot(Y, 0, "|", color="red", markersize=10)
                    ax11.annotate(f"Y*={round(Y)}", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                    #ax21 Points
                    ax21.plot(Y, N, "o", color="red", markersize=2)
                    ax21.plot(0, N, "_", color="red", markersize=10)
                    ax21.plot(Y_, N_, "o", color="red", markersize=2)
                    ax21.annotate(f"N*={round(N)}", (0, N), xytext=(55, 5), textcoords="offset points", fontsize=12, color="black")
                    ax21.plot(0, N_, "_", color="red", markersize=10)
                    ax21.annotate(rf"$\overline{{N}}={round(N_)}$", (0, N_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax21.plot(Y, 0, "|", color="red", markersize=10)
                    ax21.annotate("Y*", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax21.plot(Y_, 0, "|", color="red", markersize=10)
                    ax21.annotate(rf"$\overline{{Y}}={round(Y_)}$", (Y_, 0), xytext=(2, -35), textcoords="offset points", fontsize=12, color="black")

                    #ax12 Points
                    ax12.plot(Y2, Y2, "o", color="red", markersize=2)
                    ax12.annotate("E", (Y2, Y2), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                    ax12.plot(0, Z_2, "_", color="red", markersize=10)
                    ax12.annotate(rf"$\overline{{Z2}}={round(Z_2)}$", (0, Z_2), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax12.plot(Y2, 0, "|", color="red", markersize=10)
                    ax12.annotate(f"Y2*={round(Y2)}", (Y2, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                    #ax22 Points
                    ax22.plot(Y2, N2, "o", color="red", markersize=2)
                    ax22.plot(0, N2, "_", color="red", markersize=10)
                    ax22.plot(η2*N_2, N_2, "o", color="red", markersize=2)
                    ax22.annotate(f"N2*={round(N2)}", (0, N2), xytext=(55, 5), textcoords="offset points", fontsize=12, color="black")
                    ax22.plot(0, N_2, "_", color="red", markersize=10)
                    ax22.annotate(rf"$\overline{{N2}}={round(N_2)}$", (0, N_2), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax22.plot(Y2, 0, "|", color="red", markersize=10)
                    ax22.annotate("Y2*", (Y2, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax22.plot(η2*N_2, 0, "|", color="red", markersize=10)
                    ax22.annotate(rf"$\overline{{Y2}}={round(η2*N_2)}$", (η2*N_2, 0), xytext=(2, -35), textcoords="offset points", fontsize=12, color="black")

                    pass

                #Mercato dei beni senza occupazione_Variazione
                if Occ.lower() == "n":
                    fig, axs = plt.subplots(1, 2, num="Mercato dei beni - confronto")

                    ax11 = axs[0]
                    ax12 = axs[1]

                    Y_gr = np.linspace(0, Y*2, 1000)
                    Z_eq = Y_gr
                    Z_gr = Z_+(c*(1-t)-q)*Y_gr

                    Y_gr2 = np.linspace(0, Y2*2, 1000)
                    Z_eq2 = Y_gr2
                    Z_gr2 = Z_2+(c2*(1-t2)-q2)*Y_gr2

                    ax11.set_title("Mercato dei beni(t1)", fontsize=20, family="Arial")
                    ax11.set_xlim(left=0, right=Y*2)
                    ax11.set_ylim(bottom=0, top=Y*2)

                    ax12.set_title("Mercato dei beni(t2)", fontsize=20, family="Arial")
                    ax12.set_xlim(left=0, right=Y*2)
                    ax12.set_ylim(bottom=0, top=Y*2)

                    #ax11 Setup
                    ax11.set_xlabel("Y", fontweight="bold", loc="right")
                    ax11.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
                    ax11.vlines(Y, 0, Y, linestyle="--", color="gray", alpha=0.7)

                    #ax12 Setup
                    ax12.set_xlabel("Y", fontweight="bold", loc="right")
                    ax12.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
                    ax12.vlines(Y2, 0, Y2, linestyle="--", color="gray", alpha=0.7)

                    #ax11 lines
                    ax11.plot(Y_gr, Z_eq, color="blue")
                    ax11.plot(Y_gr, Z_gr, color="blue")

                    #ax12 lines
                    ax12.plot(Y_gr2, Z_eq2, color="blue")
                    ax12.plot(Y_gr2, Z_gr2, color="blue")

                    #ax11 Points
                    ax11.plot(Y, Y, "o", color="red", markersize=2)
                    ax11.annotate("E", (Y, Y), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                    ax11.plot(0, Z_, "_", color="red", markersize=10)
                    ax11.annotate(rf"$\overline{{Z}}={round(Z_)}$", (0, Z_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax11.plot(Y, 0, "|", color="red", markersize=10)
                    ax11.annotate(f"Y*={round(Y)}", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                    #ax12 Points
                    ax12.plot(Y2, Y2, "o", color="red", markersize=2)
                    ax12.annotate("E", (Y2, Y2), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                    ax12.plot(0, Z_2, "_", color="red", markersize=10)
                    ax12.annotate(rf"$\overline{{Z2}}={round(Z_2)}$", (0, Z_2), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax12.plot(Y2, 0, "|", color="red", markersize=10)
                    ax12.annotate(f"Y*={round(Y2)}", (Y2, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                    pass

                #Risparmio delle famiglie_Variazione
                fig, axs = plt.subplots(1, 2, num="Risparmio e investimenti - confronto")

                ax11 = axs[0]
                ax12 = axs[1]

                Y_gr = np.linspace(0, Yd*2, 1000)
                SI_gr = -C_+(1-c)*Y_gr

                Y_gr2 = np.linspace(0, Yd2*2, 1000)
                SI_gr2 = -C_2+(1-c2)*Y_gr2

                ax11.set_title("Risparmio e investimenti (t1)", fontsize=20, family="Arial")
                ax11.set_xlim(left=0, right=Yd*2) 
                ax11.set_ylim(bottom=-C_*2-100, top=Yd)

                ax12.set_title("Risparmio e investimenti (t2)", fontsize=20, family="Arial")
                ax12.set_xlim(left=0, right=Yd*2) 
                ax12.set_ylim(bottom=-C_*2-100, top=Yd)

                ax11.hlines(0, 0, Yd*2, color="black", linewidth=0.5)
                ax12.hlines(0, 0, Yd2*2, color="black", linewidth=0.5)

                #ax11 Setup
                ax11.set_xlabel("Yd", fontweight="bold", loc="right")
                ax11.set_ylabel("Sn", fontweight="bold", loc="top")
                ax11.vlines(Yd, 0, Sn, linestyle="--", color="gray", alpha=0.7)

                #ax12 Setup
                ax12.set_xlabel("Yd", fontweight="bold", loc="right")
                ax12.set_ylabel("Sn", fontweight="bold", loc="top")
                ax12.vlines(Yd2, 0, Sn2, linestyle="--", color="gray", alpha=0.7)

                #ax11 lines
                ax11.plot(Y_gr, SI_gr, color="blue")
                ax11.hlines(Sn, 0, Yd*2, color="blue")

                #ax12 lines
                ax12.plot(Y_gr2, SI_gr2, color="blue")
                ax12.hlines(Sn2, 0, Yd2*2, color="blue")

                #ax11 Points
                ax11.plot(Yd, Sn, "o", color="red", markersize=2)
                ax11.annotate("E", (Yd, Sn), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                ax11.plot(0, Sn, "_", color="red", markersize=10)
                ax11.annotate(f"Sn*={round(Sn)}", (0, Sn), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                ax11.plot(Yd, 0, "|", color="red", markersize=10)
                ax11.annotate(f"Yd*={round(Yd)}", (Yd, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                ax11.plot(0, -C_, "_", color="red", markersize=10)
                ax11.annotate(rf"-$\overline{{C}}={round(-C_)}$", (0, -C_), xytext=(2, -15), textcoords="offset points", fontsize=12, color="black")

                #ax12 Points
                ax12.plot(Yd2, Sn2, "o", color="red", markersize=2)
                ax12.annotate("E", (Yd2, Sn2), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                ax12.plot(0, Sn2, "_", color="red", markersize=10)
                ax12.annotate(f"Sn2*={round(Sn2)}", (0, Sn2), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                ax12.plot(Yd2, 0, "|", color="red", markersize=10)
                ax12.annotate(f"Yd2*={round(Yd2)}", (Yd2, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                ax12.plot(0, -C_2, "_", color="red", markersize=10)
                ax12.annotate(rf"-$\overline{{C2}}={round(-C_2)}$", (0, -C_2), xytext=(2, -15), textcoords="offset points", fontsize=12, color="black")

                #Bilancio dello Stato_Variazione
                fig, axs = plt.subplots(2, 2, num="Bilancio dello Stato - confronto")

                ax11 = axs[0, 0]
                ax21 = axs[1, 0]
                ax12 = axs[0, 1]
                ax22 = axs[1, 1]

                Y_gr = np.linspace(0, Y*2, 1000)
                BS_gr = -(G_+TR_)+(t*Y_gr)

                ax11.set_title("Bilancio dello Stato (t1)", fontsize=20, family="Arial")
                ax11.set_xlim(left=0, right=Y*2)
                ax11.set_ylim(bottom=0, top=Y*2)
                ax21.set_xlim(left=0, right=Y*2)
                ax21.set_ylim(bottom=-(G_+TR_)*3-100, top=Y*2)

                Y_gr2 = np.linspace(0, Y2*2, 1000)
                BS_gr2 = -(G_2+TR_2)+(t2*Y_gr2)
                
                ax12.set_title("Bilancio dello Stato (t2)", fontsize=20, family="Arial")
                ax12.set_xlim(left=0, right=Y*2)
                ax12.set_ylim(bottom=0, top=Y*2)
                ax22.set_xlim(left=0, right=Y*2)
                ax22.set_ylim(bottom=-(G_+TR_)*3-100, top=Y*2)

                #ax11 Setup
                ax11.set_xlabel("Y", fontweight="bold", loc="right")
                ax11.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
                ax11.vlines(Y, 0, Y, linestyle="--", color="gray", alpha=0.7)

                #ax21 Setup
                ax21.set_xlabel("Y", fontweight="bold", loc="right")
                ax21.set_ylabel("BS", fontweight="bold", loc="top", rotation=0)
                ax21.vlines(Y, -(G_+TR_)+(Y*t), Y*2, linestyle="--", color="gray", alpha=0.7)
                ax21.hlines(BS, 0, Y, linestyle="--", color="gray", alpha=0.7)

                #ax12 Setup
                ax12.set_xlabel("Y", fontweight="bold", loc="right")
                ax12.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
                ax12.vlines(Y2, 0, Y2, linestyle="--", color="gray", alpha=0.7)

                #ax22 Setup
                ax22.set_xlabel("Y2", fontweight="bold", loc="right")
                ax22.set_ylabel("BS2", fontweight="bold", loc="top", rotation=0)
                ax22.vlines(Y2, -(G_2+TR_2)+(Y2*t2), Y2*2, linestyle="--", color="gray", alpha=0.7)
                ax22.hlines(BS2, 0, Y2, linestyle="--", color="gray", alpha=0.7)

                #ax11 lines
                ax11.plot(Y_gr, Z_eq, color="blue")
                ax11.plot(Y_gr, Z_gr, color="blue")

                #ax21 lines
                ax21.hlines(0, 0, Y*2, color="black", linewidth=0.5)
                ax21.plot(Y_gr, BS_gr, color="blue")

                #ax12 lines
                ax12.plot(Y_gr2, Z_eq2, color="blue")
                ax12.plot(Y_gr2, Z_gr2, color="blue")
                
                #ax22 lines
                ax22.hlines(0, 0, Y2*2, color="black", linewidth=0.5)
                ax22.plot(Y_gr2, BS_gr2, color="blue")

                #ax11 Points
                ax11.plot(Y, Y, "o", color="red", markersize=2)
                ax11.annotate("E", (Y, Y), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                ax11.plot(0, Z_, "_", color="red", markersize=10)
                ax11.annotate(rf"$\overline{{Z}}={round(Z_)}$", (0, Z_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                ax11.plot(Y, 0, "|", color="red", markersize=10)
                ax11.annotate(f"Y*={round(Y)}", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                #ax21 Points
                ax21.plot(Y, -(G_+TR_)+(Y*t), "o", color="red", markersize=2)
                ax21.annotate(f"BS={round(BS)}", (0, BS), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                ax21.plot(0, -(G_+TR_), "_", color="red", markersize=10)
                ax21.annotate(rf"-($\overline{{G}}$+" + rf"$\overline{{TR}}$)={-(G_+TR_)}", (0, -(G_+TR_)), xytext=(5, -15), textcoords="offset points", fontsize=12, color="black")
                ax21.plot(0, BS, "_", color="red", markersize=10)

                #ax12 Points
                ax12.plot(Y2, Y2, "o", color="red", markersize=2)
                ax12.annotate("E", (Y2, Y2), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                ax12.plot(0, Z_2, "_", color="red", markersize=10)
                ax12.annotate(rf"$\overline{{Z2}}={round(Z_2)}$", (0, Z_2), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                ax12.plot(Y2, 0, "|", color="red", markersize=10)
                ax12.annotate(f"Y*={round(Y2)}", (Y2, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                #ax22 Points
                ax22.plot(Y2, -(G_2+TR_2)+(Y2*t2), "o", color="red", markersize=2)
                ax22.annotate(f"BS2={round(BS2)}", (0, BS2), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                ax22.plot(0, -(G_2+TR_2), "_", color="red", markersize=10)
                ax22.annotate(rf"-($\overline{{G2}}$+" + rf"$\overline{{TR2}}$)={-(G_2+TR_2)}", (0, -(G_2+TR_2)), xytext=(5, -15), textcoords="offset points", fontsize=12, color="black")
                ax22.plot(0, BS2, "_", color="red", markersize=10)

                #Bilancia commerciale_variazione
                fig, axs = plt.subplots(2, 2, num="Bilancia commerciale - confronto")

                ax11 = axs[0, 0]
                ax21 = axs[1, 0]
                ax12 = axs[0, 1]
                ax22 = axs[1, 1]

                Y_gr = np.linspace(0, Y*2, 1000)
                NX_gr = (qw*Y_w)-(q*Y_gr)

                ax11.set_title("Bilancia commerciale (t1)", fontsize=20, family="Arial")
                ax11.set_xlim(left=0, right=Y*2)
                ax11.set_ylim(bottom=0, top=Y*2)
                ax21.set_xlim(left=0, right=Y*2)
                ax21.set_ylim(bottom=NX*2-300, top=Y*2)

                Y_gr2 = np.linspace(0, Y2*2, 1000)
                NX_gr2 = (qw2*Y_w2)-(q2*Y_gr2)

                ax12.set_title("Bilancia commerciale (t2)", fontsize=20, family="Arial")
                ax12.set_xlim(left=0, right=Y*2)
                ax12.set_ylim(bottom=0, top=Y*2)
                ax22.set_xlim(left=0, right=Y*2)
                ax22.set_ylim(bottom=NX*2-300, top=Y*2)

                #ax11 Setup
                ax11.set_xlabel("Y", fontweight="bold", loc="right")
                ax11.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
                ax11.vlines(Y, 0, Y, linestyle="--", color="gray", alpha=0.7)

                #ax21 Setup
                ax21.set_xlabel("Y", fontweight="bold", loc="right")
                ax21.set_ylabel("NX", fontweight="bold", loc="top", rotation=0)
                ax21.vlines(Y, NX, Y*2, linestyle="--", color="gray", alpha=0.7)
                ax21.hlines(NX, 0, Y, linestyle="--", color="gray", alpha=0.7)

                #ax12 Setup
                ax12.set_xlabel("Y", fontweight="bold", loc="right")
                ax12.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
                ax12.vlines(Y2, 0, Y2, linestyle="--", color="gray", alpha=0.7)

                #ax22 Setup
                ax22.set_xlabel("Y", fontweight="bold", loc="right")
                ax22.set_ylabel("NX", fontweight="bold", loc="top", rotation=0)
                ax22.vlines(Y2, NX2, Y*2, linestyle="--", color="gray", alpha=0.7)
                ax22.hlines(NX2, 0, Y2, linestyle="--", color="gray", alpha=0.7)

                #ax11 lines
                ax11.plot(Y_gr, Z_eq, color="blue")
                ax11.plot(Y_gr, Z_gr, color="blue")

                #ax21 lines
                ax21.hlines(0, 0, Y*2, color="black", linewidth=0.5)
                ax21.plot(Y_gr, NX_gr, color="blue")

                #ax12 lines
                ax12.plot(Y_gr2, Z_eq2, color="blue")
                ax12.plot(Y_gr2, Z_gr2, color="blue")

                #ax22 lines
                ax22.hlines(0, 0, Y2*2, color="black", linewidth=0.5)
                ax22.plot(Y_gr2, NX_gr2, color="blue")

                #ax11 Points
                ax11.plot(Y, Y, "o", color="red", markersize=2)
                ax11.annotate("E", (Y, Y), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                ax11.plot(0, Z_, "_", color="red", markersize=10)
                ax11.annotate(rf"$\overline{{Z}}={round(Z_)}$", (0, Z_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                ax11.plot(Y, 0, "|", color="red", markersize=10)
                ax11.annotate(f"Y*={round(Y)}", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                #ax21 Points
                ax21.plot(Y, NX, "o", color="red", markersize=2)
                ax21.annotate(f"NX={round(NX)}", (Y, NX), xytext=(10, -15), textcoords="offset points", fontsize=12, color="black")
                ax21.plot(0, NX, "_", color="red", markersize=10)
                ax21.plot(0, qw*Y_w, "_", color="red", markersize=10)
                ax21.annotate(rf"qw$\overline{{Y}}$w", (0, qw*Y_w), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                #ax12 Points
                ax12.plot(Y2, Y2, "o", color="red", markersize=2)
                ax12.annotate("E", (Y2, Y2), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                ax12.plot(0, Z_2, "_", color="red", markersize=10)
                ax12.annotate(rf"$\overline{{Z2}}={round(Z_2)}$", (0, Z_2), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                ax12.plot(Y2, 0, "|", color="red", markersize=10)
                ax12.annotate(f"Y2*={round(Y2)}", (Y2, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                #ax22 Points
                ax22.plot(Y2, NX2, "o", color="red", markersize=2)
                ax22.annotate(f"NX2={round(NX2)}", (Y2, NX2), xytext=(10, -15), textcoords="offset points", fontsize=12, color="black")
                ax22.plot(0, NX2, "_", color="red", markersize=10)
                ax22.plot(0, qw2*Y_w2, "_", color="red", markersize=10)
                ax22.annotate(rf"qw2$\overline{{Y}}$w2", (0, qw2*Y_w2), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")


                print(colorama.Fore.RED + "CHIUDERE TUTTI I GRAFICI PER POTER CONTINUARE.") 
                plt.show()

            if Variazione.lower() == "n":     
                riavvia_programma()

else:
    #Economia chiusa senza settore pubblico
    if SP.lower() == "n":   
        #inputs
        C_ = value("A quanto ammontano i consumi fissi? ")
        I_ = value("A quanto ammontano gli investimenti delle imprese? ")
        c = parameter("A quanto ammonta la propensione al consumo delle famiglie (inserire un valore tra 0 e 1)? ")

        #Equations
        Z_ = C_+I_
        z = 1/(1-c)
        Y = z*Z_
        Yd = Y
        C = C_+c*Yd
        Sn = Yd-C

        #disoccupazione
        if Occ.lower() == "s":
            η = value("A quanto ammonta la produttività del lavoro? ")
            N_ = value("A quanto ammonta la popolazione attiva (offerta di lavoro)? ")
            N = Y/η
            U = N_-N
            u = U/N_
            Y_ = η*N_
        else:
            pass    

        #space
        print("---")
        print("")

        #Macro values
        print(f"La domanda autonoma ammonta a: {round(Z_,2)}")
        print(f"Il moltiplicatore keynesiano è: {round(z,2)}")
        print(f"Il PIL ammonta a: {round(Y,2)}")
        print(f"I consumi ammontano a: {round(C,2)}")
        if Sn > 0:
            print(f"Il risparmio delle famiglie ammonta a: {round(Sn,2)}")
        elif Sn == 0:
            print(f"Le famiglie consumano tutto il reddito a loro disposizione")
        elif Sn < 0:
            print(f"Le famiglie si indebitano per un ammontare pari a: {abs(round(Sn,2))}")
        if Occ.lower() == "s":
            print(f"La domanda di lavoro ammonta a {round(N,2)}")
            if U > 0:
                print(f"il numero di disoccupati ammonta a {round(U,2)}")
                print(f"la disoccupazione è al {round(u*100, 2)}%")
                print(f"Il reddito di pieno impiego sarebbe {round(Y_,2)}")
            elif U == 0:
                print(f"Non c'è disoccupazione")
            elif U < 0:
                print(f"C'è piena occupazione con un eccesso di domanda di lavoro di {abs(round(U,2))}")
        else:
            pass

        #Graphics
        #Mercato dei beni
        Y_gr = np.linspace(0, Y*2, 1000)
        Z_eq = Y_gr
        Z_gr = Z_+c*Y_gr
        #Con disoccupazione
        if Occ.lower() == "s":
            N_gr = (1/η)*Y_gr

            fig, (ax1, ax2) = plt.subplots(2, 1, num="Mercato dei beni e occupazione")
            ax1.set_xlim(left=0, right=Y*2)
            ax1.set_ylim(bottom=0, top=Y*2)
            ax2.set_xlim(left=0, right=Y*2)
            ax2.set_ylim(bottom=0, top=Y*2)
            ax1.set_title("Mercato dei beni", fontsize=20, family="Arial")

            #ax1 Setup
            ax1.set_xlabel("Y", fontweight="bold", loc="right")
            ax1.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
            ax1.vlines(Y, 0, Y, linestyle="--", color="gray", alpha=0.7)

            #ax1 lines
            ax1.plot(Y_gr, Z_eq, color="blue")
            ax1.plot(Y_gr, Z_gr, color="blue")

            #ax1 Points
            ax1.plot(Y, Y, "o", color="red", markersize=2)
            ax1.annotate("E", (Y, Y), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
            ax1.plot(0, Z_, "_", color="red", markersize=10)
            ax1.annotate(rf"$\overline{{Z}}={round(Z_)}$", (0, Z_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
            ax1.plot(Y, 0, "|", color="red", markersize=10)
            ax1.annotate(f"Y*={round(Y)}", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

            #ax2 Setup
            ax2.set_xlabel("Y", fontweight="bold", loc="right")
            ax2.set_ylabel("N", fontweight="bold", loc="top", rotation=0)
            ax2.vlines(Y, 0, Y*2, linestyle="--", color="gray", alpha=0.7)
            ax2.hlines(N, 0, Y, linestyle="--", color="gray", alpha=0.7)
            ax2.vlines(Y_, 0, N_, linestyle="--", color="gray", alpha=0.7)
            ax2.hlines(N_, 0, Y_, linestyle="--", color="gray", alpha=0.7)
            #ax2 lines
            ax2.plot(Y_gr, N_gr, color="blue")
            #ax2 Points
            ax2.plot(Y, N, "o", color="red", markersize=2)
            ax2.plot(0, N, "_", color="red", markersize=10)
            ax2.plot(Y_, N_, "o", color="red", markersize=2)
            ax2.annotate(f"N*={round(N)}", (0, N), xytext=(55, 5), textcoords="offset points", fontsize=12, color="black")
            ax2.plot(0, N_, "_", color="red", markersize=10)
            ax2.annotate(rf"$\overline{{N}}={round(N_)}$", (0, N_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
            if Y_ > Y:
                ax2.plot(Y_, 0, "|", color="red", markersize=10)
                ax2.annotate(rf"$\overline{{Y}}={round(Y_)}$", (Y_, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
            else:
                ax2.plot(Y_, 0, "|", color="red", markersize=10)
                ax2.annotate(r"$\overline{Y}$", (Y_, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
            ax2.plot(Y, 0, "|", color="red", markersize=10)
            ax2.annotate("Y*", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

            pass

        #Senza disoccupazione
        if Occ.lower() == "n":
            plt.figure(num="Mercato dei beni")
            plt.xlim(left=0, right=Y*2)
            plt.ylim(bottom=0, top=Y*2)
            plt.title("Mercato dei beni", fontsize=20, family="Arial")

            #Setup
            plt.xlabel("Y", fontweight="bold", loc="right")
            plt.ylabel("Z", fontweight="bold", loc="top")
            plt.vlines(Y, 0, Y, linestyle="--", color="gray", alpha=0.7)
            plt.hlines(Y, 0, Y, linestyle="--", color="gray", alpha=0.7)

            #Lines
            plt.plot(Y_gr, Z_eq, color="blue")
            plt.plot(Y_gr, Z_gr, color="blue")

            #Points
            plt.plot(Y, Y, "o", color="red", markersize=2)
            plt.annotate("E", (Y, Y), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
            plt.plot(0, Z_, "_", color="red", markersize=10)
            plt.annotate(rf"$\overline{{Z}}={round(Z_)}$", (0, Z_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
            plt.plot(Y, 0, "|", color="red", markersize=10)
            plt.annotate(f"Y*={round(Y)}", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

            pass

        #Risparmio delle famiglie
        plt.figure(num="Risparmio e investimenti")
        Y_gr = np.linspace(0, Y*2, 1000)
        SI_gr = -C_+(1-c)*Y_gr

        plt.xlim(left=0, right=Y*2)
        plt.ylim(bottom=-C_*2-100, top=Y)
        plt.hlines(0, 0, Y*2, color="black", linewidth=0.5)
        plt.title("Risparmio e investimenti", fontsize=20, family="Arial")

        #Setup
        plt.xlabel("Y", fontweight="bold", loc="right")
        plt.ylabel("S, I", fontweight="bold", loc="top")
        plt.vlines(Y, 0, I_, linestyle="--", color="gray", alpha=0.7)

        #Lines
        plt.plot(Y_gr, SI_gr, color="blue")
        plt.hlines(I_, 0, Y*2, color="blue")

        #Points
        plt.plot(Y, I_, "o", color="red", markersize=2)
        plt.annotate("E", (Y, I_), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
        plt.plot(0, I_, "_", color="red", markersize=10)
        plt.annotate(rf"$\overline{{I}}={round(I_)}$", (0, I_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
        plt.plot(Y, 0, "|", color="red", markersize=10)
        plt.annotate(f"Y*={round(Y)}", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
        plt.plot(0, -C_, "_", color="red", markersize=10)
        plt.annotate(rf"-$\overline{{C}}={round(-C_)}$", (0, -C_), xytext=(2, -15), textcoords="offset points", fontsize=12, color="black")

        print(colorama.Fore.RED + "CHIUDERE TUTTI I GRAFICI PER POTER CONTINUARE.") 
        plt.show()

        #Variazioni
        while True:
            Variazione = str(input("Desideri variare una o più variabili per un confronto (S/N)? "))
            if Variazione.lower() == "s" or Variazione.lower() == "n":
                pass
            else:
                print(colorama.Fore.RED + f"{Variazione} non è valido, indicare S o N.")
                
            if Variazione.lower() == "s":
                while True:
                    VarC = str(input("desideri variare i consumi fissi? (S/N): "))
                    if VarC.lower() == "s" or VarC.lower() == "n":
                        break
                    else:
                        print(colorama.Fore.RED + f"{VarC} non è valido, indicare S o N.")
                if VarC.lower() == "s":
                    C_2 = value("A quanto ammontano i NUOVI consumi fissi? ")
                elif VarC.lower() == "n":
                    C_2 = C_
                else:
                    pass

                while True:
                    VarI = str(input("desideri variare gli investimenti? (S/N): "))
                    if VarI.lower() == "s" or VarI.lower() == "n":
                        break
                    else:
                        print(colorama.Fore.RED + f"{VarI} non è valido, indicare S o N.")
                if VarI.lower() == "s":
                    I_2 = value("A quanto ammontano i NUOVI investimenti? ")
                elif VarI.lower() == "n":
                    I_2 = I_
                else:
                    pass
                
                while True:
                    Varc = str(input("desideri variare la propensione al consumo delle famiglie? (S/N): "))
                    if Varc.lower() == "s" or Varc.lower() == "n":
                        break
                    else:
                        print(colorama.Fore.RED + f"{Varc} non è valido, indicare S o N.")
                if Varc.lower() == "s":
                    c2 = parameter("A quanto ammonta la NUOVA propensione al consumo (inserire un valore tra 0 e 1)? ")
                elif Varc.lower() == "n":
                    c2 = c
                else:
                    pass

                if Occ.lower() == "s":
                    while True:
                        Varη = str(input("desideri variare la produttività dei lavoratori? (S/N): "))
                        if Varη.lower() == "s" or Varη.lower() == "n":
                            break
                        else:
                            print(colorama.Fore.RED + f"{Varη} non è valido, indicare S o N.")
                    if Varη.lower() == "s":
                        η2 = value("A quanto ammonta la NUOVA produttività dei lavoratori? ")
                    elif Varη.lower() == "n":
                        η2 = η
                    else:
                        pass

                    while True:
                        VarN_ = str(input("desideri variare l'offerta di lavoro? (S/N): "))
                        if VarN_.lower() == "s" or VarN_.lower() == "n":
                            break
                        else:
                            print(colorama.Fore.RED + f"{VarN_} non è valido, indicare S o N.")
                    if VarN_.lower() == "s":
                        N_2 = value("A quanto ammonta la NUOVA offerta di lavoro? ")
                    elif VarN_.lower() == "n":
                        N_2 = N_
                    else:
                        pass
    

                #Equations
                Z_2 = C_2+I_2
                z2 = 1/(1-c2)
                Y2 = z2*Z_2
                Yd2 = Y2
                C2 = C_2+c2*Yd2
                Sn2 = Yd2-C2
                if Occ.lower() == "s":
                    N2 = Y2/η2
                    U2 = N_2-N2
                    u2 = U2/N_2

                #Macro values (variazioni)
                if Z_2 > Z_:
                    print(f"Ora la domanda autonoma ammonta a: {round(Z_2,2)}" + f" {Fore.GREEN}(+{round(Z_2-Z_, 2)})")
                elif Z_2 == Z_:
                    print(f"La domanda autonoma è rimasta invariata: {round(Z_2,2)}")
                elif Z_2 < Z_:
                    print(f"Ora la domanda autonoma ammonta a: {round(Z_2,2)}" + f" {Fore.RED}({round(Z_2-Z_, 2)})")

                if z2 > z:
                    print(f"Ora il moltiplicatore keynesiano è: {round(z2,2)}" + f" {Fore.GREEN}(+{round(z2-z, 2)})")
                elif z2 == z:
                    print(f"Il moltiplicatore keynesiano è rimasto invariato: {round(z2,2)}")
                elif z2 < z:
                    print(f"Ora il moltiplicatore keynesiano è: {round(z2,2)}" + f" {Fore.RED}({round(z2-z, 2)})")

                if Y2 > Y:
                    print(f"Ora il PIL ammonta a: {round(Y2,2)}" + f" {Fore.GREEN}(+{round(Y2-Y, 2)})")
                elif Y2 == Y:
                    print(f"Il PIL è rimasto invariato: {round(Y2,2)}")
                elif Y2 < Y:
                    print(f"Ora il PIL ammonta a: {round(Y2,2)}" + f" {Fore.RED}({round(Y2-Y, 2)})")

                if C2 > C:
                    print(f"Ora i consumi ammontano a: {round(C2,2)}" + f" {Fore.GREEN}(+{round(C2-C, 2)})")
                elif C2 == C:
                    print(f"I consumi sono rimasti invariati: {round(C2,2)}")
                elif C2 < C:
                    print(f"Ora i consumi ammontano a: {round(C2,2)}" + f" {Fore.RED}({round(C2-C, 2)})")

                if Sn2 > Sn:
                    print(f"Ora i risparmi delle famiglie ammontano a: {round(Sn2,2)}" + f" {Fore.GREEN}(+{round(Sn2-Sn, 2)})")
                elif Sn2 == Sn:
                    print(f"I risparmi delle famiglie sono rimasti invariati: {round(Sn2,2)}")
                elif Sn2 < Sn:
                    print(f"Ora i risparmi delle famiglie ammontano a: {round(Sn2,2)}" + f" {Fore.RED}({round(Sn2-Sn, 2)})")
                if Sn2 > 0:
                    print(f"Il risparmio delle famiglie ammonta a: {round(Sn2,2)}")
                elif Sn2 == 0:
                    print(f"Le famiglie consumano tutto il reddito a loro disposizione")
                elif Sn2 < 0:
                    print(f"Le famiglie si indebitano per un ammontare pari a: {abs(round(Sn2,2))}")

                if Occ.lower() == "s":
                    if N2 > N:
                        print(f"Ora la domanda di lavoro ammonta a: {round(N2,2)}" + f" {Fore.GREEN}(+{round(N2-N, 2)})")
                    elif N2 == N:
                        print(f"La domanda di lavoro è rimasta invariata: {round(N2,2)}")
                    elif N2 < N:
                        print(f"Ora la domanda di lavoro ammonta a: {round(N2,2)}" + f" {Fore.RED}({round(N2-N, 2)})")

                    if U2 > U:
                        print(f"Ora la disoccupazione ammonta a: {round(U2,2)}" + f" {Fore.RED}(+{round(U2-U, 2)})")
                    elif U2 == U:
                        print(f"La disoccupazione è rimasta invariata: {round(U2,2)}")
                    elif U2 < U:
                        print(f"Ora la disoccupazione ammonta a: {round(U2,2)}" + f" {Fore.GREEN}({round(U2-U, 2)})")
                    if U2 > 0:
                        print(f"il numero di disoccupati ammonta a {round(U2,2)}")
                        print(f"la disoccupazione è al {round(u2*100, 2)}%")
                        print(f"Il reddito di pieno impiego sarebbe {round(η2*N_2,2)}")
                    elif U2 == 0:
                        print(f"Non c'è disoccupazione")
                    elif U2 < 0:
                        print(f"C'è piena occupazione con un eccesso di domanda di lavoro di {abs(round(U2,2))}")
                

                #Graph_Variations
                #Mercato dei beni con occupazione_Variazione
                if Occ.lower() == "s":
                    fig, axs = plt.subplots(2, 2, num="Mercato dei beni e occupazione - confronto")

                    ax11 = axs[0, 0]
                    ax21 = axs[1, 0]
                    ax12 = axs[0, 1]
                    ax22 = axs[1, 1]

                    Y_gr = np.linspace(0, Y*2, 1000)
                    Z_eq = Y_gr
                    Z_gr = Z_+c*Y_gr

                    N_gr = (1/η)*Y_gr

                    ax11.set_title("Mercato dei beni (t1)", fontsize=20, family="Arial")
                    ax11.set_xlim(left=0, right=Y*2)
                    ax11.set_ylim(bottom=0, top=Y*2)
                    ax21.set_xlim(left=0, right=Y*2)
                    ax21.set_ylim(bottom=0, top=Y*2)

                    Y_gr2 = np.linspace(0, Y2*2, 1000)
                    Z_eq2 = Y_gr2
                    Z_gr2 = Z_2+c2*Y_gr2
                    N_gr2 = (1/η2)*Y_gr2
                    
                    ax12.set_title("Mercato dei beni (t2)", fontsize=20, family="Arial")
                    ax12.set_xlim(left=0, right=Y*2)
                    ax12.set_ylim(bottom=0, top=Y*2)
                    ax22.set_xlim(left=0, right=Y*2)
                    ax22.set_ylim(bottom=0, top=Y*2)

                    #ax11 Setup
                    ax11.set_xlabel("Y", fontweight="bold", loc="right")
                    ax11.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
                    ax11.vlines(Y, 0, Y, linestyle="--", color="gray", alpha=0.7)

                    #ax21 Setup
                    ax21.set_xlabel("Y", fontweight="bold", loc="right")
                    ax21.set_ylabel("N", fontweight="bold", loc="top", rotation=0)
                    ax21.vlines(Y, 0, Y*2, linestyle="--", color="gray", alpha=0.7)
                    ax21.hlines(N, 0, Y, linestyle="--", color="gray", alpha=0.7)
                    ax21.vlines(Y_, 0, N_, linestyle="--", color="gray", alpha=0.7)
                    ax21.hlines(N_, 0, Y_, linestyle="--", color="gray", alpha=0.7)

                    #ax12 Setup
                    ax12.set_xlabel("Y", fontweight="bold", loc="right")
                    ax12.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
                    ax12.vlines(Y2, 0, Y2, linestyle="--", color="gray", alpha=0.7)

                    #ax22 Setup
                    ax22.set_xlabel("Y", fontweight="bold", loc="right")
                    ax22.set_ylabel("N", fontweight="bold", loc="top", rotation=0)
                    ax22.vlines(Y2, 0, Y2*2, linestyle="--", color="gray", alpha=0.7)
                    ax22.hlines(N2, 0, Y2, linestyle="--", color="gray", alpha=0.7)
                    ax22.vlines(η2*N_2, 0, N_2, linestyle="--", color="gray", alpha=0.7)
                    ax22.hlines(N_2, 0, η2*N_2, linestyle="--", color="gray", alpha=0.7)

                    #ax11 lines
                    ax11.plot(Y_gr, Z_eq, color="blue")
                    ax11.plot(Y_gr, Z_gr, color="blue")

                    #ax21 lines
                    ax21.plot(Y_gr, N_gr, color="blue")

                    #ax12 lines
                    ax12.plot(Y_gr2, Z_eq2, color="blue")
                    ax12.plot(Y_gr2, Z_gr2, color="blue")
                    
                    #ax22 lines
                    ax22.plot(Y_gr2, N_gr2, color="blue")

                    #ax11 Points
                    ax11.plot(Y, Y, "o", color="red", markersize=2)
                    ax11.annotate("E", (Y, Y), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                    ax11.plot(0, Z_, "_", color="red", markersize=10)
                    ax11.annotate(rf"$\overline{{Z}}={round(Z_)}$", (0, Z_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax11.plot(Y, 0, "|", color="red", markersize=10)
                    ax11.annotate(f"Y*={round(Y)}", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                    #ax21 Points
                    ax21.plot(Y, N, "o", color="red", markersize=2)
                    ax21.plot(0, N, "_", color="red", markersize=10)
                    ax21.plot(Y_, N_, "o", color="red", markersize=2)
                    ax21.annotate(f"N*={round(N)}", (0, N), xytext=(55, 5), textcoords="offset points", fontsize=12, color="black")
                    ax21.plot(0, N_, "_", color="red", markersize=10)
                    ax21.annotate(rf"$\overline{{N}}={round(N_)}$", (0, N_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax21.plot(Y, 0, "|", color="red", markersize=10)
                    ax21.annotate("Y*", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax21.plot(Y_, 0, "|", color="red", markersize=10)
                    ax21.annotate(rf"$\overline{{Y}}={round(Y_)}$", (Y_, 0), xytext=(2, -35), textcoords="offset points", fontsize=12, color="black")

                    #ax12 Points
                    ax12.plot(Y2, Y2, "o", color="red", markersize=2)
                    ax12.annotate("E", (Y2, Y2), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                    ax12.plot(0, Z_2, "_", color="red", markersize=10)
                    ax12.annotate(rf"$\overline{{Z2}}={round(Z_2)}$", (0, Z_2), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax12.plot(Y2, 0, "|", color="red", markersize=10)
                    ax12.annotate(f"Y*={round(Y2)}", (Y2, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                    #ax22 Points
                    ax22.plot(Y2, N2, "o", color="red", markersize=2)
                    ax22.plot(0, N2, "_", color="red", markersize=10)
                    ax22.plot(η2*N_2, N_2, "o", color="red", markersize=2)
                    ax22.annotate(f"N2*={round(N2)}", (0, N2), xytext=(55, 5), textcoords="offset points", fontsize=12, color="black")
                    ax22.plot(0, N_2, "_", color="red", markersize=10)
                    ax22.annotate(rf"$\overline{{N2}}={round(N_2)}$", (0, N_2), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax22.plot(Y2, 0, "|", color="red", markersize=10)
                    ax22.annotate("Y2*", (Y2, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax22.plot(η2*N_2, 0, "|", color="red", markersize=10)
                    ax22.annotate(rf"$\overline{{Y2}}={round(η2*N_2)}$", (η2*N_2, 0), xytext=(2, -35), textcoords="offset points", fontsize=12, color="black")

                    pass

                #Mercato dei beni senza occupazione_Variazione
                if Occ.lower() == "n":
                    fig, axs = plt.subplots(1, 2, num="Mercato dei beni - confronto")

                    ax11 = axs[0]
                    ax12 = axs[1]

                    Y_gr = np.linspace(0, Y*2, 1000)
                    Z_eq = Y_gr
                    Z_gr = Z_+c*Y_gr

                    Y_gr2 = np.linspace(0, Y2*2, 1000)
                    Z_eq2 = Y_gr2
                    Z_gr2 = Z_2+c2*Y_gr2

                    ax11.set_title("Mercato dei beni(t1)", fontsize=20, family="Arial")
                    ax11.set_xlim(left=0, right=Y*2)
                    ax11.set_ylim(bottom=0, top=Y*2)

                    ax12.set_title("Mercato dei beni(t2)", fontsize=20, family="Arial")
                    ax12.set_xlim(left=0, right=Y*2)
                    ax12.set_ylim(bottom=0, top=Y*2)

                    #ax11 Setup
                    ax11.set_xlabel("Y", fontweight="bold", loc="right")
                    ax11.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
                    ax11.vlines(Y, 0, Y, linestyle="--", color="gray", alpha=0.7)

                    #ax12 Setup
                    ax12.set_xlabel("Y", fontweight="bold", loc="right")
                    ax12.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
                    ax12.vlines(Y2, 0, Y2, linestyle="--", color="gray", alpha=0.7)

                    #ax11 lines
                    ax11.plot(Y_gr, Z_eq, color="blue")
                    ax11.plot(Y_gr, Z_gr, color="blue")

                    #ax12 lines
                    ax12.plot(Y_gr2, Z_eq2, color="blue")
                    ax12.plot(Y_gr2, Z_gr2, color="blue")

                    #ax11 Points
                    ax11.plot(Y, Y, "o", color="red", markersize=2)
                    ax11.annotate("E", (Y, Y), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                    ax11.plot(0, Z_, "_", color="red", markersize=10)
                    ax11.annotate(rf"$\overline{{Z}}={round(Z_)}$", (0, Z_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax11.plot(Y, 0, "|", color="red", markersize=10)
                    ax11.annotate(f"Y*={round(Y)}", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                    #ax12 Points
                    ax12.plot(Y2, Y2, "o", color="red", markersize=2)
                    ax12.annotate("E", (Y2, Y2), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                    ax12.plot(0, Z_2, "_", color="red", markersize=10)
                    ax12.annotate(rf"$\overline{{Z2}}={round(Z_2)}$", (0, Z_2), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax12.plot(Y2, 0, "|", color="red", markersize=10)
                    ax12.annotate(f"Y*={round(Y2)}", (Y2, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                    pass

                #Risparmio delle famiglie_Variazione
                fig, axs = plt.subplots(1, 2, num="Risparmio e investimenti")

                ax11 = axs[0]
                ax12 = axs[1]

                Y_gr = np.linspace(0, Y*2, 1000)
                SI_gr = -C_+(1-c)*Y_gr

                Y_gr2 = np.linspace(0, Y2*2, 1000)
                SI_gr2 = -C_2+(1-c2)*Y_gr2

                ax11.set_title("Risparmio e investimenti (t1)", fontsize=20, family="Arial")
                ax11.set_xlim(left=0, right=Y*2) 
                ax11.set_ylim(bottom=-C_*2-100, top=Y)

                ax12.set_title("Risparmio e investimenti (t2)", fontsize=20, family="Arial")
                ax12.set_xlim(left=0, right=Y*2) 
                ax12.set_ylim(bottom=-C_*2-100, top=Y)

                ax11.hlines(0, 0, Y*2, color="black", linewidth=0.5)
                ax12.hlines(0, 0, Y2*2, color="black", linewidth=0.5)

                #ax11 Setup
                ax11.set_xlabel("Y", fontweight="bold", loc="right")
                ax11.set_ylabel("S, I", fontweight="bold", loc="top")
                ax11.vlines(Y, 0, I_, linestyle="--", color="gray", alpha=0.7)

                #ax12 Setup
                ax12.set_xlabel("Y", fontweight="bold", loc="right")
                ax12.set_ylabel("S, I", fontweight="bold", loc="top")
                ax12.vlines(Y2, 0, I_2, linestyle="--", color="gray", alpha=0.7)

                #ax11 lines
                ax11.plot(Y_gr, SI_gr, color="blue")
                ax11.hlines(I_, 0, Y*2, color="blue")

                #ax12 lines
                ax12.plot(Y_gr2, SI_gr2, color="blue")
                ax12.hlines(I_2, 0, Y2*2, color="blue")

                #ax11 Points
                ax11.plot(Y, I_, "o", color="red", markersize=2)
                ax11.annotate("E", (Y, I_), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                ax11.plot(0, I_, "_", color="red", markersize=10)
                ax11.annotate(rf"$\overline{{I}}={round(I_)}$", (0, I_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                ax11.plot(Y, 0, "|", color="red", markersize=10)
                ax11.annotate(f"Y*={round(Y)}", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                ax11.plot(0, -C_, "_", color="red", markersize=10)
                ax11.annotate(rf"-$\overline{{C}}={round(-C_)}$", (0, -C_), xytext=(2, -15), textcoords="offset points", fontsize=12, color="black")
                #ax12 Points
                ax12.plot(Y2, I_2, "o", color="red", markersize=2)
                ax12.annotate("E", (Y2, I_2), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                ax12.plot(0, I_2, "_", color="red", markersize=10)
                ax12.annotate(rf"$\overline{{I2}}={round(I_2)}$", (0, I_2), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                ax12.plot(Y, 0, "|", color="red", markersize=10)
                ax12.annotate(f"Y*={round(Y2)}", (Y2, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                ax12.plot(0, -C_2, "_", color="red", markersize=10)
                ax12.annotate(rf"-$\overline{{C2}}={round(-C_2)}$", (0, -C_2), xytext=(2, -15), textcoords="offset points", fontsize=12, color="black")

                print(colorama.Fore.RED + "CHIUDERE TUTTI I GRAFICI PER POTER CONTINUARE.") 
                plt.show()

            if Variazione.lower() == "n":     
                riavvia_programma()
     
    else:
        pass  



    #Economia chiusa con settore pubblico
    #Tasse esogene
    if SP.lower() == "s" and Tasse.lower() == "es":
        while True:
                
            #inputs
            C_ = value("A quanto ammontano i consumi fissi? ")
            I_ = value("A quanto ammontano gli investimenti delle imprese? ")
            c = parameter("A quanto ammonta la propensione al consumo delle famiglie (inserire un valore tra 0 e 1)? ")
            G_ = value("A quanto ammonta la spesa pubblica? ")
            TA_ = value("A quanto ammontano le tasse? ")
            TR_ = value("A quanto ammontano i trasferimenti pubblici alle famiglie? ")

            #Equations
            Z_ = C_+I_+G_+c*TR_-c*TA_
            z = 1/(1-c)
            Y = z*Z_
            Yd = Y+TR_-TA_
            C = C_+c*Yd
            Sn = Yd-C
            BS = TA_-(TR_+G_)

            #disoccupazione
            if Occ.lower() == "s":
                η = value("A quanto ammonta la produttività del lavoro? ")
                N_ = value("A quanto ammonta la popolazione attiva (offerta di lavoro)? ")
                N = Y/η
                U = N_-N
                u = U/N_
                Y_ = η*N_
            else:
                pass    

            #space
            print("---")
            print("")

            #Macro values
            print(f"La domanda autonoma ammonta a: {round(Z_,2)}")
            print(f"Il moltiplicatore keynesiano è: {round(z,2)}")
            print(f"Il PIL ammonta a: {round(Y,2)}")
            print(f"Il reddito disponibile ammonta a: {round(Yd,2)}")
            print(f"I consumi ammontano a: {round(C,2)}")
            if Sn > 0:
                print(f"Il risparmio delle famiglie ammonta a: {round(Sn,2)}")
            elif Sn == 0:
                print(f"Le famiglie consumano tutto il reddito a loro disposizione")
            elif Sn < 0:
                print(f"Le famiglie si indebitano per un ammontare pari a: {abs(round(Sn))}")
            if Occ.lower() == "s":
                print(f"La domanda di lavoro ammonta a {round(N,2)}")
                if U > 0:
                    print(f"il numero di disoccupati ammonta a {round(U,2)}")
                    print(f"la disoccupazione è al {round(u*100, 2)}%")
                    print(f"Il reddito di pieno impiego sarebbe {round(Y_,2)}")
                elif U == 0:
                    print(f"Non c'è disoccupazione")
                elif U < 0:
                    print(f"C'è piena occupazione con un eccesso di domanda di lavoro di {abs(round(U,2))}")
            else:
                pass
                
            #Analysis:
            #Bilancio dello Stato
            if BS == 0:
                print("Il bilancio dello Stato è in equilibrio")
            elif BS > 0:
                print(f"Il bilancio dello Stato è in surplus finanziario di {round(BS,2)}")
            elif BS < 0:
                print(f"Il bilancio dello Stato è in deficit finanziario di {abs(round(BS,2))}")
            
            #Graphics
            #Mercato dei beni
            Y_gr = np.linspace(0, Y*2, 1000)
            Z_eq = Y_gr
            Z_gr = Z_+c*Y_gr
            #Con disoccupazione
            if Occ.lower() == "s":
                N_gr = (1/η)*Y_gr

                fig, (ax1, ax2) = plt.subplots(2, 1, num="Mercato dei beni e occupazione")
                ax1.set_xlim(left=0, right=Y*2)
                ax1.set_ylim(bottom=0, top=Y*2)
                ax2.set_xlim(left=0, right=Y*2)
                ax2.set_ylim(bottom=0, top=Y*2)
                ax1.set_title("Mercato dei beni", fontsize=20, family="Arial")

                #ax1 Setup
                ax1.set_xlabel("Y", fontweight="bold", loc="right")
                ax1.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
                ax1.vlines(Y, 0, Y, linestyle="--", color="gray", alpha=0.7)

                #ax1 lines
                ax1.plot(Y_gr, Z_eq, color="blue")
                ax1.plot(Y_gr, Z_gr, color="blue")

                #ax1 Points
                ax1.plot(Y, Y, "o", color="red", markersize=2)
                ax1.annotate("E", (Y, Y), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                ax1.plot(0, Z_, "_", color="red", markersize=10)
                ax1.annotate(rf"$\overline{{Z}}={round(Z_)}$", (0, Z_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                ax1.plot(Y, 0, "|", color="red", markersize=10)
                ax1.annotate(f"Y*={round(Y)}", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                #ax2 Setup
                ax2.set_xlabel("Y", fontweight="bold", loc="right")
                ax2.set_ylabel("N", fontweight="bold", loc="top", rotation=0)
                ax2.vlines(Y, 0, Y*2, linestyle="--", color="gray", alpha=0.7)
                ax2.hlines(N, 0, Y, linestyle="--", color="gray", alpha=0.7)
                ax2.vlines(Y_, 0, N_, linestyle="--", color="gray", alpha=0.7)
                ax2.hlines(N_, 0, Y_, linestyle="--", color="gray", alpha=0.7)
                #ax2 lines
                ax2.plot(Y_gr, N_gr, color="blue")
                #ax2 Points
                ax2.plot(Y, N, "o", color="red", markersize=2)
                ax2.plot(0, N, "_", color="red", markersize=10)
                ax2.plot(Y_, N_, "o", color="red", markersize=2)
                ax2.annotate(f"N*={round(N)}", (0, N), xytext=(55, 5), textcoords="offset points", fontsize=12, color="black")
                ax2.plot(0, N_, "_", color="red", markersize=10)
                ax2.annotate(rf"$\overline{{N}}={round(N_)}$", (0, N_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                if Y_ > Y:
                    ax2.plot(Y_, 0, "|", color="red", markersize=10)
                    ax2.annotate(rf"$\overline{{Y}}={round(Y_)}$", (Y_, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                else:
                    ax2.plot(Y_, 0, "|", color="red", markersize=10)
                    ax2.annotate(r"$\overline{Y}$", (Y_, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                ax2.plot(Y, 0, "|", color="red", markersize=10)
                ax2.annotate("Y*", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                pass

            #Senza disoccupazione
            if Occ.lower() == "n":
                plt.figure(num="Mercato dei beni")
                plt.xlim(left=0, right=Y*2)
                plt.ylim(bottom=0, top=Y*2)
                plt.title("Mercato dei beni", fontsize=20, family="Arial")

                #Setup
                plt.xlabel("Y", fontweight="bold", loc="right")
                plt.ylabel("Z", fontweight="bold", loc="top")
                plt.vlines(Y, 0, Y, linestyle="--", color="gray", alpha=0.7)

                #Lines
                plt.plot(Y_gr, Z_eq, color="blue")
                plt.plot(Y_gr, Z_gr, color="blue")

                #Points
                plt.plot(Y, Y, "o", color="red", markersize=2)
                plt.annotate("E", (Y, Y), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                plt.plot(0, Z_, "_", color="red", markersize=10)
                plt.annotate(rf"$\overline{{Z}}={round(Z_)}$", (0, Z_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                plt.plot(Y, 0, "|", color="red", markersize=10)
                plt.annotate(f"Y*={round(Y)}", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                pass

            #Risparmio delle famiglie
            plt.figure(num="Risparmio e investimenti")
            Yd_gr = np.linspace(0, Yd*2, 1000)
            SI_gr = -C_+(1-c)*Yd_gr

            plt.xlim(left=0, right=Yd*2)
            plt.ylim(bottom=-C_*2-100, top=Yd)
            plt.hlines(0, 0, Yd*2, color="black", linewidth=0.5)
            plt.title("Risparmio e investimenti", fontsize=20, family="Arial")

            #Setup
            plt.xlabel("Yd", fontweight="bold", loc="right")
            plt.ylabel("Sn", fontweight="bold", loc="top")
            plt.vlines(Yd, 0, Sn, linestyle="--", color="gray", alpha=0.7)

            #Lines
            plt.plot(Yd_gr, SI_gr, color="blue")
            plt.hlines(Sn, 0, Yd*2, color="blue")

            #Points
            plt.plot(Yd, Sn, "o", color="red", markersize=2)
            plt.annotate("E", (Yd, Sn), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
            plt.plot(0, Sn, "_", color="red", markersize=10)
            plt.annotate(f"Sn*={round(Sn)}", (0, Sn), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
            plt.plot(Yd, 0, "|", color="red", markersize=10)
            plt.annotate(f"Yd*={round(Yd)}", (Yd, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
            plt.plot(0, -C_, "_", color="red", markersize=10)
            plt.annotate(rf"-$\overline{{C}}={round(-C_)}$", (0, -C_), xytext=(2, -15), textcoords="offset points", fontsize=12, color="black")

            print(colorama.Fore.RED + "CHIUDERE TUTTI I GRAFICI PER POTER CONTINUARE.") 
            plt.show()

            #Variazioni
            while True:
                Variazione = str(input("Desideri variare una o più variabili per un confronto (S/N)? "))
                if Variazione.lower() == "s" or Variazione.lower() == "n":
                    pass
                else:
                    print(colorama.Fore.RED + f"{Variazione} non è valido, indicare S o N.")
                    
                if Variazione.lower() == "s":

                    while True:
                        VarC = str(input("desideri variare i consumi fissi? (S/N): "))
                        if VarC.lower() == "s" or VarC.lower() == "n":
                            break
                        else:
                            print(colorama.Fore.RED + f"{VarC} non è valido, indicare S o N.")
                    if VarC.lower() == "s":
                        C_2 = value("A quanto ammontano i NUOVI consumi fissi? ")
                    elif VarC.lower() == "n":
                        C_2 = C_
                    else:
                        pass

                    while True:
                        VarI = str(input("desideri variare gli investimenti? (S/N): "))
                        if VarI.lower() == "s" or VarI.lower() == "n":
                            break
                        else:
                            print(colorama.Fore.RED + f"{VarI} non è valido, indicare S o N.")
                    if VarI.lower() == "s":
                        I_2 = value("A quanto ammontano i NUOVI investimenti? ")
                    elif VarI.lower() == "n":
                        I_2 = I_
                    else:
                        pass
                    
                    while True:
                        Varc = str(input("desideri variare la propensione al consumo delle famiglie? (S/N): "))
                        if Varc.lower() == "s" or Varc.lower() == "n":
                            break
                        else:
                            print(colorama.Fore.RED + f"{Varc} non è valido, indicare S o N.")
                    if Varc.lower() == "s":
                        c2 = parameter("A quanto ammonta la NUOVA propensione al consumo (inserire un valore tra 0 e 1)? ")
                    elif Varc.lower() == "n":
                        c2 = c
                    else:
                        pass

                    while True:
                        VarG = str(input("desideri variare la spesa pubblica? (S/N): "))
                        if VarG.lower() == "s" or VarG.lower() == "n":
                            break
                        else:
                            print(colorama.Fore.RED + f"{VarG} non è valido, indicare S o N.")
                    if VarG.lower() == "s":
                        G_2 = value("A quanto ammonta la NUOVA spesa pubblica? ")
                    elif VarG.lower() == "n":
                        G_2 = G_
                    else:
                        pass

                    while True:
                        VarTA = str(input("desideri variare le tasse? (S/N): "))
                        if VarTA.lower() == "s" or VarTA.lower() == "n":
                            break
                        else:
                            print(colorama.Fore.RED + f"{VarTA} non è valido, indicare S o N.")
                    if VarTA.lower() == "s":
                        TA_2 = value("A quanto ammontano le NUOVE tasse? ")
                    elif VarTA.lower() == "n":
                        TA_2 = TA_
                    else:
                        pass

                    while True:
                        VarTR = str(input("desideri variare i trasferimenti pubblici alle famiglie? (S/N): "))
                        if VarTR.lower() == "s" or VarTR.lower() == "n":
                            break
                        else:
                            print(colorama.Fore.RED + f"{VarTR} non è valido, indicare S o N.")
                    if VarTR.lower() == "s":
                        TR_2 = value("A quanto ammontano i NUOVI trasferimenti pubblici alle famiglie? ")
                    elif VarTR.lower() == "n":
                        TR_2 = TR_
                    else:
                        pass

                    if Occ.lower() == "s":
                        while True:
                            Varη = str(input("desideri variare la produttività dei lavoratori? (S/N): "))
                            if Varη.lower() == "s" or Varη.lower() == "n":
                                break
                            else:
                                print(colorama.Fore.RED + f"{Varη} non è valido, indicare S o N.")
                        if Varη.lower() == "s":
                            η2 = value("A quanto ammonta la NUOVA produttività dei lavoratori? ")
                        elif Varη.lower() == "n":
                            η2 = η
                        else:
                            pass

                        while True:
                            VarN_ = str(input("desideri variare l'offerta di lavoro? (S/N): "))
                            if VarN_.lower() == "s" or VarN_.lower() == "n":
                                break
                            else:
                                print(colorama.Fore.RED + f"{VarN_} non è valido, indicare S o N.")
                        if VarN_.lower() == "s":
                            N_2 = value("A quanto ammonta la NUOVA offerta di lavoro? ")
                        elif VarN_.lower() == "n":
                            N_2 = N_
                        else:
                            pass

                    #space
                    print("---")
                    print("")
                    
  
                    #Equations
                    Z_2 = C_2+I_2+G_2+c2*TR_2-c*TA_2
                    z2 = 1/(1-c2)
                    Y2 = z2*Z_2
                    Yd2 = Y2+TR_2-TA_2
                    C2 = C_2+c2*Yd2
                    Sn2 = Yd2-C2
                    BS2 = TA_2-(TR_2+G_2)
                    if Occ.lower() == "s":
                        N2 = Y2/η2
                        U2 = N_2-N2
                        u2 = U2/N_2

                    #Macro values (variazioni)
                    if Z_2 > Z_:
                        print(f"Ora la domanda autonoma ammonta a: {round(Z_2,2)}" + f" {Fore.GREEN}(+{round(Z_2-Z_, 2)})")
                    elif Z_2 == Z_:
                        print(f"La domanda autonoma è rimasta invariata: {round(Z_2,2)}")
                    elif Z_2 < Z_:
                        print(f"Ora la domanda autonoma ammonta a: {round(Z_2,2)}" + f" {Fore.RED}({round(Z_2-Z_, 2)})")

                    if z2 > z:
                        print(f"Ora il moltiplicatore keynesiano è: {round(z2,2)}" + f" {Fore.GREEN}(+{round(z2-z, 2)})")
                    elif z2 == z:
                        print(f"Il moltiplicatore keynesiano è rimasto invariato: {round(z2,2)}")
                    elif z2 < z:
                        print(f"Ora il moltiplicatore keynesiano è: {round(z2,2)}" + f" {Fore.RED}({round(z2-z, 2)})")

                    if Y2 > Y:
                        print(f"Ora il PIL ammonta a: {round(Y2,2)}" + f" {Fore.GREEN}(+{round(Y2-Y, 2)})")
                    elif Y2 == Y:
                        print(f"Il PIL è rimasto invariato: {round(Y2,2)}")
                    elif Y2 < Y:
                        print(f"Ora il PIL ammonta a: {round(Y2,2)}" + f" {Fore.RED}({round(Y2-Y, 2)})")

                    if C2 > C:
                        print(f"Ora i consumi ammontano a: {round(C2,2)}" + f" {Fore.GREEN}(+{round(C2-C, 2)})")
                    elif C2 == C:
                        print(f"I consumi sono rimasti invariati: {round(C2,2)}")
                    elif C2 < C:
                        print(f"Ora i consumi ammontano a: {round(C2,2)}" + f" {Fore.RED}({round(C2-C, 2)})")

                    if Sn2 > Sn:
                        print(f"Ora i risparmi delle famiglie ammontano a: {round(Sn2,2)}" + f" {Fore.GREEN}(+{round(Sn2-Sn, 2)})")
                    elif Sn2 == Sn:
                        print(f"I risparmi delle famiglie sono rimasti invariati: {round(Sn2,2)}")
                    elif Sn2 < Sn:
                        print(f"Ora i risparmi delle famiglie ammontano a: {round(Sn2,2)}" + f" {Fore.RED}({round(Sn2-Sn, 2)})")
                    elif Sn2 == 0:
                        print(f"Le famiglie consumano tutto il reddito a loro disposizione")
                    elif Sn2 < 0:
                        print(f"Le famiglie si indebitano per un ammontare pari a: {abs(round(Sn2,2))}")

                    if BS2 > BS:
                        print(f"Ora il bilancio dello Stato ammonta a: {round(BS2,2)}" + f" {Fore.GREEN}(+{round(BS2-BS, 2)})")
                    elif BS2 == BS:
                        print(f"Il bilancio dello Stato è rimasto invariato: {round(BS2,2)}")
                    elif BS2 < BS:
                        print(f"Ora il bilancio dello Stato ammonta a: {round(BS2,2)}" + f" {Fore.RED}({round(BS2-BS, 2)})")
                    if BS2 == 0:
                        print("Il bilancio dello Stato è in equilibrio")
                    elif BS2 > 0:
                        print(f"Il bilancio dello Stato è in surplus finanziario di {round(BS2,2)}")
                    elif BS2 < 0:
                        print(f"Il bilancio dello Stato è in deficit finanziario di {abs(round(BS2,2))}")

                    if Occ.lower() == "s":
                        if N2 > N:
                            print(f"Ora la domanda di lavoro ammonta a: {round(N2,2)}" + f" {Fore.GREEN}(+{round(N2-N, 2)})")
                        elif N2 == N:
                            print(f"La domanda di lavoro è rimasta invariata: {round(N2,2)}")
                        elif N2 < N:
                            print(f"Ora la domanda di lavoro ammonta a: {round(N2,2)}" + f" {Fore.RED}({round(N2-N, 2)})")

                        if U2 > U:
                            print(f"Ora la disoccupazione ammonta a: {round(U2,2)}" + f" {Fore.RED}(+{round(U2-U, 2)})")
                        elif U2 == U:
                            print(f"La disoccupazione è rimasta invariata: {round(U2,2)}")
                        elif U2 < U:
                            print(f"Ora la disoccupazione ammonta a: {round(U2,2)}" + f" {Fore.GREEN}({round(U2-U, 2)})")
                        if U2 > 0:
                            print(f"il numero di disoccupati ammonta a {round(U2,2)}")
                            print(f"la disoccupazione è al {round(u2*100, 2)}%")
                            print(f"Il reddito di pieno impiego sarebbe {round(η2*N_2,2)}")
                        elif U2 == 0:
                            print(f"Non c'è disoccupazione")
                        elif U2 < 0:
                            print(f"C'è piena occupazione con un eccesso di domanda di lavoro di {abs(round(U2,2))}")
                    

                    #Graph_Variations
                    #Mercato dei beni con occupazione_Variazione
                    if Occ.lower() == "s":
                        fig, axs = plt.subplots(2, 2, num="Mercato dei beni e occupazione- confronto")

                        ax11 = axs[0, 0]
                        ax21 = axs[1, 0]
                        ax12 = axs[0, 1]
                        ax22 = axs[1, 1]

                        Y_gr = np.linspace(0, Y*2, 1000)
                        Z_eq = Y_gr
                        Z_gr = Z_+c*Y_gr

                        N_gr = (1/η)*Y_gr

                        ax11.set_title("Mercato dei beni (t1)", fontsize=20, family="Arial")
                        ax11.set_xlim(left=0, right=Y*2)
                        ax11.set_ylim(bottom=0, top=Y*2)
                        ax21.set_xlim(left=0, right=Y*2)
                        ax21.set_ylim(bottom=0, top=Y*2)

                        Y_gr2 = np.linspace(0, Y2*2, 1000)
                        Z_eq2 = Y_gr2
                        Z_gr2 = Z_2+c2*Y_gr2
                        N_gr2 = (1/η2)*Y_gr2
                        
                        ax12.set_title("Mercato dei beni (t2)", fontsize=20, family="Arial")
                        ax12.set_xlim(left=0, right=Y*2)
                        ax12.set_ylim(bottom=0, top=Y*2)
                        ax22.set_xlim(left=0, right=Y*2)
                        ax22.set_ylim(bottom=0, top=Y*2)

                        #ax11 Setup
                        ax11.set_xlabel("Y", fontweight="bold", loc="right")
                        ax11.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
                        ax11.vlines(Y, 0, Y, linestyle="--", color="gray", alpha=0.7)

                        #ax21 Setup
                        ax21.set_xlabel("Y", fontweight="bold", loc="right")
                        ax21.set_ylabel("N", fontweight="bold", loc="top", rotation=0)
                        ax21.vlines(Y, 0, Y*2, linestyle="--", color="gray", alpha=0.7)
                        ax21.hlines(N, 0, Y, linestyle="--", color="gray", alpha=0.7)
                        ax21.vlines(Y_, 0, N_, linestyle="--", color="gray", alpha=0.7)
                        ax21.hlines(N_, 0, Y_, linestyle="--", color="gray", alpha=0.7)

                        #ax12 Setup
                        ax12.set_xlabel("Y", fontweight="bold", loc="right")
                        ax12.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
                        ax12.vlines(Y2, 0, Y2, linestyle="--", color="gray", alpha=0.7)

                        #ax22 Setup
                        ax22.set_xlabel("Y", fontweight="bold", loc="right")
                        ax22.set_ylabel("N", fontweight="bold", loc="top", rotation=0)
                        ax22.vlines(Y2, 0, Y2*2, linestyle="--", color="gray", alpha=0.7)
                        ax22.hlines(N2, 0, Y2, linestyle="--", color="gray", alpha=0.7)
                        ax22.vlines(η2*N_2, 0, N_2, linestyle="--", color="gray", alpha=0.7)
                        ax22.hlines(N_2, 0, η2*N_2, linestyle="--", color="gray", alpha=0.7)

                        #ax11 lines
                        ax11.plot(Y_gr, Z_eq, color="blue")
                        ax11.plot(Y_gr, Z_gr, color="blue")

                        #ax21 lines
                        ax21.plot(Y_gr, N_gr, color="blue")

                        #ax12 lines
                        ax12.plot(Y_gr2, Z_eq2, color="blue")
                        ax12.plot(Y_gr2, Z_gr2, color="blue")
                        
                        #ax22 lines
                        ax22.plot(Y_gr2, N_gr2, color="blue")

                        #ax11 Points
                        ax11.plot(Y, Y, "o", color="red", markersize=2)
                        ax11.annotate("E", (Y, Y), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                        ax11.plot(0, Z_, "_", color="red", markersize=10)
                        ax11.annotate(rf"$\overline{{Z}}={round(Z_)}$", (0, Z_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                        ax11.plot(Y, 0, "|", color="red", markersize=10)
                        ax11.annotate(f"Y*={round(Y)}", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                        #ax21 Points
                        ax21.plot(Y, N, "o", color="red", markersize=2)
                        ax21.plot(0, N, "_", color="red", markersize=10)
                        ax21.plot(Y_, N_, "o", color="red", markersize=2)
                        ax21.annotate(f"N*={round(N)}", (0, N), xytext=(55, 5), textcoords="offset points", fontsize=12, color="black")
                        ax21.plot(0, N_, "_", color="red", markersize=10)
                        ax21.annotate(rf"$\overline{{N}}={round(N_)}$", (0, N_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                        ax21.plot(Y, 0, "|", color="red", markersize=10)
                        ax21.annotate("Y*", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                        ax21.plot(Y_, 0, "|", color="red", markersize=10)
                        ax21.annotate(rf"$\overline{{Y}}={round(Y_)}$", (Y_, 0), xytext=(2, -35), textcoords="offset points", fontsize=12, color="black")

                        #ax12 Points
                        ax12.plot(Y2, Y2, "o", color="red", markersize=2)
                        ax12.annotate("E", (Y2, Y2), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                        ax12.plot(0, Z_2, "_", color="red", markersize=10)
                        ax12.annotate(rf"$\overline{{Z2}}={round(Z_2)}$", (0, Z_2), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                        ax12.plot(Y2, 0, "|", color="red", markersize=10)
                        ax12.annotate(f"Y2*={round(Y2)}", (Y2, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                        #ax22 Points
                        ax22.plot(Y2, N2, "o", color="red", markersize=2)
                        ax22.plot(0, N2, "_", color="red", markersize=10)
                        ax22.plot(η2*N_2, N_2, "o", color="red", markersize=2)
                        ax22.annotate(f"N2*={round(N2)}", (0, N2), xytext=(55, 5), textcoords="offset points", fontsize=12, color="black")
                        ax22.plot(0, N_2, "_", color="red", markersize=10)
                        ax22.annotate(rf"$\overline{{N2}}={round(N_2)}$", (0, N_2), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                        ax22.plot(Y2, 0, "|", color="red", markersize=10)
                        ax22.annotate("Y2*", (Y2, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                        ax22.plot(η2*N_2, 0, "|", color="red", markersize=10)
                        ax22.annotate(rf"$\overline{{Y2}}={round(η2*N_2)}$", (η2*N_2, 0), xytext=(2, -35), textcoords="offset points", fontsize=12, color="black")

                        pass

                    #Mercato dei beni senza occupazione_Variazione
                    if Occ.lower() == "n":
                        fig, axs = plt.subplots(1, 2, num="Mercato dei beni - confronto")

                        ax11 = axs[0]
                        ax12 = axs[1]

                        Y_gr = np.linspace(0, Y*2, 1000)
                        Z_eq = Y_gr
                        Z_gr = Z_+c*Y_gr

                        Y_gr2 = np.linspace(0, Y2*2, 1000)
                        Z_eq2 = Y_gr2
                        Z_gr2 = Z_2+c2*Y_gr2

                        ax11.set_title("Mercato dei beni(t1)", fontsize=20, family="Arial")
                        ax11.set_xlim(left=0, right=Y*2)
                        ax11.set_ylim(bottom=0, top=Y*2)

                        ax12.set_title("Mercato dei beni(t2)", fontsize=20, family="Arial")
                        ax12.set_xlim(left=0, right=Y*2)
                        ax12.set_ylim(bottom=0, top=Y*2)

                        #ax11 Setup
                        ax11.set_xlabel("Y", fontweight="bold", loc="right")
                        ax11.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
                        ax11.vlines(Y, 0, Y, linestyle="--", color="gray", alpha=0.7)

                        #ax12 Setup
                        ax12.set_xlabel("Y", fontweight="bold", loc="right")
                        ax12.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
                        ax12.vlines(Y2, 0, Y2, linestyle="--", color="gray", alpha=0.7)

                        #ax11 lines
                        ax11.plot(Y_gr, Z_eq, color="blue")
                        ax11.plot(Y_gr, Z_gr, color="blue")

                        #ax12 lines
                        ax12.plot(Y_gr2, Z_eq2, color="blue")
                        ax12.plot(Y_gr2, Z_gr2, color="blue")

                        #ax11 Points
                        ax11.plot(Y, Y, "o", color="red", markersize=2)
                        ax11.annotate("E", (Y, Y), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                        ax11.plot(0, Z_, "_", color="red", markersize=10)
                        ax11.annotate(rf"$\overline{{Z}}={round(Z_)}$", (0, Z_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                        ax11.plot(Y, 0, "|", color="red", markersize=10)
                        ax11.annotate(f"Y*={round(Y)}", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                        #ax12 Points
                        ax12.plot(Y2, Y2, "o", color="red", markersize=2)
                        ax12.annotate("E", (Y2, Y2), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                        ax12.plot(0, Z_2, "_", color="red", markersize=10)
                        ax12.annotate(rf"$\overline{{Z2}}={round(Z_2)}$", (0, Z_2), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                        ax12.plot(Y2, 0, "|", color="red", markersize=10)
                        ax12.annotate(f"Y*={round(Y2)}", (Y2, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                        pass

                    #Risparmio delle famiglie_Variazione
                    fig, axs = plt.subplots(1, 2, num="Risparmio e investimenti")

                    ax11 = axs[0]
                    ax12 = axs[1]

                    Y_gr = np.linspace(0, Yd*2, 1000)
                    SI_gr = -C_+(1-c)*Y_gr

                    Y_gr2 = np.linspace(0, Yd2*2, 1000)
                    SI_gr2 = -C_2+(1-c2)*Y_gr2

                    ax11.set_title("Risparmio e investimenti (t1)", fontsize=20, family="Arial")
                    ax11.set_xlim(left=0, right=Yd*2) 
                    ax11.set_ylim(bottom=-C_*2-100, top=Yd)

                    ax12.set_title("Risparmio e investimenti (t2)", fontsize=20, family="Arial")
                    ax12.set_xlim(left=0, right=Yd*2) 
                    ax12.set_ylim(bottom=-C_*2-100, top=Yd)

                    ax11.hlines(0, 0, Yd*2, color="black", linewidth=0.5)
                    ax12.hlines(0, 0, Yd2*2, color="black", linewidth=0.5)

                    #ax11 Setup
                    ax11.set_xlabel("Yd", fontweight="bold", loc="right")
                    ax11.set_ylabel("Sn", fontweight="bold", loc="top")
                    ax11.vlines(Yd, 0, Sn, linestyle="--", color="gray", alpha=0.7)

                    #ax12 Setup
                    ax12.set_xlabel("Yd", fontweight="bold", loc="right")
                    ax12.set_ylabel("Sn", fontweight="bold", loc="top")
                    ax12.vlines(Yd2, 0, Sn2, linestyle="--", color="gray", alpha=0.7)

                    #ax11 lines
                    ax11.plot(Y_gr, SI_gr, color="blue")
                    ax11.hlines(Sn, 0, Yd*2, color="blue")

                    #ax12 lines
                    ax12.plot(Y_gr2, SI_gr2, color="blue")
                    ax12.hlines(Sn2, 0, Yd2*2, color="blue")

                    #ax11 Points
                    ax11.plot(Yd, Sn, "o", color="red", markersize=2)
                    ax11.annotate("E", (Yd, Sn), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                    ax11.plot(0, Sn, "_", color="red", markersize=10)
                    ax11.annotate(f"Sn*={round(Sn)}", (0, Sn), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax11.plot(Yd, 0, "|", color="red", markersize=10)
                    ax11.annotate(f"Yd*={round(Yd)}", (Yd, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax11.plot(0, -C_, "_", color="red", markersize=10)
                    ax11.annotate(rf"-$\overline{{C}}={round(-C_)}$", (0, -C_), xytext=(2, -15), textcoords="offset points", fontsize=12, color="black")

                    #ax12 Points
                    ax12.plot(Yd2, Sn2, "o", color="red", markersize=2)
                    ax12.annotate("E", (Yd2, Sn2), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                    ax12.plot(0, Sn2, "_", color="red", markersize=10)
                    ax12.annotate(f"Sn2*={round(Sn2)}", (0, Sn2), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax12.plot(Yd, 0, "|", color="red", markersize=10)
                    ax12.annotate(f"Yd2*={round(Yd2)}", (Yd2, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax12.plot(0, -C_2, "_", color="red", markersize=10)
                    ax12.annotate(rf"-$\overline{{C2}}={round(-C_2)}$", (0, -C_2), xytext=(2, -15), textcoords="offset points", fontsize=12, color="black")

                    print(colorama.Fore.RED + "CHIUDERE TUTTI I GRAFICI PER POTER CONTINUARE.") 
                    plt.show()

                if Variazione.lower() == "n":     
                    riavvia_programma()
                


    #Tasse endogene
    if SP.lower() == "s" and Tasse.lower() == "en":
        while True:

            #inputs
            C_ = value("A quanto ammontano i consumi fissi? ")
            I_ = value("A quanto ammontano gli investimenti delle imprese? ")
            c = parameter("A quanto ammonta la propensione al consumo delle famiglie (inserire un valore tra 0 e 1)? ")
            G_ = value("A quanto ammonta la spesa pubblica? ")
            t = parameter("Qual è l'entità della pressione fiscale (inserire un valore tra 0 e 1)? ")
            TR_ = value("A quanto ammontano i trasferimenti pubblici alle famiglie? ")

            #Equations
            Z_ = C_+I_+G_+c*TR_
            z = 1/(1-c*(1-t))
            Y = z*Z_
            Yd = Y*(1-t)+TR_
            C = C_+c*Yd
            Sn = Yd-C
            BS = t*Y-(TR_+G_)

            #disoccupazione
            if Occ.lower() == "s":
                η = value("A quanto ammonta la produttività del lavoro? ")
                N_ = value("A quanto ammonta la popolazione attiva (offerta di lavoro)? ")
                N = Y/η
                U = N_-N
                u = U/N_
                Y_ = η*N_
            else:
                pass

            #space
            print("---")
            print("")

            #Macro values
            print(f"La domanda autonoma ammonta a: {round(Z_,2)}")
            print(f"Il moltiplicatore keynesiano è: {round(z,2)}")
            print(f"Il PIL ammonta a: {round(Y,2)}")
            print(f"Il reddito disponibile ammonta a: {round(Yd,2)}")
            print(f"I consumi ammontano a: {round(C,2)}")
            if Sn > 0:
                print(f"Il risparmio delle famiglie ammonta a: {round(Sn,2)}")
            elif Sn == 0:
                print(f"Le famiglie consumano tutto il reddito a loro disposizione")
            elif Sn < 0:
                print(f"Le famiglie si indebitano per un ammontare pari a: {round(abs(Sn))}")
            if Occ.lower() == "s":
                print(f"La domanda di lavoro ammonta a {round(N,2)}")
                if U > 0:
                    print(f"il numero di disoccupati ammonta a {round(U,2)}")
                    print(f"la disoccupazione è al {round(u*100, 2)}%")
                    print(f"Il reddito di pieno impiego sarebbe {round(Y_,2)}")
                elif U == 0:
                    print(f"Non c'è disoccupazione")
                elif U < 0:
                    print(f"C'è piena occupazione con un eccesso di domanda di lavoro di {abs(round(U,2))}")
            else:
                pass

            #Analysis:
            #Bilancio dello Stato
            if BS == 0:
                print("Il bilancio dello Stato è in equilibrio")
            elif BS > 0:
                print(f"Il bilancio dello Stato è in surplus finanziario di {round(BS,2)}")
            elif BS < 0:
                print(f"Il bilancio dello Stato è in deficit finanziario di {abs(round(BS,2))}")
            
            #space
            print("---")
            print("")

            #Graphics
            #Mercato dei beni
            Y_gr = np.linspace(0, Y*2, 1000)
            Z_eq = Y_gr
            Z_gr = Z_+c*(1-t)*Y_gr
            #Con disoccupazione
            if Occ.lower() == "s":
                N_gr = (1/η)*Y_gr

                fig, (ax1, ax2) = plt.subplots(2, 1, num="Mercato dei beni e occupazione")
                ax1.set_xlim(left=0, right=Y*2)
                ax1.set_ylim(bottom=0, top=Y*2)
                ax2.set_xlim(left=0, right=Y*2)
                ax2.set_ylim(bottom=0, top=Y*2)
                ax1.set_title("Mercato dei beni", fontsize=20, family="Arial")

                #ax1 Setup
                ax1.set_xlabel("Y", fontweight="bold", loc="right")
                ax1.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
                ax1.vlines(Y, 0, Y, linestyle="--", color="gray", alpha=0.7)

                #ax1 lines
                ax1.plot(Y_gr, Z_eq, color="blue")
                ax1.plot(Y_gr, Z_gr, color="blue")

                #ax1 Points
                ax1.plot(Y, Y, "o", color="red", markersize=2)
                ax1.annotate("E", (Y, Y), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                ax1.plot(0, Z_, "_", color="red", markersize=10)
                ax1.annotate(rf"$\overline{{Z}}={round(Z_)}$", (0, Z_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                ax1.plot(Y, 0, "|", color="red", markersize=10)
                ax1.annotate(f"Y*={round(Y)}", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                #ax2 Setup
                ax2.set_xlabel("Y", fontweight="bold", loc="right")
                ax2.set_ylabel("N", fontweight="bold", loc="top", rotation=0)
                ax2.vlines(Y, 0, Y*2, linestyle="--", color="gray", alpha=0.7)
                ax2.hlines(N, 0, Y, linestyle="--", color="gray", alpha=0.7)
                ax2.vlines(Y_, 0, N_, linestyle="--", color="gray", alpha=0.7)
                ax2.hlines(N_, 0, Y_, linestyle="--", color="gray", alpha=0.7)
                #ax2 lines
                ax2.plot(Y_gr, N_gr, color="blue")
                #ax2 Points
                ax2.plot(Y, N, "o", color="red", markersize=2)
                ax2.plot(0, N, "_", color="red", markersize=10)
                ax2.plot(Y_, N_, "o", color="red", markersize=2)
                ax2.annotate(f"N*={round(N)}", (0, N), xytext=(55, 5), textcoords="offset points", fontsize=12, color="black")
                ax2.plot(0, N_, "_", color="red", markersize=10)
                ax2.annotate(rf"$\overline{{N}}={round(N_)}$", (0, N_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                if Y_ > Y:
                    ax2.plot(Y_, 0, "|", color="red", markersize=10)
                    ax2.annotate(rf"$\overline{{Y}}={round(Y_)}$", (Y_, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                else:
                    ax2.plot(Y_, 0, "|", color="red", markersize=10)
                    ax2.annotate(r"$\overline{Y}$", (Y_, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                ax2.plot(Y, 0, "|", color="red", markersize=10)
                ax2.annotate("Y*", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                pass

            #Senza disoccupazione
            if Occ.lower() == "n":
                plt.figure(num="Mercato dei beni")
                plt.xlim(left=0, right=Y*2)
                plt.ylim(bottom=0, top=Y*2)
                plt.title("Mercato dei beni", fontsize=20, family="Arial")

                #Setup
                plt.xlabel("Y", fontweight="bold", loc="right")
                plt.ylabel("Z", fontweight="bold", loc="top")
                plt.vlines(Y, 0, Y, linestyle="--", color="gray", alpha=0.7)

                #Lines
                plt.plot(Y_gr, Z_eq, color="blue")
                plt.plot(Y_gr, Z_gr, color="blue")

                #Points
                plt.plot(Y, Y, "o", color="red", markersize=2)
                plt.annotate("E", (Y, Y), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                plt.plot(0, Z_, "_", color="red", markersize=10)
                plt.annotate(rf"$\overline{{Z}}={round(Z_)}$", (0, Z_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                plt.plot(Y, 0, "|", color="red", markersize=10)
                plt.annotate(f"Y*={round(Y)}", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                pass

            #Risparmio delle famiglie
            plt.figure(num="Risparmio e investimenti")
            Yd_gr = np.linspace(0, Yd*2, 1000)
            SI_gr = -C_+(1-c)*Yd_gr

            plt.xlim(left=0, right=Yd*2)
            plt.ylim(bottom=-C_*2-100, top=Yd)
            plt.hlines(0, 0, Yd*2, color="black", linewidth=0.5)
            plt.title("Risparmio e investimenti", fontsize=20, family="Arial")

            #Setup
            plt.xlabel("Yd", fontweight="bold", loc="right")
            plt.ylabel("Sn", fontweight="bold", loc="top")
            plt.vlines(Yd, 0, Sn, linestyle="--", color="gray", alpha=0.7)

            #Lines
            plt.plot(Yd_gr, SI_gr, color="blue")
            plt.hlines(Sn, 0, Yd*2, color="blue")

            #Points
            plt.plot(Yd, Sn, "o", color="red", markersize=2)
            plt.annotate("E", (Yd, Sn), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
            plt.plot(0, Sn, "_", color="red", markersize=10)
            plt.annotate(f"Sn*={round(Sn)}", (0, Sn), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
            plt.plot(Yd, 0, "|", color="red", markersize=10)
            plt.annotate(f"Yd*={round(Yd)}", (Yd, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
            plt.plot(0, -C_, "_", color="red", markersize=10)
            plt.annotate(rf"-$\overline{{C}}={round(-C_)}$", (0, -C_), xytext=(2, -15), textcoords="offset points", fontsize=12, color="black")



            #Bilancio dello Stato
            Y_gr = np.linspace(0, Y*2, 1000)
            BS_gr = -(G_+TR_)+(t*Y_gr)

            fig, (ax1, ax2) = plt.subplots(2, 1, num="Bilancio dello Stato")
            ax1.set_xlim(left=0, right=Y*2)
            ax1.set_ylim(bottom=0, top=Y*2)
            ax2.set_xlim(left=0, right=Y*2)
            ax2.set_ylim(bottom=-(G_+TR_)*3-100, top=Y*2)
            ax1.set_title("Bilancio dello Stato", fontsize=20, family="Arial")

            #ax1 Setup
            ax1.set_xlabel("Y", fontweight="bold", loc="right")
            ax1.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
            ax1.vlines(Y, 0, Y, linestyle="--", color="gray", alpha=0.7)

            #ax1 lines
            ax1.plot(Y_gr, Z_eq, color="blue")
            ax1.plot(Y_gr, Z_gr, color="blue")

            #ax1 Points
            ax1.plot(Y, Y, "o", color="red", markersize=2)
            ax1.annotate("E", (Y, Y), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
            ax1.plot(0, Z_, "_", color="red", markersize=10)
            ax1.annotate(rf"$\overline{{Z}}={round(Z_)}$", (0, Z_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
            ax1.plot(Y, 0, "|", color="red", markersize=10)
            ax1.annotate(f"Y*={round(Y)}", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

            #ax2 Setup
            ax2.set_xlabel("Y", fontweight="bold", loc="right")
            ax2.set_ylabel("BS", fontweight="bold", loc="top", rotation=0)
            ax2.vlines(Y, -(G_+TR_)+(Y*t), Y*2, linestyle="--", color="gray", alpha=0.7)
            ax2.hlines(BS, 0, Y, linestyle="--", color="gray", alpha=0.7)

            #ax2 lines
            ax2.hlines(0, 0, Y*2, color="black", linewidth=0.5)
            ax2.plot(Y_gr, BS_gr, color="blue")

            #ax2 Points
            ax2.plot(Y, -(G_+TR_)+(Y*t), "o", color="red", markersize=2)
            ax2.annotate(f"BS={round(BS)}", (0, BS), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
            ax2.plot(0, -(G_+TR_), "_", color="red", markersize=10)
            ax2.annotate(rf"-($\overline{{G}}$+" + rf"$\overline{{TR}}$)={-(G_+TR_)}", (0, -(G_+TR_)), xytext=(5, -15), textcoords="offset points", fontsize=12, color="black")
            ax2.plot(0, BS, "_", color="red", markersize=10)

            print(colorama.Fore.RED + "CHIUDERE TUTTI I GRAFICI PER POTER CONTINUARE.") 
            plt.show()

            #Variazioni
            while True:
                Variazione = str(input("Desideri variare una o più variabili per un confronto (S/N)? "))
                if Variazione.lower() == "s" or Variazione.lower() == "n":
                    pass
                else:
                    print(colorama.Fore.RED + f"{Variazione} non è valido, indicare S o N.")
                    
                if Variazione.lower() == "s":

                    while True:
                        VarC = str(input("desideri variare i consumi fissi? (S/N): "))
                        if VarC.lower() == "s" or VarC.lower() == "n":
                            break
                        else:
                            print(colorama.Fore.RED + f"{VarC} non è valido, indicare S o N.")
                    if VarC.lower() == "s":
                        C_2 = value("A quanto ammontano i NUOVI consumi fissi? ")
                    elif VarC.lower() == "n":
                        C_2 = C_
                    else:
                        pass

                    while True:
                        VarI = str(input("desideri variare gli investimenti? (S/N): "))
                        if VarI.lower() == "s" or VarI.lower() == "n":
                            break
                        else:
                            print(colorama.Fore.RED + f"{VarI} non è valido, indicare S o N.")
                    if VarI.lower() == "s":
                        I_2 = value("A quanto ammontano i NUOVI investimenti? ")
                    elif VarI.lower() == "n":
                        I_2 = I_
                    else:
                        pass
                    
                    while True:
                        Varc = str(input("desideri variare la propensione al consumo delle famiglie? (S/N): "))
                        if Varc.lower() == "s" or Varc.lower() == "n":
                            break
                        else:
                            print(colorama.Fore.RED + f"{Varc} non è valido, indicare S o N.")
                    if Varc.lower() == "s":
                        c2 = parameter("A quanto ammonta la NUOVA propensione al consumo (inserire un valore tra 0 e 1)? ")
                    elif Varc.lower() == "n":
                        c2 = c
                    else:
                        pass

                    while True:
                        VarG = str(input("desideri variare la spesa pubblica? (S/N): "))
                        if VarG.lower() == "s" or VarG.lower() == "n":
                            break
                        else:
                            print(colorama.Fore.RED + f"{VarG} non è valido, indicare S o N.")
                    if VarG.lower() == "s":
                        G_2 = value("A quanto ammonta la NUOVA spesa pubblica? ")
                    elif VarG.lower() == "n":
                        G_2 = G_
                    else:
                        pass

                    while True:
                        Vart = str(input("desideri variare la pressione fiscale? (S/N): "))
                        if Vart.lower() == "s" or Vart.lower() == "n":
                            break
                        else:
                            print(colorama.Fore.RED + f"{Vart} non è valido, indicare S o N.")
                    if Vart.lower() == "s":
                        t2 = parameter("A quanto ammonta la NUOVA pressione fiscale (inserire un valore tra 0 e 1)")
                    elif Vart.lower() == "n":
                        t2 = t
                    else:
                        pass

                    while True:
                        VarTR = str(input("desideri variare i trasferimenti pubblici alle famiglie? (S/N): "))
                        if VarTR.lower() == "s" or VarTR.lower() == "n":
                            break
                        else:
                            print(colorama.Fore.RED + f"{VarTR} non è valido, indicare S o N.")
                    if VarTR.lower() == "s":
                        TR_2 = value("A quanto ammontano i NUOVI trasferimenti pubblici alle famiglie? ")
                    elif VarTR.lower() == "n":
                        TR_2 = TR_
                    else:
                        pass

                    if Occ.lower() == "s":
                        while True:
                            Varη = str(input("desideri variare la produttività dei lavoratori? (S/N): "))
                            if Varη.lower() == "s" or Varη.lower() == "n":
                                break
                            else:
                                print(colorama.Fore.RED + f"{Varη} non è valido, indicare S o N.")
                        if Varη.lower() == "s":
                            η2 = value("A quanto ammonta la NUOVA produttività dei lavoratori? ")
                        elif Varη.lower() == "n":
                            η2 = η
                        else:
                            pass

                        while True:
                            VarN_ = str(input("desideri variare l'offerta di lavoro? (S/N): "))
                            if VarN_.lower() == "s" or VarN_.lower() == "n":
                                break
                            else:
                                print(colorama.Fore.RED + f"{VarN_} non è valido, indicare S o N.")
                        if VarN_.lower() == "s":
                            N_2 = value("A quanto ammonta la NUOVA offerta di lavoro? ")
                        elif VarN_.lower() == "n":
                            N_2 = N_
                        else:
                            pass

                    #space
                    print("---")
                    print("")                
  
                    #Equations
                    Z_2 = C_2+I_2+G_2+c2*TR_2
                    z2 = 1/(1-c2*(1-t2))
                    Y2 = z2*Z_2
                    Yd2 = (1-t2)*Y2+TR_2
                    C2 = C_2+c2*Yd2
                    Sn2 = Yd2-C2
                    BS2 = Y2*t2-(TR_2+G_2)
                    if Occ.lower() == "s":
                        N2 = Y2/η2
                        U2 = N_2-N2
                        u2 = U2/N_2

                    #Macro values (variazioni)
                    if Z_2 > Z_:
                        print(f"Ora la domanda autonoma ammonta a: {round(Z_2,2)}" + f" {Fore.GREEN}(+{round(Z_2-Z_, 2)})")
                    elif Z_2 == Z_:
                        print(f"La domanda autonoma è rimasta invariata: {round(Z_2,2)}")
                    elif Z_2 < Z_:
                        print(f"Ora la domanda autonoma ammonta a: {round(Z_2,2)}" + f" {Fore.RED}({round(Z_2-Z_, 2)})")

                    if z2 > z:
                        print(f"Ora il moltiplicatore keynesiano è: {round(z2,2)}" + f" {Fore.GREEN}(+{round(z2-z, 2)})")
                    elif z2 == z:
                        print(f"Il moltiplicatore keynesiano è rimasto invariato: {round(z2,2)}")
                    elif z2 < z:
                        print(f"Ora il moltiplicatore keynesiano è: {round(z2,2)}" + f" {Fore.RED}({round(z2-z, 2)})")

                    if Y2 > Y:
                        print(f"Ora il PIL ammonta a: {round(Y2,2)}" + f" {Fore.GREEN}(+{round(Y2-Y, 2)})")
                    elif Y2 == Y:
                        print(f"Il PIL è rimasto invariato: {round(Y2,2)}")
                    elif Y2 < Y:
                        print(f"Ora il PIL ammonta a: {round(Y2,2)}" + f" {Fore.RED}({round(Y2-Y, 2)})")

                    if C2 > C:
                        print(f"Ora i consumi ammontano a: {round(C2,2)}" + f" {Fore.GREEN}(+{round(C2-C, 2)})")
                    elif C2 == C:
                        print(f"I consumi sono rimasti invariati: {round(C2,2)}")
                    elif C2 < C:
                        print(f"Ora i consumi ammontano a: {round(C2,2)}" + f" {Fore.RED}({round(C2-C, 2)})")

                    if Sn2 > Sn:
                        print(f"Ora i risparmi delle famiglie ammontano a: {round(Sn2,2)}" + f" {Fore.GREEN}(+{round(Sn2-Sn, 2)})")
                    elif Sn2 == Sn:
                        print(f"I risparmi delle famiglie sono rimasti invariati: {round(Sn2,2)}")
                    elif Sn2 < Sn:
                        print(f"Ora i risparmi delle famiglie ammontano a: {round(Sn2,2)}" + f" {Fore.RED}({round(Sn2-Sn, 2)})")
                    elif Sn2 == 0:
                        print(f"Le famiglie consumano tutto il reddito a loro disposizione")
                    elif Sn2 < 0:
                        print(f"Le famiglie si indebitano per un ammontare pari a: {abs(round(Sn2,2))}")

                    if BS2 > BS:
                        print(f"Ora il bilancio dello Stato ammonta a: {round(BS2,2)}" + f" {Fore.GREEN}(+{round(BS2-BS, 2)})")
                    elif BS2 == BS:
                        print(f"Il bilancio dello Stato è rimasto invariato: {round(BS2,2)}")
                    elif BS2 < BS:
                        print(f"Ora il bilancio dello Stato ammonta a: {round(BS2,2)}" + f" {Fore.RED}({round(BS2-BS, 2)})")
                    if BS2 == 0:
                        print("Il bilancio dello Stato è in equilibrio")
                    elif BS2 > 0:
                        print(f"Il bilancio dello Stato è in surplus finanziario di {round(BS2,2)}")
                    elif BS2 < 0:
                        print(f"Il bilancio dello Stato è in deficit finanziario di {abs(round(BS2,2))}")

                    if Occ.lower() == "s":
                        if N2 > N:
                            print(f"Ora la domanda di lavoro ammonta a: {round(N2,2)}" + f" {Fore.GREEN}(+{round(N2-N, 2)})")
                        elif N2 == N:
                            print(f"La domanda di lavoro è rimasta invariata: {round(N2,2)}")
                        elif N2 < N:
                            print(f"Ora la domanda di lavoro ammonta a: {round(N2,2)}" + f" {Fore.RED}({round(N2-N, 2)})")

                        if U2 > U:
                            print(f"Ora la disoccupazione ammonta a: {round(U2,2)}" + f" {Fore.RED}(+{round(U2-U, 2)})")
                        elif U2 == U:
                            print(f"La disoccupazione è rimasta invariata: {round(U2,2)}")
                        elif U2 < U:
                            print(f"Ora la disoccupazione ammonta a: {round(U2,2)}" + f" {Fore.GREEN}({round(U2-U, 2)})")
                        if U2 > 0:
                            print(f"il numero di disoccupati ammonta a {round(U2,2)}")
                            print(f"la disoccupazione è al {round(u2*100, 2)}%")
                            print(f"Il reddito di pieno impiego sarebbe {round(η2*N_2,2)}")
                        elif U2 == 0:
                            print(f"Non c'è disoccupazione")
                        elif U2 < 0:
                            print(f"C'è piena occupazione con un eccesso di domanda di lavoro di {abs(round(U2,2))}")
                    

                    #Graph_Variations
                    #Mercato dei beni con occupazione_Variazione
                    if Occ.lower() == "s":
                        fig, axs = plt.subplots(2, 2, num="Mercato dei beni e occupazione - confronto")

                        ax11 = axs[0, 0]
                        ax21 = axs[1, 0]
                        ax12 = axs[0, 1]
                        ax22 = axs[1, 1]

                        Y_gr = np.linspace(0, Y*2, 1000)
                        Z_eq = Y_gr
                        Z_gr = Z_+c*(1-t)*Y_gr

                        N_gr = (1/η)*Y_gr

                        ax11.set_title("Mercato dei beni (t1)", fontsize=20, family="Arial")
                        ax11.set_xlim(left=0, right=Y*2)
                        ax11.set_ylim(bottom=0, top=Y*2)
                        ax21.set_xlim(left=0, right=Y*2)
                        ax21.set_ylim(bottom=0, top=Y*2)

                        Y_gr2 = np.linspace(0, Y2*2, 1000)
                        Z_eq2 = Y_gr2
                        Z_gr2 = Z_2+c2*(1-t2)*Y_gr2
                        N_gr2 = (1/η2)*Y_gr2
                        
                        ax12.set_title("Mercato dei beni (t2)", fontsize=20, family="Arial")
                        ax12.set_xlim(left=0, right=Y*2)
                        ax12.set_ylim(bottom=0, top=Y*2)
                        ax22.set_xlim(left=0, right=Y*2)
                        ax22.set_ylim(bottom=0, top=Y*2)

                        #ax11 Setup
                        ax11.set_xlabel("Y", fontweight="bold", loc="right")
                        ax11.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
                        ax11.vlines(Y, 0, Y, linestyle="--", color="gray", alpha=0.7)

                        #ax21 Setup
                        ax21.set_xlabel("Y", fontweight="bold", loc="right")
                        ax21.set_ylabel("N", fontweight="bold", loc="top", rotation=0)
                        ax21.vlines(Y, 0, Y*2, linestyle="--", color="gray", alpha=0.7)
                        ax21.hlines(N, 0, Y, linestyle="--", color="gray", alpha=0.7)
                        ax21.vlines(Y_, 0, N_, linestyle="--", color="gray", alpha=0.7)
                        ax21.hlines(N_, 0, Y_, linestyle="--", color="gray", alpha=0.7)

                        #ax12 Setup
                        ax12.set_xlabel("Y", fontweight="bold", loc="right")
                        ax12.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
                        ax12.vlines(Y2, 0, Y2, linestyle="--", color="gray", alpha=0.7)

                        #ax22 Setup
                        ax22.set_xlabel("Y", fontweight="bold", loc="right")
                        ax22.set_ylabel("N", fontweight="bold", loc="top", rotation=0)
                        ax22.vlines(Y2, 0, Y2*2, linestyle="--", color="gray", alpha=0.7)
                        ax22.hlines(N2, 0, Y2, linestyle="--", color="gray", alpha=0.7)
                        ax22.vlines(η2*N_2, 0, N_2, linestyle="--", color="gray", alpha=0.7)
                        ax22.hlines(N_2, 0, η2*N_2, linestyle="--", color="gray", alpha=0.7)

                        #ax11 lines
                        ax11.plot(Y_gr, Z_eq, color="blue")
                        ax11.plot(Y_gr, Z_gr, color="blue")

                        #ax21 lines
                        ax21.plot(Y_gr, N_gr, color="blue")

                        #ax12 lines
                        ax12.plot(Y_gr2, Z_eq2, color="blue")
                        ax12.plot(Y_gr2, Z_gr2, color="blue")
                        
                        #ax22 lines
                        ax22.plot(Y_gr2, N_gr2, color="blue")

                        #ax11 Points
                        ax11.plot(Y, Y, "o", color="red", markersize=2)
                        ax11.annotate("E", (Y, Y), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                        ax11.plot(0, Z_, "_", color="red", markersize=10)
                        ax11.annotate(rf"$\overline{{Z}}={round(Z_)}$", (0, Z_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                        ax11.plot(Y, 0, "|", color="red", markersize=10)
                        ax11.annotate(f"Y*={round(Y)}", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                        #ax21 Points
                        ax21.plot(Y, N, "o", color="red", markersize=2)
                        ax21.plot(0, N, "_", color="red", markersize=10)
                        ax21.plot(Y_, N_, "o", color="red", markersize=2)
                        ax21.annotate(f"N*={round(N)}", (0, N), xytext=(55, 5), textcoords="offset points", fontsize=12, color="black")
                        ax21.plot(0, N_, "_", color="red", markersize=10)
                        ax21.annotate(rf"$\overline{{N}}={round(N_)}$", (0, N_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                        ax21.plot(Y, 0, "|", color="red", markersize=10)
                        ax21.annotate("Y*", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                        ax21.plot(Y_, 0, "|", color="red", markersize=10)
                        ax21.annotate(rf"$\overline{{Y}}={round(Y_)}$", (Y_, 0), xytext=(2, -35), textcoords="offset points", fontsize=12, color="black")

                        #ax12 Points
                        ax12.plot(Y2, Y2, "o", color="red", markersize=2)
                        ax12.annotate("E", (Y2, Y2), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                        ax12.plot(0, Z_2, "_", color="red", markersize=10)
                        ax12.annotate(rf"$\overline{{Z2}}={round(Z_2)}$", (0, Z_2), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                        ax12.plot(Y2, 0, "|", color="red", markersize=10)
                        ax12.annotate(f"Y2*={round(Y2)}", (Y2, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                        #ax22 Points
                        ax22.plot(Y2, N2, "o", color="red", markersize=2)
                        ax22.plot(0, N2, "_", color="red", markersize=10)
                        ax22.plot(η2*N_2, N_2, "o", color="red", markersize=2)
                        ax22.annotate(f"N2*={round(N2)}", (0, N2), xytext=(55, 5), textcoords="offset points", fontsize=12, color="black")
                        ax22.plot(0, N_2, "_", color="red", markersize=10)
                        ax22.annotate(rf"$\overline{{N2}}={round(N_2)}$", (0, N_2), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                        ax22.plot(Y2, 0, "|", color="red", markersize=10)
                        ax22.annotate("Y2*", (Y2, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                        ax22.plot(η2*N_2, 0, "|", color="red", markersize=10)
                        ax22.annotate(rf"$\overline{{Y2}}={round(η2*N_2)}$", (η2*N_2, 0), xytext=(2, -35), textcoords="offset points", fontsize=12, color="black")

                        pass

                    #Mercato dei beni senza occupazione_Variazione
                    if Occ.lower() == "n":
                        fig, axs = plt.subplots(1, 2, num="Mercato dei beni - confronto")

                        ax11 = axs[0]
                        ax12 = axs[1]

                        Y_gr = np.linspace(0, Y*2, 1000)
                        Z_eq = Y_gr
                        Z_gr = Z_+c*(1-t)*Y_gr

                        Y_gr2 = np.linspace(0, Y2*2, 1000)
                        Z_eq2 = Y_gr2
                        Z_gr2 = Z_2+c2*(1-t2)*Y_gr2

                        ax11.set_title("Mercato dei beni(t1)", fontsize=20, family="Arial")
                        ax11.set_xlim(left=0, right=Y*2)
                        ax11.set_ylim(bottom=0, top=Y*2)

                        ax12.set_title("Mercato dei beni(t2)", fontsize=20, family="Arial")
                        ax12.set_xlim(left=0, right=Y*2)
                        ax12.set_ylim(bottom=0, top=Y*2)

                        #ax11 Setup
                        ax11.set_xlabel("Y", fontweight="bold", loc="right")
                        ax11.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
                        ax11.vlines(Y, 0, Y, linestyle="--", color="gray", alpha=0.7)

                        #ax12 Setup
                        ax12.set_xlabel("Y", fontweight="bold", loc="right")
                        ax12.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
                        ax12.vlines(Y2, 0, Y2, linestyle="--", color="gray", alpha=0.7)

                        #ax11 lines
                        ax11.plot(Y_gr, Z_eq, color="blue")
                        ax11.plot(Y_gr, Z_gr, color="blue")

                        #ax12 lines
                        ax12.plot(Y_gr2, Z_eq2, color="blue")
                        ax12.plot(Y_gr2, Z_gr2, color="blue")

                        #ax11 Points
                        ax11.plot(Y, Y, "o", color="red", markersize=2)
                        ax11.annotate("E", (Y, Y), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                        ax11.plot(0, Z_, "_", color="red", markersize=10)
                        ax11.annotate(rf"$\overline{{Z}}={round(Z_)}$", (0, Z_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                        ax11.plot(Y, 0, "|", color="red", markersize=10)
                        ax11.annotate(f"Y*={round(Y)}", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                        #ax12 Points
                        ax12.plot(Y2, Y2, "o", color="red", markersize=2)
                        ax12.annotate("E", (Y2, Y2), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                        ax12.plot(0, Z_2, "_", color="red", markersize=10)
                        ax12.annotate(rf"$\overline{{Z2}}={round(Z_2)}$", (0, Z_2), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                        ax12.plot(Y2, 0, "|", color="red", markersize=10)
                        ax12.annotate(f"Y*={round(Y2)}", (Y2, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                        pass

                    #Risparmio delle famiglie_Variazione
                    fig, axs = plt.subplots(1, 2, num="Risparmio e investimenti - confronto")

                    ax11 = axs[0]
                    ax12 = axs[1]

                    Y_gr = np.linspace(0, Yd*2, 1000)
                    SI_gr = -C_+(1-c)*Y_gr

                    Y_gr2 = np.linspace(0, Yd2*2, 1000)
                    SI_gr2 = -C_2+(1-c2)*Y_gr2

                    ax11.set_title("Risparmio e investimenti (t1)", fontsize=20, family="Arial")
                    ax11.set_xlim(left=0, right=Yd*2) 
                    ax11.set_ylim(bottom=-C_*2-100, top=Yd)

                    ax12.set_title("Risparmio e investimenti (t2)", fontsize=20, family="Arial")
                    ax12.set_xlim(left=0, right=Yd*2) 
                    ax12.set_ylim(bottom=-C_*2-100, top=Yd)

                    ax11.hlines(0, 0, Yd*2, color="black", linewidth=0.5)
                    ax12.hlines(0, 0, Yd2*2, color="black", linewidth=0.5)

                    #ax11 Setup
                    ax11.set_xlabel("Yd", fontweight="bold", loc="right")
                    ax11.set_ylabel("Sn", fontweight="bold", loc="top")
                    ax11.vlines(Yd, 0, Sn, linestyle="--", color="gray", alpha=0.7)

                    #ax12 Setup
                    ax12.set_xlabel("Yd", fontweight="bold", loc="right")
                    ax12.set_ylabel("Sn", fontweight="bold", loc="top")
                    ax12.vlines(Yd2, 0, Sn2, linestyle="--", color="gray", alpha=0.7)

                    #ax11 lines
                    ax11.plot(Y_gr, SI_gr, color="blue")
                    ax11.hlines(Sn, 0, Yd*2, color="blue")

                    #ax12 lines
                    ax12.plot(Y_gr2, SI_gr2, color="blue")
                    ax12.hlines(Sn2, 0, Yd2*2, color="blue")

                    #ax11 Points
                    ax11.plot(Yd, Sn, "o", color="red", markersize=2)
                    ax11.annotate("E", (Yd, Sn), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                    ax11.plot(0, Sn, "_", color="red", markersize=10)
                    ax11.annotate(f"Sn*={round(Sn)}", (0, Sn), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax11.plot(Yd, 0, "|", color="red", markersize=10)
                    ax11.annotate(f"Yd*={round(Yd)}", (Yd, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax11.plot(0, -C_, "_", color="red", markersize=10)
                    ax11.annotate(rf"-$\overline{{C}}={round(-C_)}$", (0, -C_), xytext=(2, -15), textcoords="offset points", fontsize=12, color="black")

                    #ax12 Points
                    ax12.plot(Yd2, Sn2, "o", color="red", markersize=2)
                    ax12.annotate("E", (Yd2, Sn2), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                    ax12.plot(0, Sn2, "_", color="red", markersize=10)
                    ax12.annotate(f"Sn2*={round(Sn2)}", (0, Sn2), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax12.plot(Yd2, 0, "|", color="red", markersize=10)
                    ax12.annotate(f"Yd2*={round(Yd2)}", (Yd2, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax12.plot(0, -C_2, "_", color="red", markersize=10)
                    ax12.annotate(rf"-$\overline{{C2}}={round(-C_2)}$", (0, -C_2), xytext=(2, -15), textcoords="offset points", fontsize=12, color="black")

                    #Bilancio dello Stato_Variazione
                    fig, axs = plt.subplots(2, 2, num="Bilancio dello Stato - confronto")

                    ax11 = axs[0, 0]
                    ax21 = axs[1, 0]
                    ax12 = axs[0, 1]
                    ax22 = axs[1, 1]

                    Y_gr = np.linspace(0, Y*2, 1000)
                    BS_gr = -(G_+TR_)+(t*Y_gr)

                    ax11.set_title("Bilancio dello Stato (t1)", fontsize=20, family="Arial")
                    ax11.set_xlim(left=0, right=Y*2)
                    ax11.set_ylim(bottom=0, top=Y*2)
                    ax21.set_xlim(left=0, right=Y*2)
                    ax21.set_ylim(bottom=-(G_+TR_)*3-100, top=Y*2)

                    Y_gr2 = np.linspace(0, Y2*2, 1000)
                    BS_gr2 = -(G_2+TR_2)+(t2*Y_gr2)
                    
                    ax12.set_title("Bilancio dello Stato (t2)", fontsize=20, family="Arial")
                    ax12.set_xlim(left=0, right=Y*2)
                    ax12.set_ylim(bottom=0, top=Y*2)
                    ax22.set_xlim(left=0, right=Y*2)
                    ax22.set_ylim(bottom=-(G_+TR_)*3-100, top=Y*2)

                    #ax11 Setup
                    ax11.set_xlabel("Y", fontweight="bold", loc="right")
                    ax11.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
                    ax11.vlines(Y, 0, Y, linestyle="--", color="gray", alpha=0.7)

                    #ax21 Setup
                    ax21.set_xlabel("Y", fontweight="bold", loc="right")
                    ax21.set_ylabel("BS", fontweight="bold", loc="top", rotation=0)
                    ax21.hlines(BS, 0, Y, linestyle="--", color="gray", alpha=0.7)
                    ax21.vlines(Y, -(G_+TR_)+(Y*t), Y*2, linestyle="--", color="gray", alpha=0.7)

                    #ax12 Setup
                    ax12.set_xlabel("Y", fontweight="bold", loc="right")
                    ax12.set_ylabel("Z", fontweight="bold", loc="top", rotation=0)
                    ax12.vlines(Y2, 0, Y2, linestyle="--", color="gray", alpha=0.7)

                    #ax22 Setup
                    ax22.set_xlabel("Y2", fontweight="bold", loc="right")
                    ax22.set_ylabel("BS2", fontweight="bold", loc="top", rotation=0)
                    ax22.hlines(BS2, 0, Y2, linestyle="--", color="gray", alpha=0.7)
                    ax22.vlines(Y2, -(G_2+TR_2)+(Y2*t2), Y2*2, linestyle="--", color="gray", alpha=0.7)

                    #ax11 lines
                    ax11.plot(Y_gr, Z_eq, color="blue")
                    ax11.plot(Y_gr, Z_gr, color="blue")

                    #ax21 lines
                    ax21.hlines(0, 0, Y*2, color="black", linewidth=0.5)
                    ax21.plot(Y_gr, BS_gr, color="blue")

                    #ax12 lines
                    ax12.plot(Y_gr2, Z_eq2, color="blue")
                    ax12.plot(Y_gr2, Z_gr2, color="blue")
                    
                    #ax22 lines
                    ax22.hlines(0, 0, Y2*2, color="black", linewidth=0.5)
                    ax22.plot(Y_gr2, BS_gr2, color="blue")

                    #ax11 Points
                    ax11.plot(Y, Y, "o", color="red", markersize=2)
                    ax11.annotate("E", (Y, Y), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                    ax11.plot(0, Z_, "_", color="red", markersize=10)
                    ax11.annotate(rf"$\overline{{Z}}={round(Z_)}$", (0, Z_), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax11.plot(Y, 0, "|", color="red", markersize=10)
                    ax11.annotate(f"Y*={round(Y)}", (Y, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                    #ax21 Points
                    ax21.plot(Y, -(G_+TR_)+(Y*t), "o", color="red", markersize=2)
                    ax21.annotate(f"BS={round(BS)}", (0, BS), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax21.plot(0, -(G_+TR_), "_", color="red", markersize=10)
                    ax21.annotate(rf"-($\overline{{G}}$+" + rf"$\overline{{TR}}$)={-(G_+TR_)}", (0, -(G_+TR_)), xytext=(5, -15), textcoords="offset points", fontsize=12, color="black")
                    ax21.plot(0, BS, "_", color="red", markersize=10)

                    #ax12 Points
                    ax12.plot(Y2, Y2, "o", color="red", markersize=2)
                    ax12.annotate("E", (Y2, Y2), xytext=(-15, -12), textcoords="offset points", fontsize=12, color="black", fontweight="bold")
                    ax12.plot(0, Z_2, "_", color="red", markersize=10)
                    ax12.annotate(rf"$\overline{{Z2}}={round(Z_2)}$", (0, Z_2), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax12.plot(Y2, 0, "|", color="red", markersize=10)
                    ax12.annotate(f"Y*={round(Y2)}", (Y2, 0), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")

                    #ax22 Points
                    ax22.plot(Y2, -(G_2+TR_2)+(Y2*t2), "o", color="red", markersize=2)
                    ax22.annotate(f"BS2={round(BS2)}", (0, BS2), xytext=(2, 5), textcoords="offset points", fontsize=12, color="black")
                    ax22.plot(0, -(G_2+TR_2), "_", color="red", markersize=10)
                    ax22.annotate(rf"-($\overline{{G2}}$+" + rf"$\overline{{TR2}}$)={-(G_2+TR_2)}", (0, -(G_2+TR_2)), xytext=(5, -15), textcoords="offset points", fontsize=12, color="black")
                    ax22.plot(0, BS2, "_", color="red", markersize=10)

                    print(colorama.Fore.RED + "CHIUDERE TUTTI I GRAFICI PER POTER CONTINUARE.") 
                    plt.show()

                if Variazione.lower() == "n":     
                    riavvia_programma()