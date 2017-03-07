import os
import tempfile
import unittest

from farg.core.ltm.graph import LTMGraph
from farg.core.ltm.storable import LTMStorableMixin, LTMNodeContent
# TODO: I need a class called LTMNodeContent, which can actually be content, and this can have
# MemoizedConstructor as a metaclass. This class should have a kw-only constructor, and any attribute
# not passed in via the constructor must begin with a _.


class PlatonicInt(LTMNodeContent):

    def __init__(self, *, me):
        """me is a positive int; if it is bigger than 1, PlatonicInt(half of me) is the parent."""
        print("PlatonicInt constructor called: me=", me)
        self.me = me
        if me > 1:
            self._parent = PlatonicInt(me=int(me / 2))
        else:
            self._parent = None

    def BriefLabel(self):
        return 'PlatonicInt(%d)' % self.me

    def LTMDependentContent(self):
        if self._parent:
            return [self._parent]
        return ()


class FullInt(LTMStorableMixin):

    def __init__(self, me):
        """Not the item stored: its platonic version is PlatonicInt."""
        self.me = me

    def BriefLabel(self):
        return 'BriefLabel(%d)' % self.me

    def GetLTMStorableContent(self):
        return PlatonicInt(me=self.me)


class LTMTestBase(unittest.TestCase):

    def setUp(self):
        unused_filehandle, self.filename = tempfile.mkstemp()

    def tearDown(self):
        os.remove(self.filename)

    def test_sanity(self):
        graph = LTMGraph(filename=self.filename)
        self.assertFalse(graph.is_working_copy)
        self.assertTrue(graph.IsEmpty())

        fi6 = FullInt(6)
        fi6_2 = FullInt(6)
        self.assertNotEqual(fi6, fi6_2)
        self.assertEqual(fi6.GetLTMStorableContent(),
                         fi6_2.GetLTMStorableContent())

        node = graph.GetNode(content=fi6)
        self.assertFalse(graph.IsEmpty())
        self.assertEqual(3, len(graph.GetNodes()))
        self.assertEqual(node, graph.GetNode(content=fi6_2))
        self.assertEqual(3, len(graph.GetNodes()))

        # Add an edge.
        graph.AddEdge(FullInt(3), FullInt(6), utility=5)

        # Dump to file.
        graph.DumpToFile()
        graph2 = LTMGraph(filename=self.filename)
        self.assertEqual(3, len(graph2.GetNodes()))
        node2 = graph2.GetNode(content=fi6)
        self.assertEqual(3, len(graph2.GetNodes()))
        self.assertEqual(node2, graph2.GetNode(content=fi6_2))
        self.assertNotEqual(node, node2)
        self.assertEqual(3, len(graph2.GetNodes()))

        outgoing_edges_from_pi3 = graph2.GetNode(
            content=PlatonicInt(me=3)).GetOutgoingEdges()
        # That contains two (to 6, and to 1, on which it depends)
        for i in range(2):
            self.assertTrue(outgoing_edges_from_pi3[
                            i].to_node.content.me in {1, 6})
            self.assertTrue(outgoing_edges_from_pi3[i].utility in {1, 5})

        # Test COPYING
        graph3 = LTMGraph(master_graph=graph2)
        self.assertTrue(graph3.is_working_copy)
        self.assertEqual(3, len(graph3.GetNodes()))
        # The nodes are different
        self.assertNotEqual(graph2.GetNode(content=fi6),
                            graph3.GetNode(content=fi6))
