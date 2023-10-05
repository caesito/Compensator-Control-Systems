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
