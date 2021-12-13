import pytest
from pytest import mark
from pytest import fixture
from checkout import Checkout

@fixture()
def checkout():
    checkout = Checkout()
    checkout.addItemPrice('a',1)
    checkout.addItemPrice('b',2)
    return checkout


def test_CanCalculateTotal(checkout):
    checkout.addItem('a')
    assert checkout.caculateTotal() == 1

def test_GetCorrectTotalwithMultipleItems(checkout):
    checkout.addItem('a')
    checkout.addItem('b')
    assert checkout.caculateTotal() == 3

def test_canAddDiscountRule(checkout):
    checkout.addDiscount('a',3,2)

def test_canApplyDiscountRule(checkout):
    checkout.addDiscount('a',3,2)
    checkout.addItem('a')
    checkout.addItem('a')
    checkout.addItem('a')
    checkout.addItem('a')
    checkout.addItem('a')
    checkout.addItem('a')
    checkout.addItem('a')
    assert checkout.caculateTotal() == 5

def test_ExceptionWithBadItem(checkout):
    with pytest.raises(Exception):
        checkout.addItem('c')
