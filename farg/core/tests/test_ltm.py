import os
import tempfile
import unittest

from farg.core.ltm.edge import LTMEdge
from farg.core.ltm.graph import LTMGraph
from farg.core.ltm.node import LTMNode
from farg.core.ltm.storable import LTMNodeContent


class MockCategory(LTMNodeContent):

    def __init__(self, *, foo):
        print("Initializing MockCategory instance ", self)
        self.foo = foo

    def BriefLabel(self):
        return "foo=%s" % self.foo


class MockCategory2(LTMNodeContent):

    def __init__(self, *, foo):
        print("Initializing MockCategory2 instance ", self)
        self.foo = foo

    def BriefLabel(self):
        return "foo=%s" % self.foo


class MockMapping(LTMNodeContent):

    def __init__(self, *, category):
        self.category = category

    def BriefLabel(self):
        return "category=%s" % self.category


class TestLTMNode(unittest.TestCase):

    def test_sanity(self):
        node = LTMNode(MockCategory(foo=3))
        self.assertEqual(MockCategory(foo=3), node.content)

    def test_each_class_separate_memo(self):
        node1 = MockCategory(foo=5)
        node1a = MockCategory(foo=5)
        node2 = MockCategory2(foo=5)
        node2a = MockCategory2(foo=5)
        self.assertEqual(node1, node1a)
        self.assertEqual(node2, node2a)
        self.assertNotEqual(node1, node2)


class LTMTestBase(unittest.TestCase):

    def setUp(self):
        filehandle, self.filename = tempfile.mkstemp()

    def tearDown(self):
        os.remove(self.filename)


class TestLTM(LTMTestBase):

    def test_sanity(self):
        myltm = LTMGraph(filename=self.filename)
        c1 = MockCategory(foo=7)
        m1 = MockMapping(category=c1)
        c2 = MockCategory(foo=9)
        m2 = MockMapping(category=c2)

        for content in (c1, m1, c2, m2):
            myltm.GetNode(content=content)

        myltm.DumpToFile()

        # I'll remove the memos for MockMapping but not MockCategory, thereby testing the creation
        # mechanism.
        MockMapping.__memo__ = dict()
        # MockCategory.memos = {}

        myltm2 = LTMGraph(filename=self.filename)
        self.assertEqual(4, len(myltm2.nodes))
        c1p, m1p, c2p, m2p = (x.content for x in myltm2.nodes)
        self.assertEqual(c1p, c1)
        self.assertNotEqual(m1p, m1)
        self.assertEqual(7, c1p.foo)
        self.assertEqual(9, c2p.foo)
        self.assertEqual(c1p, m1p.category)
        self.assertEqual(c2p, m2p.category)

        c3 = MockCategory(foo=9)
        self.assertEqual(c3, c2p)

        m3 = MockMapping(category=c3)
        self.assertEqual(m3, m2p)


class TestLTM2(LTMTestBase):

    def test_activation(self):
        MockCategory.__memo__ = dict()
        MockCategory2.__memo__ = dict()
        MockMapping.__memo__ = dict()

        myltm = LTMGraph(filename=self.filename)
        c1 = MockCategory(foo=7)
        m1 = MockMapping(category=c1)
        for content in (m1, c1):
            myltm.GetNode(content=content)
        myltm.AddEdge(m1, c1)

        node_m1 = myltm.GetNode(content=m1)
        node_c1 = myltm.GetNode(content=c1)
        self.assertEqual(0, node_m1.GetRawActivation(current_time=0))
        self.assertEqual(0, node_c1.GetRawActivation(current_time=0))

        # Spiking c1 does not send activation back to m1 (edge is
        # unidirectional).
        node_c1.IncreaseActivation(2, current_time=0)
        self.assertEqual(0, node_m1.GetRawActivation(current_time=0))
        self.assertEqual(2, node_c1.GetRawActivation(current_time=0))

        # Spiking m1, though, sends activation to c1 as well.
        node_m1.IncreaseActivation(2, current_time=0)
        self.assertEqual(2, node_m1.GetRawActivation(current_time=0))
        self.assertTrue(2 < node_c1.GetRawActivation(current_time=0))

        myltm.DumpToFile()
        MockCategory.__memo__ = dict()
        MockCategory2.__memo__ = dict()
        MockMapping.__memo__ = dict()
        myltm2 = LTMGraph(filename=self.filename)
        node_m1p, node_c1p = myltm2.nodes
        m1p, c1p = (x.content for x in myltm2.nodes)
        edges = myltm2.GetNode(content=m1p).GetOutgoingEdges()
        self.assertEqual(c1p, edges[0].to_node.content)

        #: Activations reset on loading...
        self.assertEqual(0, node_m1p.GetRawActivation(current_time=0))
        self.assertEqual(0, node_c1p.GetRawActivation(current_time=0))
