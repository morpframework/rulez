
from ... import action as ra
from ... import operator as op
from ...engine import Engine
from sqlalchemy.sql import expression as sqlexp
import sqlalchemy as sa
METHOD = 'sqlalchemy'


@Engine.rulechain_compiler(method=METHOD)
def _compile_rulechain(engine, method, rulechain):
    def apply(model):
        conditions = {}
        defaults = {}
        for rule in rulechain:
            if rule.get('condition', None):
                condition = engine.compile_condition(
                    method, rule.get('condition', None))
                actions = [engine.get_action(**act) for act in rule['actions']]
                for a in actions:
                    conditions.setdefault(a.identifier, [])
                    conditions[a.identifier].append(
                        (condition(model),
                         engine.compile_action(method, a)(model)))
            else:
                actions = [engine.get_action(**act) for act in rule['actions']]
                for a in actions:
                    defaults[a.identifier] = engine.compile_action(
                        method, a)(model)
        result = []
        for k, v in conditions.items():
            d = defaults.get(k, None)
            result.append(sqlexp.case(v, else_=d).label(k))
        return result
    return apply


@Engine.action_compiler(method=METHOD, action=ra.Set)
def set(engine, method, action):
    def func(model):
        value = action.value
        if isinstance(value, op.Operator):
            value = engine.compile_operator(method, value)(model)
        return value
    return func
