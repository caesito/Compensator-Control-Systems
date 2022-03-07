from Controller import *

"""
 Etapa 0: Definir os requisitos de projeto do sistema para erro estatico de velocidade (Kv), Margem de Fase (MF) e Margem de Ganho (MG)
 OBS: Insira os valores como limites minimos para o sistema.
 ex: MFrequerido >= 50
     MGrequerido >= 10
     Kvrequerido >=20 
"""
MFrequerido=50
MGrequerido=10
Kvrequerido=20

# Etapa 1: Definir K = Ka, determinar valor de K que satisfaz Kv:
print('-----------------------------------')
print('Definir K = Ka, determinar valor de K que satisfaz Kv:')
K=GainK.calc_K(Kvrequerido)
# Etapa 2: Diagrama de Bode G1 = KGs. Avaliar se satisfaz os requisitos:
print('-----------------------------------')
infosys=CompensadorAvanco.margin_analytic(K)
comparacao_compensado_erro_estatico(infosys,MFrequerido,MGrequerido,Kvrequerido,K)
print('-----------------------------------')
# Etapa 3: Determinar a contribuicao de fase que o compensador proporciona (Fimax):
MFatual=infosys[1]
fimax=calc_fimax(MFrequerido,MFatual,8)
print(f'O valor de Fimax para o avanco de fase e: {fimax} graus, com uma Folga de 8 graus, e uma MF atual de: {MFatual} graus, onde a MFrdo projeto é maior ou igual a: {MFrequerido} graus')
# Etapa 4: Determinar o valor de Alfa:
alfa=calc_alfa(fimax)
print(f'O valor de Alfa para o angulo de Fimax: {fimax} graus, é: {alfa} ')
# Etapa 5: Determinar nova frequencia de cruzamento de fanho (wn):
print('-----------------------------------')
mag=frequencia_cruzamento_de_ganho(alfa)
print(f'Para um alfa igual a: {alfa}, a magnitude em dB é: {mag}')
wn, Kcu=CompensadorAvanco.bode_analytic(mag,K)
# Etapa 6: Determinar polos e zeros:
print('-----------------------------------')
zero,polo=polo_zero(alfa,wn)
print(f'Com base no angulo de Fimax e a nova frequencia de corte apresentado acima, os zeros e polos do compensador Avanço de Fase são:\nzero:{zero} \npolo:{polo}')
# Etapa 7: Determinar Kc:
print('-----------------------------------')
Kc=calc_kc(alfa,K)
print(f'O valor de Kc é: \nKc: {Kc}')
# Compensador Avanco de Fase:
print('-----------------------------------')
Gc=CompensadorAvanco.compensador_avanco(Kc,zero,polo)
print(f'A Função de Transferencia do Compensador de Avanço de Fase para os requisitos apresentados é: \n{Gc}')
print('-----------------------------------')
print('Conclusões:\n')
CompensadorAvanco.step_response()
CompensadorAvanco.step_compensator(Gc)
novoKv=GainK.calc_limt_final(zero,polo,Kc,Kvrequerido)
infosyscompensado=CompensadorAvanco.margin_analytic_compensador(Gc)
comparacao_compensador(infosyscompensado,MFrequerido,MGrequerido,Kvrequerido,novoKv)
CompensadorAvanco.create_bode(Gc,wn,mag)
print('-----------------------------------')
