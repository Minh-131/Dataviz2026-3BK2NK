from src.basket import basket_rows, basket_medians, country_basket_plot, income_group_plot
from src.data import read_datasets


def test_food_groups_only_exist_in_2021_and_are_complete():
    data,_ = read_datasets()
    rows = basket_rows(data)
    assert len(rows) == 165
    assert set(rows.year.unique()) == {2021}
    cols = [name for name in rows if name.endswith('_PPP_share')]
    assert ((rows[cols].sum(axis=1) - 100).abs() < 1e-8).all()
    assert ((rows.basket_sum-rows.CoHD_PPP).abs() <= 0.025).all()


def test_income_medians_and_charts():
    data,_ = read_datasets()
    grouped=basket_medians(data)
    assert len(grouped) == 4
    low=grouped[grouped.income_group.eq('Low income') | grouped.income_group.eq('Low-income')]
    high=grouped[grouped.income_group.eq('High income') | grouped.income_group.eq('High-income')]
    assert 37 < low.iloc[0].median_asf_share < 39
    assert 23 < high.iloc[0].median_asf_share < 25
    for mode in (True,False):
        assert len(country_basket_plot(basket_rows(data).iloc[0],mode).data) == 1
        assert len(income_group_plot(data,mode).data) == 1
