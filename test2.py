from itertools import permutations, product as permutations_product
import copy



def permutazioni(lista_di_liste):
    permutazioni_sottoliste = [list(permutations(sottolista)) for sottolista in
                               lista_di_liste]  # lista PERMUTAZIONI della combinazione N
    h = 0
    for perm_comb in permutations_product(*permutazioni_sottoliste):
        h += 1
        perm_comb_lista = [list(sublist) for sublist in
                           perm_comb]
        #print(f'permutazione {h} : {perm_comb_lista}')
        #self.calcola_costi(perm_comb_lista)


def trova_combinazioni(listConsegne, assegnamento_corrente, risultato):
        if not listConsegne:
            risultato.append(assegnamento_corrente.copy())
            print(risultato[-1])
            #self.checkDimensione(risultato[-1]):
            permutazioni(risultato[-1])                                                       #ATTIVAMI £ DISATTIVAMI
            return
        prodotto = listConsegne[0]
        for camion in assegnamento_corrente:
            camion.append(prodotto)
            trova_combinazioni(listConsegne[1:], assegnamento_corrente, risultato)
            camion.pop()
        nuovo_camion = [prodotto]
        assegnamento_corrente.append(nuovo_camion)
        trova_combinazioni(listConsegne[1:], assegnamento_corrente, risultato)
        assegnamento_corrente.pop()



if __name__ == "__main__":
    lista = [1, 2, 3, 4]
    trova_combinazioni(lista, [], [])



