from ..documents.constants import pubkey_regex
from ..documents.constants import block_hash_regex as hash_regex
from pypeg2 import *


class Pubkey(Symbol):
    regex = re.compile(pubkey_regex)


class Hash(Symbol):
    regex = re.compile(hash_regex)


class SIG(str):
    grammar = "SIG(", attr('pubkey', Pubkey), ")"

    def compose(self, parser, grammar=None, attr_of=None):
        return "SIG({0})".format(self.pubkey)


class XHX(str):
    grammar = "XHX(", attr('sha_hash', Hash), ")"

    def compose(self, parser, grammar=None, attr_of=None):
        return "XHX({0})".format(self.sha_hash)


class Operator(Keyword):
    grammar = Enum(K("AND"), K("OR"))

    def compose(self, parser, grammar=None, attr_of=None):
        return "{0}".format(self.name)


class Condition(str):
    def compose(self, parser, grammar=None, attr_of=None):
        if type(self.left) is Condition:
            left = "({0})".format(parser.compose(self.left, grammar=grammar, attr_of=attr_of))
        else:
            left = parser.compose(self.left, grammar=grammar, attr_of=attr_of)

        if getattr(self, 'op', None):

            if type(self.right) is Condition:
                right = "({0})".format(parser.compose(self.right, grammar=grammar, attr_of=attr_of))
            else:
                right = parser.compose(self.right, grammar=grammar, attr_of=attr_of)
            op = parser.compose(self.op, grammar=grammar, attr_of=attr_of)
            result = "{0} {1} {2}".format(left, op, right)
        else:
            result = left
        return result

Condition.grammar = contiguous(attr('left', [SIG, XHX, ('(', Condition, ')')]),
                     maybe_some(whitespace, attr('op', Operator), whitespace,
                               attr('right', [SIG, XHX, ('(', Condition, ')')])))
