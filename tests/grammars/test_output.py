from duniterpy.grammars import output
import unittest
import pypeg2


class Test_OutputGrammar(unittest.TestCase):
    def test_sig(self):
        condition = "SIG(HgTTJLAQ5sqfknMq7yLPZbehtuLSsKj9CxWN7k8QvYJd)"
        result = pypeg2.parse(condition, output.SIG)
        self.assertEqual(result.pubkey, "HgTTJLAQ5sqfknMq7yLPZbehtuLSsKj9CxWN7k8QvYJd")
        self.assertEqual(pypeg2.compose(result, output.Condition), condition)

    def test_xhx(self):
        condition = "XHX(309BC5E644F797F53E5A2065EAF38A173437F2E6)"
        result = pypeg2.parse(condition, output.XHX)
        self.assertEqual(result.sha_hash, "309BC5E644F797F53E5A2065EAF38A173437F2E6")

    def test_sig_condition(self):
        condition = "SIG(HgTTJLAQ5sqfknMq7yLPZbehtuLSsKj9CxWN7k8QvYJd)"
        result = pypeg2.parse(condition, output.Condition)
        self.assertEqual(result.left.pubkey, "HgTTJLAQ5sqfknMq7yLPZbehtuLSsKj9CxWN7k8QvYJd")
        self.assertEqual(pypeg2.compose(result, output.Condition), condition)

    def test_xhr_condition(self):
        condition = "SIG(HgTTJLAQ5sqfknMq7yLPZbehtuLSsKj9CxWN7k8QvYJd)"
        result = pypeg2.parse(condition, output.Condition)
        self.assertEqual(result.left.pubkey, "HgTTJLAQ5sqfknMq7yLPZbehtuLSsKj9CxWN7k8QvYJd")
        self.assertEqual(pypeg2.compose(result, output.Condition), condition)

    def test_simple_condition(self):
        condition = "(SIG(HgTTJLAQ5sqfknMq7yLPZbehtuLSsKj9CxWN7k8QvYJd))"
        result = pypeg2.parse(condition, output.Condition)
        self.assertEqual(result.left.left.pubkey, "HgTTJLAQ5sqfknMq7yLPZbehtuLSsKj9CxWN7k8QvYJd")
        self.assertEqual(pypeg2.compose(result, output.Condition), condition)

    def test_simple_and_condition(self):
        condition = "(SIG(HgTTJLAQ5sqfknMq7yLPZbehtuLSsKj9CxWN7k8QvYJd) AND XHX(309BC5E644F797F53E5A2065EAF38A173437F2E6))"
        result = pypeg2.parse(condition, output.Condition)
        self.assertEqual(result.left.left.pubkey, "HgTTJLAQ5sqfknMq7yLPZbehtuLSsKj9CxWN7k8QvYJd")
        self.assertEqual(result.left.op.name, "AND")
        self.assertEqual(result.left.right.sha_hash, "309BC5E644F797F53E5A2065EAF38A173437F2E6")
        self.assertEqual(pypeg2.compose(result, output.Condition), condition)

    def test_simple_or_condition(self):
        condition = "(SIG(HgTTJLAQ5sqfknMq7yLPZbehtuLSsKj9CxWN7k8QvYJd) OR XHX(309BC5E644F797F53E5A2065EAF38A173437F2E6))"
        result = pypeg2.parse(condition, output.Condition)
        self.assertEqual(result.left.left.pubkey, "HgTTJLAQ5sqfknMq7yLPZbehtuLSsKj9CxWN7k8QvYJd")
        self.assertEqual(result.left.op.name, "OR")
        self.assertEqual(result.left.right.sha_hash, "309BC5E644F797F53E5A2065EAF38A173437F2E6")
        self.assertEqual(pypeg2.compose(result, output.Condition), condition)

    def test_complex_condition(self):
        condition = "(SIG(HgTTJLAQ5sqfknMq7yLPZbehtuLSsKj9CxWN7k8QvYJd) OR (SIG(DNann1Lh55eZMEDXeYt59bzHbA3NJR46DeQYCS2qQdLV) AND XHX(309BC5E644F797F53E5A2065EAF38A173437F2E6)))"
        result = pypeg2.parse(condition, output.Condition)
        self.assertEqual(result.left.left.pubkey, "HgTTJLAQ5sqfknMq7yLPZbehtuLSsKj9CxWN7k8QvYJd")
        self.assertEqual(result.left.op.name, "OR")
        self.assertEqual(result.left.right.left.pubkey, "DNann1Lh55eZMEDXeYt59bzHbA3NJR46DeQYCS2qQdLV")
        self.assertEqual(result.left.right.op.name, "AND")
        self.assertEqual(result.left.right.right.sha_hash, "309BC5E644F797F53E5A2065EAF38A173437F2E6")
        self.assertEqual(pypeg2.compose(result, output.Condition), condition)

    def test_instanciate_condition(self):
        inst = output.Condition.token(output.SIG.token("HgTTJLAQ5sqfknMq7yLPZbehtuLSsKj9CxWN7k8QvYJd"),
                                           output.Operator.token("OR"),
                                           output.Condition.token(
                                               output.SIG.token("DNann1Lh55eZMEDXeYt59bzHbA3NJR46DeQYCS2qQdLV"),
                                               output.Operator.token("AND"),
                                               output.XHX.token("309BC5E644F797F53E5A2065EAF38A173437F2E6")
                                           ))
        condition = "(SIG(HgTTJLAQ5sqfknMq7yLPZbehtuLSsKj9CxWN7k8QvYJd) OR (SIG(DNann1Lh55eZMEDXeYt59bzHbA3NJR46DeQYCS2qQdLV) AND XHX(309BC5E644F797F53E5A2065EAF38A173437F2E6)))"
        inst = pypeg2.parse(condition, output.Condition)
        self.assertEqual(inst.left.left.pubkey, "HgTTJLAQ5sqfknMq7yLPZbehtuLSsKj9CxWN7k8QvYJd")
        self.assertEqual(inst.left.op.name, "OR")
        self.assertEqual(inst.left.right.left.pubkey, "DNann1Lh55eZMEDXeYt59bzHbA3NJR46DeQYCS2qQdLV")
        self.assertEqual(inst.left.right.op.name, "AND")
        self.assertEqual(inst.left.right.right.sha_hash, "309BC5E644F797F53E5A2065EAF38A173437F2E6")
        self.assertEqual(pypeg2.compose(inst, output.Condition), condition)
