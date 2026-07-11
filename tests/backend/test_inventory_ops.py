from inventory_ops import stock_is_sufficient   # conftest puts server/ on sys.path


def test_equal_stock_is_fulfillable():
    assert stock_is_sufficient(850, 850) is True     # the off-by-one boundary


def test_shortfall_not_fulfillable():
    assert stock_is_sufficient(800, 850) is False


def test_surplus_is_fulfillable():
    assert stock_is_sufficient(900, 850) is True
