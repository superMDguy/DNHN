from farg.apps.pyseqsee.categorization.categories import PSCategory
from farg.apps.pyseqsee.categorization.logic import InstanceLogic, Verify
from farg.apps.pyseqsee.codelets import CF_DescribeRelationWithObject
from farg.apps.pyseqsee.objects import PSElement
from farg.core.codelet import Codelet


class CategoryInteger(PSCategory):
    _Checks = ('isinstance(_INSTANCE, PSElement)',)
    _Context = dict(PSElement=PSElement, isinstance=isinstance)

    class DeltaReln(PSCategory):
        _Attributes = ('delta',)
        _RequiredAttributes = ('delta',)
        _Rules = ('delta: PSElement(magnitude=(_INSTANCE.second.magnitude - '
                  '_INSTANCE.first.magnitude))',)
        _Checks = ('delta.magnitude == _INSTANCE.second.magnitude - '
                   '_INSTANCE.first.magnitude',)
        _Context = dict(PSElement=PSElement)

    class RatioReln(PSCategory):
        _Attributes = ('ratio',)
        _RequiredAttributes = ('ratio',)
        _Rules = ('ratio: PSElement(magnitude=(_INSTANCE.second.magnitude / '
                  '_INSTANCE.first.magnitude))',)
        _Checks = ('ratio.magnitude == _INSTANCE.second.magnitude / '
                   '_INSTANCE.first.magnitude',
                   'ratio.magnitude == int(ratio.magnitude)')
        _Context = dict(PSElement=PSElement, int=int)

    _RelationCategories = (DeltaReln(), RatioReln())

    def BriefLabel(self):
        return 'CategoryInteger'

    def SuggestActions(self, *, instance, logic, controller):
        """What actions could we take with things that are integers?"""
        # Are these categories? "I have tried extending right", "I should try extending right..."
        # I want to suggest the following only when it has not recently been tried. Perhaps the logic
        # can store some of this bookkeepinginfo?
        object_to_right = controller.workspace.GetObjectToRight(instance)
        if not object_to_right:
            return []
        return [
            Codelet(
                family=CF_DescribeRelationWithObject,
                controller=controller,
                urgency=100,
                arguments_dict=dict(first=instance, second=object_to_right))
        ]


class CategoryEvenInteger(PSCategory):
    _Rules = ('_mag: _INSTANCE.magnitude', '_half: _mag / 2',
              'half: PSElement(magnitude=_half)')
    _Checks = ('_mag % 2 == 0',)
    _Constructors = {('_mag',): (lambda _mag: PSElement(magnitude=_mag))}
    _Attributes = set(('half',))
    _Context = dict(PSElement=PSElement)
    _TurnedOffAttributes = set(('half',))

    def BriefLabel(self):
        return 'CategoryEvenInteger'


class PrecomputedListNumericCategory(PSCategory):
    _Constructors = {('_mag',): (lambda _mag: PSElement(magnitude=_mag))}
    _Rules = ('_mag: _INSTANCE.magnitude',)
    _Checks = ('_mag in number_list',)

    def __init__(self):
        self._Context = dict(number_list=self._number_list)
        PSCategory.__init__(self)


class CategoryPrime(PrecomputedListNumericCategory):
    _number_list = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
                    59, 61, 67, 71, 73, 79, 83, 89, 97)

    def BriefLabel(self):
        return 'Primes'
