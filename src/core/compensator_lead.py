from sympy import *
import numpy as np
import control as clt
import matplotlib.pyplot as plt
import math
from control.matlab import *
from scipy import signal
from model import SystemControl, FunctionSystem

class CompensadorAvanco(SystemControl):
    s=clt.tf('s')

    @classmethod
    def compensador_avanco(cls,Kc,zero,polo):
        Gc=float(Kc)*((cls.s + zero)/(cls.s + polo))
        return Gc

    @classmethod
    def create_bode(cls,G,wc,Kcu):
        system=G*cls.sys
        print(f'A nova Função de Transferencia apos aplicar o Compensador é:\n {system}')
        clt.bode(cls.sys)
        plt.tight_layout()
        ax1, ax2 = plt.gcf().axes
        plt.sca(ax1)
        plt.title('Sem compensador')
        plt.figure()
        clt.bode(system)
        ax1, ax2 = plt.gcf().axes
        plt.sca(ax1)
        plt.title('Com Compensador Avanço de Fase')
        plt.figure()
        clt.bode(cls.sys)
        clt.bode(system)
        ax1, ax2 = plt.gcf().axes
        plt.sca(ax1)
        plt.title('Sistema sem Compensador x Sistema com Compensador Avanço de Fase')
        plt.legend(['Sem compensador', 'Com compensador'])
        plt.show()


    @classmethod
    def bode_analytic(cls,wn,K):
        signalsys = signal.TransferFunction([float(K)*cls.num], cls.den)
        w, mag, phase = signalsys.bode()
        wc = np.interp(wn, np.flipud(mag), np.flipud(w))
        Kcu = np.interp(wc, mag, w)
        print(f'A Frequencia de corte para uma magnitude em dB de: {wn}, é Wn = ', wc, ' rad/sec')
        W=np.logspace(-1,1)
        clt.bode_plot(float(K)*cls.sys,W)
        plt.show()
        return (wc,Kcu)

    @classmethod
    def margin_analytic(cls,K):
        system=float(K)*cls.sys
        gm, pm, wcg,wcp=clt.margin(system)
        infosys = list()
        infosys.append(gm)
        infosys.append(pm)
        infosys.append(wcg)
        infosys.append(wcp)
        print(f'MG:{gm} \nMF:{pm} \nWCG:{wcg} \nWCP:{wcp}')
        return infosys

    @classmethod
    def margin_analytic_compensador(cls,Gc):
        system=Gc*cls.sys
        gm, pm, wcg,wcp=clt.margin(system)
        infosys = list()
        infosys.append(gm)
        infosys.append(pm)
        print(f'MG:{gm}\nMF:{pm}')
        return infosys

    @classmethod
    def step_response(cls):
        system=cls.sys
        feedsys=feedback(system,1)
        t = np.arange(0, 8,0.001)
        y,t=step(feedsys,t)
        plt.title('Sem compensador')
        plt.plot(t,y)
        plt.show()

    @classmethod
    def step_compensator(cls,Gc):
        system = cls.sys*Gc
        feedsys= feedback(cls.sys,1)
        feedsyscomp= feedback(system, 1)
        t = np.arange(0, 8, 0.001)
        y1, t1 = step(feedsyscomp, t)
        y2, t2 = step(feedsys, t)
        plt.plot(t1, y1,t2,y2)
        plt.legend(['Com compensador', 'Sem compensador'])
        plt.grid()
        plt.title('Sem compensador x Com Compensador')
        plt.show()
