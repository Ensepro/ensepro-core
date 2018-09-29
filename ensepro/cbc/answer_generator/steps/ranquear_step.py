# -*- coding: utf-8 -*-
"""
@project ensepro
@since 08/06/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import json
from ensepro import save_as_json
from ensepro.cbc.answer_generator import helper


def ranquear_step_value(params, step, steps, log=False):
    helper.init_helper(params["helper"])

    if log:
        print("ordenando(ranquenado) triplas... ", end="")
    # dist , TRs, var
    # values_sorted = sorted(params["values"], key=lambda x: (x[-1], -x[-2], x[-3]))
    # TRs, dist, var
    values_sorted = sorted(params["values"], key=lambda x: (-x[-2], x[-1], x[-3]))

    if log:
        print("done.")
    values = {}
    values["helper"] = helper.save_helper()
    values["values"] = values_sorted
    save_as_json(values, "queries_renqueadas.json")

    if steps.get(step, None):
        return steps[step][0](values, steps[step][1], steps, log=log)
    else:
        return values_sorted


def ranquear_step(params, step, steps, log=False):
    with open(params[0], encoding="UTF-8", mode="r") as f:
        value = json.load(f)

    return ranquear_step_value(value, step, steps, log=log)
