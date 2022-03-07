from sympy import *
import numpy as np
import control as clt
import matplotlib.pyplot as plt
import math
from control.matlab import *
from scipy import signal
from model import SystemControl, FunctionSystem

class GainK(FunctionSystem):

    @classmethod
    def calc_K(cls,Kv):
        func= cls.s*cls.Gs
        limite=limit(func,cls.s,0)
        K=Kv/limite
        print('O valor do limite:', limite, '\nA funcao Gs:', cls.Gs, '\nA funcao a ser calulado o limite:', func,'\no valor de K:', K)
        return K

    @classmethod
    def calc_limt_final(cls,zero,polo,Kc,Kvrequerido):
        compensador=((float(Kc)*zero)/polo)
        func=cls.s*compensador*cls.Gs
        limite=limit(func,cls.s,0)
        print('-*-*-*-')
        if Kvrequerido== limite:
            print(f'O Erro estático de Velocidade Kv cumpre com o requisito o valor de Kv calculado é é: {int(limite)}, e o valor do Kv requerido é: {Kvrequerido}')
        else:
            print(f'O Erro estático de Velocidade Kv não cumpre com o requisito o valor de Kv calculado é é: {int(limite)}, e o valor do Kv requerido é: {Kvrequerido}')
        print('-*-*-*-')
        return int(limite)


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

def comparacao_compensado_erro_estatico(lista,MF,MG,Kv,K):
    requisito = np.array([MG,MF])
    comparando = False
    print(f'Apos o ajuste do ganho K em K= {K} p/ satisfazer o erro estático de velocidade (Kv) em Kv= {Kv}, os demais requisitos foram:')
    print(f'a MF é: {lista[1]}, e a MG é: {lista[0]}')
    print('-*-*-*-')
    if requisito[1] <= lista[1]:
        print('a Margem de Fase cumpre com o requisito')
    else:
        print('a Margem de Fase não cumpre com o requisito')
    print('-*-*-*-')
    if requisito[0] <= lista[0]:
        print('a Margem de Ganho cumpre com o requisito')
    else:
        print('a Margem de Ganho não cumpre com o requisito')
    print('-*-*-*-')
    if requisito[0] <= lista[0] and requisito[1] <= lista[1]:
        comparando = True
        print('apenas com o ajuste de ganho K é possivel satisfazer os requisistos')
    else:
        print('Apenas com o ajuste de ganho K não foi possivel atender todos os requisitos, desta forma vamos aplicar um compensador avanço de fase:')

def comparacao_compensador(lista, MF, MG, Kvrequerido, Kvnovo):
    requisito = np.array([MG, MF])
    comparando = False
    print(f'Apos a aplicação do compensador os requisitos são:')
    print('-*-*-*-')
    if Kvrequerido==Kvnovo:
        print('o erro estático de velocidade cumpre com os requisitos')
        print(f'Kv encontrado:{Kvnovo}\nKv requisito maior ou igual a:{Kvrequerido}')
    else:
        print('o erro estático de velocidade não cumpre com os requisitos')
        print(f'Kv encontrado:{Kvnovo}\nKv requisito maior ou igual a:{Kvrequerido}')
    print('-*-*-*-')
    if requisito[1] <= lista[1]:
        print('a Margem de Fase cumpre com o requisito')
        print(f'MF encontrado:{lista[1]}\nMF requisito maior ou igual a:{requisito[1]}')
    else:
        print('a Margem de Fase não cumpre com o requisito')
        print(f'MF encontrado:{lista[1]}\nMF requisito maior ou igual a:{requisito[1]}')
    print('-*-*-*-')
    if requisito[0] <= lista[0]:
        print('a Margem de Ganho cumpre com o requisito')
        print(f'MG encontrado:{lista[0]}\nMG requisito maior ou igual a:{requisito[0]}')
    else:
        print('a Margem de Ganho não cumpre com o requisito')
        print(f'MG encontrado:{lista[0]}\nMG requisito maior ou igual a:{requisito[0]}')
    print('-*-*-*-')
    if requisito[0] <= lista[0] and requisito[1] <= lista[1] and Kvnovo==Kvrequerido:
        comparando = True
        print('todos requisitos foram satisfeitos, o Compensador Avanço de Fase foi suficiente para compensar o sistema')
    else:
        print('alguns requisitos nao foram atendidos, talvez seja melhor utilizar outro compensador como o Atraso de Fase,ou Avanço-Atraso de fase')
    print('-*-*-*-')

def calc_fimax(MFrequerido, MFatual, folga):
    fimax= MFrequerido-MFatual+folga
    return fimax

def calc_alfa(fimax):
    radianofimax=0.0174533*fimax
    fimaxrad = math.sin(radianofimax)
    alfa=(1 - fimaxrad)/(fimaxrad + 1)
    return alfa

def frequencia_cruzamento_de_ganho(alfa):
    G1= -20*(math.log10((1/(math.sqrt(alfa)))))
    return G1

def polo_zero(alfa,wn):
    zero=wn*math.sqrt(alfa)
    polo=wn/math.sqrt(alfa)
    return (zero,polo)

def calc_kc(alfa,k):
    Kc=k/alfa
    return Kc

