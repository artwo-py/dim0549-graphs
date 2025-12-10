def swap(grafo):
    """"""


def two_opt(grafo, ciclo):
    """Busca melhoria de um ciclo usando a heurística 2-opt."""
    melhoria = True
    melhor_ciclo = ciclo[:]

    def custo_total(c):
        soma = 0
        for i in range(len(c) - 1):
            soma += grafo.get_peso(c[i], c[i+1])
        return soma

    melhor_custo = custo_total(melhor_ciclo)

    while melhoria:
        melhoria = False
        for i in range(1, len(melhor_ciclo) - 2):
            for j in range(i+1, len(melhor_ciclo) - 1):

                novo_ciclo = (
                    melhor_ciclo[:i] +
                    list(reversed(melhor_ciclo[i:j])) +
                    melhor_ciclo[j:]
                )

                novo_custo = custo_total(novo_ciclo)
                if novo_custo < melhor_custo:
                    melhor_ciclo = novo_ciclo
                    melhor_custo = novo_custo
                    melhoria = True
                    break 
            if melhoria:
                break

    return melhor_ciclo, melhor_custo
