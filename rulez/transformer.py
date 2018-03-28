import dectate
import reg
import functools
import jsonpath_ng
import copy


def jsonpath_value(path, data, multi=False, default=None):
    if path == '$.':
        return data
    expr = jsonpath_ng.parse(path)
    res = expr.find(data)
    values = list([r.value for r in res])
    if multi:
        return values
    if res:
        return values[0]
    return default


class TransformerAction(dectate.Action):

    app_class_arg = True

    def __init__(self, name):
        self.name = name

    def identifier(self, app_class):
        return str([app_class, self.name])

    def perform(self, obj, app_class):
        def o(function, *args, **kwargs): return obj(*args, **kwargs)
        app_class._transform.register(name=self.name)(reg.methodify(o))


class Engine(dectate.App):

    register = dectate.directive(TransformerAction)

    def transform(self, name):
        return functools.partial(self._transform, name)

    def remap(self, rule, source, dest, **kwargs):
        rules = self._parse_rules(rule, **kwargs)
        dest = copy.deepcopy(dest)
        for p, f in rules:
            dest_pattern = jsonpath_ng.parse(p)
            # default = jsonpath_value(p, dest)
            # FIXME: get a sane default value
            default = None
            dest = dest_pattern.update(dest, f(source, dest, default))
        return dest

    def _return_value(self, v):
        return lambda s, d, dv: v

    def _source_path(self, path):
        def f(s, d, dv):
            return jsonpath_value(path, s, default=dv)
        return f

    def _apply_function(self, config,  **kwargs):
        def f(s, d, dv):
            params = {}
            for k, v in kwargs.items():
                params[k] = v
            for k, v in config.items():
                if isinstance(v, dict) and v.get('function', None):
                    v = self._apply_function(v, **kwargs)(s, d, dv)
                elif v.startswith('$.'):
                    v = jsonpath_value(v, s, default=dv)
                params[k] = v
            return self._transform(**params)
        return f

    def _parse_rules(self, rule, **kwargs):
        res = []
        for k, v in rule.items():
            if isinstance(v, dict) and v.get('function', None):
                res.append((k, self._apply_function(v, **kwargs)))
            elif isinstance(v, int) or isinstance(v, float):
                res.append((k, self._return_value(v)))
            elif v.startswith('$.'):
                res.append((k, self._source_path(v)))
            else:
                res.append((k, self._return_value(v)))
        return res

    @reg.dispatch_method(
        reg.match_key('name',
                      lambda self, function, *args, **kwargs: function))
    def _transform(self, function, *args, **kwargs):
        raise NotImplementedError('Transform function %s' % function)
