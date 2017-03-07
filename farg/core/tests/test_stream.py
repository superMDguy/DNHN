import unittest

from farg.core.controller import Controller
from farg.core.focusable_mixin import FocusableMixin
from farg.core.stream import Stream
from farg.core.ui.batch_ui import BatchUI


class MyFocusable(FocusableMixin):

    def __init__(self, x):
        self.x = x
        self.y = 2 * x

    def GetFringe(self, controller):
        return {self.x: 0.7, self.y: 0.4}

    def GetAffordances(self, controller):
        return ()

    def GetSimilarityAffordances(self, focusable, other_fringe, my_fringe, controller):
        return ()


class TestStream(unittest.TestCase):

    def test_basic(self):

        c = BatchUI(controller_class=Controller).controller
        s = c.stream
        self.assertEqual(0, s.FociCount())

        m3 = MyFocusable(3)
        m6 = MyFocusable(6)
        m12 = MyFocusable(12)

        hits_map = s.StoreFringeAndCalculateOverlap(m3)
        self.assertEqual(1, s.FociCount())
        self.assertEqual(0, len(hits_map))

        s.FocusOn(m3)
        self.assertEqual(1, s.FociCount())

        hits_map = s.StoreFringeAndCalculateOverlap(m6)
        self.assertEqual(2, s.FociCount())
        self.assertEqual(1, len(hits_map))
        self.assertTrue(m3 in hits_map)
        self.assertAlmostEqual(0.28, hits_map[m3])

        hits_map = s.StoreFringeAndCalculateOverlap(m12)
        self.assertEqual(3, s.FociCount())
        self.assertEqual(1, len(hits_map))
        self.assertTrue(m6 in hits_map)
        self.assertAlmostEqual(0.28, hits_map[m6])

        s._PrepareForFocusing(m6)
        hits_map = s.StoreFringeAndCalculateOverlap(m6)
        self.assertEqual(3, s.FociCount())
        self.assertEqual(2, len(hits_map))
        self.assertTrue(m3 in hits_map)
        self.assertTrue(m12 in hits_map)
        self.assertAlmostEqual(0.28, hits_map[m12])
        self.assertAlmostEqual(0.2527, hits_map[m3])

        s.kMaxFocusableCount = 3
        # So now adding any will remove something (specifically, m3)
        f = MyFocusable(1.5)
        s._PrepareForFocusing(f)
        hits_map = s.StoreFringeAndCalculateOverlap(f)
        self.assertEqual(3, s.FociCount())
        self.assertEqual(0, len(hits_map))
        self.assertFalse(m3 in s.foci)
