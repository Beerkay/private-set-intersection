__author__ = 'Milinda Perera'

import random as pyrandom

from charm.toolbox.integergroup import random, integer

from pkenc_paillier import Paillier
from utils_poly import poly_eval_horner, poly_from_roots


class PSI2RoundPaillier(object):
    def __init__(self, sec_param):
        self.sec_param = sec_param

    def client_to_server(self, client_set):
        enc_scheme = Paillier()
        pk, sk = enc_scheme.keygen(self.sec_param)

        slient_set_mapped = [integer(a, pk['n']) for a in client_set]
        coefs = poly_from_roots(slient_set_mapped, integer(-1, pk['n']), integer(1, pk['n']))
        coef_cts = [enc_scheme.encrypt(pk, c) for c in coefs]

        out = {'pk': pk, 'coef_cts': coef_cts}
        client_state = {'pk': pk, 'sk': sk, 'client_set': client_set}

        return out, client_state

    def server_to_client(self, server_set, pk, coef_cts):
        eval_cts = [poly_eval_horner(coef_cts, e) * random(pk['n']) + e for e in server_set]

        return eval_cts

    def client_output(self, eval_cts, pk, sk, client_set):
        enc_scheme = Paillier()
        evals = [int(enc_scheme.decrypt(pk, sk, ct)) for ct in eval_cts]
        intersection = sorted(set(evals) & set(client_set))

        return intersection
