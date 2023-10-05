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
