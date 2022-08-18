import unittest
from DesafioBootCamp import Investiments, inv_milp, to_table


class ChallengeTests(unittest.TestCase):
    def test_cost(self):
        self.assertTrue(
            chosen_inv['Cost'].iloc[-1] <= 1000000
        )

    def test_con1(self):
        self.assertNotIn(
            'Item 4',
            chosen_inv2['Item'].tolist()
        )
        self.assertNotIn(
            'Item 0',
            chosen_inv3['Item'].tolist()
        )

    def test_con2(self):
        self.assertIn(
            'Item 3',
            chosen_inv4['Item'].tolist()
        )
        self.assertNotIn(
            ['Item 1', 'Item 3'],
            chosen_inv5['Item'].tolist()
        )


if __name__ == '__main__':
    # Teste 1 (Questão do enunciado)
    limit = 1000000

    ret = [
        410000, 330000, 140000, 250000, 320000, 320000, 90000, 190000
    ]

    cost = [
        470000, 400000, 170000, 270000, 340000, 230000, 50000, 440000
    ]

    invests = [Investiments(f'Item {i}', r, c) for i, (r, c) in enumerate(zip(cost, ret))]

    chosen_inv = inv_milp(limit, invests, verbose=True)
    chosen_inv = to_table(chosen_inv)
    print(chosen_inv)

    # Teste 2 (testando a primeira restrição: x1 + x5 <= 1)

    """O primeiro caso a ser testado será com o primeiro investimento tendo um retorno maior que o quinto,
    porém ambos possuindo custo 0, o que deverá implicar na escolha do primeiro em detrimento do quinto.
    """

    limit = 1000000

    ret = [
        410000, 330000, 140000, 250000, 320000, 320000, 90000, 190000
    ]

    cost = [
        0, 400000, 170000, 270000, 0, 230000, 50000, 440000
    ]

    invests = [Investiments(f'Item {i}', r, c) for i, (r, c) in enumerate(zip(cost, ret))]

    chosen_inv2 = inv_milp(limit, invests, verbose=True)
    chosen_inv2 = to_table(chosen_inv2)

    """O segundo caso será similar, porém o retorno do quinto investimento será maior
    """

    limit = 1000000

    ret = [
        410000, 330000, 140000, 250000, 600000, 320000, 90000, 190000
    ]

    cost = [
        0, 400000, 170000, 270000, 0, 230000, 50000, 440000
    ]

    invests = [Investiments(f'Item {i}', r, c) for i, (r, c) in enumerate(zip(cost, ret))]

    chosen_inv3 = inv_milp(limit, invests, verbose=True)
    chosen_inv3 = to_table(chosen_inv3)

    # Teste 3 (testando a segunda restrição: x2 - x4 <= 0)

    """O custo do investimento 2 será zerado, enquanto o do investimento 4 será aumentado.
        O programa deve escolher o 4 mesmo assim.
    """

    limit = 1000000

    ret = [
        410000, 330000, 140000, 250000, 320000, 320000, 90000, 190000
    ]

    cost = [
        470000, 0, 170000, 700000, 340000, 230000, 50000, 440000
    ]

    invests = [Investiments(f'Item {i}', r, c) for i, (r, c) in enumerate(zip(cost, ret))]

    chosen_inv4 = inv_milp(limit, invests, verbose=True)
    chosen_inv4 = to_table(chosen_inv4)

    """O último teste mostrará que, caso o quarto investimento não for escolhido, o segundo não será.
    Para isso, mesmo o custo do segundo sendo zerado, graças ao custo altíssimo do quarto, nenhum dos dois será escolhido.
    """

    limit = 1000000

    ret = [
        410000, 330000, 140000, 250000, 320000, 320000, 90000, 190000
    ]

    cost = [
        470000, 0, 170000, 800000, 340000, 230000, 50000, 440000
    ]

    invests = [Investiments(f'Item {i}', r, c) for i, (r, c) in enumerate(zip(cost, ret))]

    chosen_inv5 = inv_milp(limit, invests, verbose=True)
    chosen_inv5 = to_table(chosen_inv5)

    unittest.main()
