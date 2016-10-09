# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from datetime import datetime
from collections import namedtuple as NT  # noqa: N812

from grako.util import (
    compress_seq,
    indent,
    re,
    safe_name,
)
from grako.objectmodel import Node
from grako.objectmodel import BASE_CLASS_TOKEN
from grako.exceptions import CodegenError
from grako.rendering import Renderer
from grako.codegen.cgbase import ModelRenderer, CodeGenerator


NODE_NAME_PATTERN = '(?!\d)\w+(' + BASE_CLASS_TOKEN + '(?!\d)\w+)*'


_TypeSpec = NT('TypeSpec', ['class_name', 'base'])


def codegen(model):
    return ObjectModelCodeGenerator().render(model)


def _has_node_name(rule):
    if not rule.params:
        return None

    typespec = rule.params[0]
    if not re.match(NODE_NAME_PATTERN, typespec):
        return None
    if not typespec[0].isupper():
        return None
    return typespec


def _typespec(rule, default_base=True):
    if not _has_node_name(rule):
        return _TypeSpec(None, None)

    spec = rule.params[0].split(BASE_CLASS_TOKEN)
    class_name = safe_name(spec[0])
    base = None
    bases = spec[1:]
    if bases:
        base = safe_name(bases[0])
    elif default_base:
        base = 'ModelBase'
    return _TypeSpec(class_name, base)


class BaseClassRenderer(Renderer):
    def __init__(self, class_name):
        self.class_name = class_name

    template = '''
        class {class_name}(ModelBase):
            pass
        '''


class ObjectModelCodeGenerator(CodeGenerator):
    def _find_renderer_class(self, item):
        if not isinstance(item, Node):
            return None

        name = item.__class__.__name__
        renderer = globals().get(name, None)
        if not renderer or not issubclass(renderer, ModelRenderer):
            raise CodegenError('Renderer for %s not found' % name)
        return renderer


class Rule(ModelRenderer):
    def render_fields(self, fields):
        defs = [safe_name(d) for d, l in compress_seq(self.defines())]
        defs = list(sorted(set(defs)))

        kwargs = '\n'.join('%s=None, ' % d for d in defs)
        params = '\n'.join('%s=%s,' % (d, d) for d in defs)
        if params:
            params = '\n*_args_,\n' + params + '\n**_kwargs_\n'
            params = indent(params, 3)
            params = params + '\n' + indent(')', 2)

            kwargs = '\n' + indent(kwargs + '\n**_kwargs_', indent=17, multiplier=1)
        else:
            kwargs = ' **_kwargs_'
            params = '*_args_, **_kwargs_)'

        spec = _typespec(self.node)

        fields.update(
            class_name=spec.class_name,
            base=spec.base,
            _kwargs_=kwargs,
            params=params,
        )

    template = '''
        class {class_name}({base}):
            def __init__(self, *_args_,{_kwargs_}):
                super({class_name}, self).__init__({params}\
        '''


class Grammar(ModelRenderer):
    def render_fields(self, fields):
        bases = {_typespec(rule, False).base for rule in self.node.rules}
        base_class_declarations = [
            BaseClassRenderer(base).render()
            for base in bases
            if base is not None
        ]

        model_rules = [
            rule
            for rule in self.node.rules
            if _has_node_name(rule)
        ]

        model_class_declarations = [
            self.get_renderer(rule).render()
            for rule in model_rules
        ]

        base_class_declarations = '\n\n\n'.join(base_class_declarations)
        if base_class_declarations:
            base_class_declarations += '\n\n'
        model_class_declarations = '\n\n\n'.join(model_class_declarations)

        version = datetime.now().strftime('%Y.%m.%d.%H')

        fields.update(
            base_class_declarations=base_class_declarations,
            model_class_declarations=model_class_declarations,
            version=version,
        )

    template = '''\
                #!/usr/bin/env python
                # -*- coding: utf-8 -*-

                # CAVEAT UTILITOR
                #
                # This file was automatically generated by Grako.
                #
                #    https://pypi.python.org/pypi/grako/
                #
                # Any changes you make to it will be overwritten the next time
                # the file is generated.

                from __future__ import print_function, division, absolute_import, unicode_literals

                from grako.objectmodel import Node
                from grako.semantics import ModelBuilderSemantics


                class {name}ModelBuilderSemantics(ModelBuilderSemantics):
                    def __init__(self):
                        types = [
                            t for t in globals().values()
                            if type(t) is type and issubclass(t, ModelBase)
                        ]
                        super({name}ModelBuilderSemantics, self).__init__(types=types)


                class ModelBase(Node):
                    pass


                {base_class_declarations}{model_class_declarations}
                '''
