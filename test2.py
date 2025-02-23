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







"""

    def calcola_costi(self, perm_comb_lista):
        costo = 0
        viaggio = 0
        for drone in perm_comb_lista:
            costo = costo + self.costoFisso
            viaggio += 1
            print("viaggio ", viaggio, "||    costo ", costo)
            for i in range(len(drone) - 1):
                nodo1 = drone[i][1]
                nodo2 = drone[i + 1][1]
                peso = self.getPeso(nodo1, nodo2)
                if peso is not None:
                    costo += peso
                else:
                    print(f"Non esiste un arco tra {nodo1} e {nodo2}")
                    return None
        print("costo TOTALE.    ", costo)
        if self.costoBest == 0 or costo < self.costoBest:
            self.costoBest = costo
            self._solBest = copy.deepcopy(perm_comb_lista)
        return costo
        
        """