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

from grako.parsing import graken, Parser
from grako.util import re, RE_FLAGS, generic_main  # noqa


__version__ = (2016, 4, 25, 13, 48, 23, 0)

__all__ = [
    'GrakoBootstrapParser',
    'GrakoBootstrapSemantics',
    'main'
]

KEYWORDS = set([])


class GrakoBootstrapParser(Parser):
    def __init__(self,
                 whitespace=None,
                 nameguard=None,
                 comments_re='\\(\\*((?:.|\\n)*?)\\*\\)',
                 eol_comments_re='#([^\\n]*?)$',
                 ignorecase=None,
                 left_recursion=True,
                 keywords=KEYWORDS,
                 **kwargs):
        super(GrakoBootstrapParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            left_recursion=left_recursion,
            keywords=keywords,
            **kwargs
        )

    @graken()
    def _start_(self):
        self._grammar_()

    @graken('Grammar')
    def _grammar_(self):
        self._constant('GRAKO')
        self.name_last_node('title')

        def block2():
            self._directive_()
        self._closure(block2)
        self.name_last_node('directives')
        self._keywords_()
        self.name_last_node('keywords')

        def block5():
            self._rule_()
        self._positive_closure(block5)
        self.name_last_node('rules')
        self._check_eof()

        self.ast._define(
            ['title', 'directives', 'keywords', 'rules'],
            []
        )

    @graken()
    def _directive_(self):
        self._token('@@')
        with self._ifnot():
            self._token('keyword')
        self._cut()
        with self._group():
            with self._choice():
                with self._option():
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._token('comments')
                            with self._option():
                                self._token('eol_comments')
                            with self._option():
                                self._token('whitespace')
                            self._error('expecting one of: comments eol_comments whitespace')
                    self.name_last_node('name')
                    self._cut()
                    self._cut()
                    self._token('::')
                    self._cut()
                    self._regex_()
                    self.name_last_node('value')
                with self._option():
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._token('nameguard')
                            with self._option():
                                self._token('ignorecase')
                            with self._option():
                                self._token('left_recursion')
                            self._error('expecting one of: ignorecase left_recursion nameguard')
                    self.name_last_node('name')
                    self._cut()
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._token('::')
                                self._cut()
                                self._boolean_()
                                self.name_last_node('value')
                            with self._option():
                                self._constant('True')
                                self.name_last_node('value')
                            self._error('no available options')
                with self._option():
                    with self._group():
                        self._token('grammar')
                    self.name_last_node('name')
                    self._cut()
                    self._token('::')
                    self._cut()
                    self._word_()
                    self.name_last_node('value')
                self._error('no available options')

        self.ast._define(
            ['name', 'value'],
            []
        )

    @graken()
    def _keywords_(self):

        def block0():
            self._token('@@keyword')
            self._cut()
            self._token('::')
            self._cut()

            def block1():
                self._literal_()
                self.add_last_node_to_name('@')
                with self._ifnot():
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._token(':')
                            with self._option():
                                self._token('=')
                            self._error('expecting one of: : =')
            self._closure(block1)
        self._closure(block0)

    @graken()
    def _paramdef_(self):
        with self._choice():
            with self._option():
                self._token('::')
                self._cut()
                self._params_only_()
                self.name_last_node('params')
            with self._option():
                self._token('(')
                self._cut()
                with self._group():
                    with self._choice():
                        with self._option():
                            self._kwparams_()
                            self.name_last_node('kwparams')
                        with self._option():
                            self._params_()
                            self.name_last_node('params')
                            self._token(',')
                            self._cut()
                            self._kwparams_()
                            self.name_last_node('kwparams')
                        with self._option():
                            self._params_()
                            self.name_last_node('params')
                        self._error('no available options')
                self._token(')')
            self._error('no available options')

        self.ast._define(
            ['params', 'kwparams'],
            []
        )

    @graken('Rule')
    def _rule_(self):

        def block1():
            self._decorator_()
        self._closure(block1)
        self.name_last_node('decorators')
        self._name_()
        self.name_last_node('name')
        self._cut()
        with self._optional():
            with self._choice():
                with self._option():
                    self._token('::')
                    self._cut()
                    self._params_only_()
                    self.name_last_node('params')
                with self._option():
                    self._token('(')
                    self._cut()
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._kwparams_()
                                self.name_last_node('kwparams')
                            with self._option():
                                self._params_()
                                self.name_last_node('params')
                                self._token(',')
                                self._cut()
                                self._kwparams_()
                                self.name_last_node('kwparams')
                            with self._option():
                                self._params_()
                                self.name_last_node('params')
                            self._error('no available options')
                    self._token(')')
                self._error('no available options')
        with self._optional():
            self._token('<')
            self._cut()
            self._known_name_()
            self.name_last_node('base')
        self._token('=')
        self._cut()
        self._expre_()
        self.name_last_node('exp')
        self._token(';')
        self._cut()

        self.ast._define(
            ['decorators', 'name', 'params', 'kwparams', 'base', 'exp'],
            []
        )

    @graken()
    def _decorator_(self):
        self._token('@')
        self._cut()
        with self._group():
            with self._choice():
                with self._option():
                    self._token('override')
                with self._option():
                    self._token('name')
                self._error('expecting one of: name override')
        self.name_last_node('@')

    @graken()
    def _params_(self):
        self._literal_()
        self.add_last_node_to_name('@')

        def block1():
            self._token(',')
            self._literal_()
            self.add_last_node_to_name('@')
            with self._ifnot():
                self._token('=')
            self._cut()
        self._closure(block1)

    @graken()
    def _params_only_(self):

        def sep0():
            self._token(',')

        def block0():
            self._literal_()
        self._positive_closure(block0, prefix=sep0)

    @graken()
    def _kwparams_(self):

        def sep0():
            self._token(',')

        def block0():
            self._pair_()
        self._positive_closure(block0, prefix=sep0)

    @graken()
    def _pair_(self):
        self._word_()
        self.add_last_node_to_name('@')
        self._token('=')
        self._cut()
        self._literal_()
        self.add_last_node_to_name('@')

    @graken()
    def _expre_(self):
        with self._choice():
            with self._option():
                self._choice_()
            with self._option():
                self._sequence_()
            self._error('no available options')

    @graken('Choice')
    def _choice_(self):
        self._sequence_()
        self.add_last_node_to_name('@')

        def block1():
            self._token('|')
            self._cut()
            self._sequence_()
            self.add_last_node_to_name('@')
        self._positive_closure(block1)

    @graken('Sequence')
    def _sequence_(self):

        def block1():
            self._element_()
        self._positive_closure(block1)
        self.name_last_node('sequence')

        self.ast._define(
            ['sequence'],
            []
        )

    @graken()
    def _element_(self):
        with self._choice():
            with self._option():
                self._rule_include_()
            with self._option():
                self._named_()
            with self._option():
                self._override_()
            with self._option():
                self._term_()
            self._error('no available options')

    @graken('RuleInclude')
    def _rule_include_(self):
        self._token('>')
        self._cut()
        self._known_name_()
        self.name_last_node('@')

    @graken()
    def _named_(self):
        with self._choice():
            with self._option():
                self._named_list_()
            with self._option():
                self._named_single_()
            self._error('no available options')

    @graken('NamedList')
    def _named_list_(self):
        self._name_()
        self.name_last_node('name')
        self._token('+:')
        self._cut()
        self._element_()
        self.name_last_node('exp')

        self.ast._define(
            ['name', 'exp'],
            []
        )

    @graken('Named')
    def _named_single_(self):
        self._name_()
        self.name_last_node('name')
        self._token(':')
        self._cut()
        self._element_()
        self.name_last_node('exp')

        self.ast._define(
            ['name', 'exp'],
            []
        )

    @graken()
    def _override_(self):
        with self._choice():
            with self._option():
                self._override_list_()
            with self._option():
                self._override_single_()
            with self._option():
                self._override_single_deprecated_()
            self._error('no available options')

    @graken('OverrideList')
    def _override_list_(self):
        self._token('@+:')
        self._cut()
        self._element_()
        self.name_last_node('@')

    @graken('Override')
    def _override_single_(self):
        self._token('@:')
        self._cut()
        self._element_()
        self.name_last_node('@')

    @graken('Override')
    def _override_single_deprecated_(self):
        self._token('@')
        self._cut()
        self._element_()
        self.name_last_node('@')

    @graken()
    def _term_(self):
        with self._choice():
            with self._option():
                self._void_()
            with self._option():
                self._join_()
            with self._option():
                self._group_()
            with self._option():
                self._empty_closure_()
            with self._option():
                self._positive_closure_()
            with self._option():
                self._closure_()
            with self._option():
                self._optional_()
            with self._option():
                self._special_()
            with self._option():
                self._kif_()
            with self._option():
                self._knot_()
            with self._option():
                self._atom_()
            self._error('no available options')

    @graken('Group')
    def _group_(self):
        self._token('(')
        self._cut()
        self._expre_()
        self.name_last_node('exp')
        self._token(')')
        self._cut()

        self.ast._define(
            ['exp'],
            []
        )

    @graken('Join')
    def _join_(self):
        self._separator_()
        self.name_last_node('sep')
        self._token('.')
        self._cut()
        self._token('{')
        self._cut()
        self._expre_()
        self.name_last_node('exp')
        self._token('}')
        self._cut()
        with self._optional():
            self._token('+')
            self._cut()

        self.ast._define(
            ['sep', 'exp'],
            []
        )

    @graken()
    def _separator_(self):
        with self._choice():
            with self._option():
                self._group_()
            with self._option():
                self._token_()
            with self._option():
                self._constant_()
            with self._option():
                self._pattern_()
            self._error('no available options')

    @graken('PositiveClosure')
    def _positive_closure_(self):
        self._token('{')
        self._expre_()
        self.name_last_node('@')
        self._token('}')
        with self._group():
            with self._choice():
                with self._option():
                    self._token('-')
                with self._option():
                    self._token('+')
                self._error('expecting one of: + -')
        self._cut()

    @graken('Closure')
    def _closure_(self):
        self._token('{')
        self._expre_()
        self.name_last_node('@')
        self._token('}')
        with self._optional():
            self._token('*')
        self._cut()

    @graken('EmptyClosure')
    def _empty_closure_(self):
        self._token('{')
        pass
        self.name_last_node('@')
        self._token('}')

    @graken('Optional')
    def _optional_(self):
        self._token('[')
        self._cut()
        self._expre_()
        self.name_last_node('@')
        self._token(']')
        self._cut()

    @graken('Special')
    def _special_(self):
        self._token('?(')
        self._cut()
        self._pattern(r'.*?(?!\)\?)')
        self.name_last_node('@')
        self._token(')?')
        self._cut()

    @graken('Lookahead')
    def _kif_(self):
        self._token('&')
        self._cut()
        self._term_()
        self.name_last_node('@')

    @graken('NegativeLookahead')
    def _knot_(self):
        self._token('!')
        self._cut()
        self._term_()
        self.name_last_node('@')

    @graken()
    def _atom_(self):
        with self._choice():
            with self._option():
                self._cut_()
            with self._option():
                self._cut_deprecated_()
            with self._option():
                self._token_()
            with self._option():
                self._constant_()
            with self._option():
                self._call_()
            with self._option():
                self._pattern_()
            with self._option():
                self._eof_()
            self._error('no available options')

    @graken('RuleRef')
    def _call_(self):
        self._word_()

    @graken('Void')
    def _void_(self):
        self._token('()')
        self._cut()

    @graken('Cut')
    def _cut_(self):
        self._token('~')
        self._cut()

    @graken('Cut')
    def _cut_deprecated_(self):
        self._token('>>')
        self._cut()

    @graken()
    def _known_name_(self):
        self._name_()
        self._cut()

    @graken()
    def _name_(self):
        self._word_()

    @graken('Constant')
    def _constant_(self):
        self._pattern(r'`')
        self._cut()
        self._literal_()
        self.name_last_node('@')
        self._pattern(r'`')

    @graken('Token')
    def _token_(self):
        self._string_()

    @graken()
    def _literal_(self):
        with self._choice():
            with self._option():
                self._string_()
            with self._option():
                self._word_()
            with self._option():
                self._hex_()
            with self._option():
                self._float_()
            with self._option():
                self._int_()
            self._error('no available options')

    @graken()
    def _string_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._token('"')
                    self._cut()
                    self._pattern(r'([^"\n]|\\"|\\\\)*')
                    self.name_last_node('@')
                    self._token('"')
                with self._option():
                    self._token("'")
                    self._cut()
                    self._pattern(r"([^'\n]|\\'|\\\\)*")
                    self.name_last_node('@')
                    self._token("'")
                self._error('expecting one of: " \'')
        self._cut()

    @graken()
    def _hex_(self):
        self._pattern(r'0[xX](\d|[a-fA-F])+')

    @graken()
    def _float_(self):
        with self._choice():
            with self._option():
                self._pattern(r'[-+]?\d+\.(?:\d*)?(?:[Ee][-+]?\d+)?')
            with self._option():
                self._pattern(r'[-+]?\d*\.\d+(?:[Ee][-+]?\d+)?')
            self._error('expecting one of: [-+]?\\d*\\.\\d+(?:[Ee][-+]?\\d+)? [-+]?\\d+\\.(?:\\d*)?(?:[Ee][-+]?\\d+)?')

    @graken()
    def _int_(self):
        self._pattern(r'[-+]?\d+')

    @graken()
    def _word_(self):
        self._pattern(r'(?!\d)\w+')

    @graken('Pattern')
    def _pattern_(self):
        self._regex_()

    @graken()
    def _regex_(self):
        with self._choice():
            with self._option():
                self._token('?/')
                self._cut()
                self._pattern(r'(.|\n)+?(?=/\?)')
                self.name_last_node('@')
                self._pattern(r'/\?+')
                self._cut()
            with self._option():
                self._token('/')
                self._cut()
                self._pattern(r'(.|\n)+?(?=/)')
                self.name_last_node('@')
                self._token('/')
                self._cut()
            self._error('expecting one of: / ?/')

    @graken()
    def _boolean_(self):
        with self._choice():
            with self._option():
                self._token('True')
            with self._option():
                self._token('False')
            self._error('expecting one of: False True')

    @graken('EOF')
    def _eof_(self):
        self._token('$')
        self._cut()


class GrakoBootstrapSemantics(object):
    def start(self, ast):
        return ast

    def grammar(self, ast):
        return ast

    def directive(self, ast):
        return ast

    def keywords(self, ast):
        return ast

    def paramdef(self, ast):
        return ast

    def rule(self, ast):
        return ast

    def decorator(self, ast):
        return ast

    def params(self, ast):
        return ast

    def params_only(self, ast):
        return ast

    def kwparams(self, ast):
        return ast

    def pair(self, ast):
        return ast

    def expre(self, ast):
        return ast

    def choice(self, ast):
        return ast

    def sequence(self, ast):
        return ast

    def element(self, ast):
        return ast

    def rule_include(self, ast):
        return ast

    def named(self, ast):
        return ast

    def named_list(self, ast):
        return ast

    def named_single(self, ast):
        return ast

    def override(self, ast):
        return ast

    def override_list(self, ast):
        return ast

    def override_single(self, ast):
        return ast

    def override_single_deprecated(self, ast):
        return ast

    def term(self, ast):
        return ast

    def group(self, ast):
        return ast

    def join(self, ast):
        return ast

    def separator(self, ast):
        return ast

    def positive_closure(self, ast):
        return ast

    def closure(self, ast):
        return ast

    def empty_closure(self, ast):
        return ast

    def optional(self, ast):
        return ast

    def special(self, ast):
        return ast

    def kif(self, ast):
        return ast

    def knot(self, ast):
        return ast

    def atom(self, ast):
        return ast

    def call(self, ast):
        return ast

    def void(self, ast):
        return ast

    def cut(self, ast):
        return ast

    def cut_deprecated(self, ast):
        return ast

    def known_name(self, ast):
        return ast

    def name(self, ast):
        return ast

    def constant(self, ast):
        return ast

    def token(self, ast):
        return ast

    def literal(self, ast):
        return ast

    def string(self, ast):
        return ast

    def hex(self, ast):
        return ast

    def float(self, ast):
        return ast

    def int(self, ast):
        return ast

    def word(self, ast):
        return ast

    def pattern(self, ast):
        return ast

    def regex(self, ast):
        return ast

    def boolean(self, ast):
        return ast

    def eof(self, ast):
        return ast


def main(
        filename,
        startrule,
        trace=False,
        whitespace=None,
        nameguard=None,
        comments_re='\\(\\*((?:.|\\n)*?)\\*\\)',
        eol_comments_re='#([^\\n]*?)$',
        ignorecase=None,
        left_recursion=True,
        **kwargs):

    with open(filename) as f:
        text = f.read()
    whitespace = whitespace or None
    parser = GrakoBootstrapParser(parseinfo=False)
    ast = parser.parse(
        text,
        startrule,
        filename=filename,
        trace=trace,
        whitespace=whitespace,
        nameguard=nameguard,
        ignorecase=ignorecase,
        **kwargs)
    return ast

if __name__ == '__main__':
    import json
    ast = generic_main(main, GrakoBootstrapParser, name='GrakoBootstrap')
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(ast, indent=2))
    print()
