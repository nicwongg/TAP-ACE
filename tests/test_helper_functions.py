import pytest
import helper_functions


def test_valid_number_of_teams():
    assert helper_functions.valid_number_of_teams([]) == False
    assert helper_functions.valid_number_of_teams(
        ["teamA", "teamB", "teamC", "teamD", "teamE", "teamF"]) == False
    assert helper_functions.valid_number_of_teams(
        ["teamA", "teamB", "teamC", "teamD", "teamE", "teamF",
         "teamG", "teamH", "teamI", "teamJ", "teamK", "teamL"]) == True


def test_sufficient_team_data():
    assert helper_functions.sufficient_team_data([]) == False
    assert helper_functions.sufficient_team_data(["teamA", "16/01"]) == False
    assert helper_functions.sufficient_team_data(
        ["teamA", "16/01", "1"]) == True


def test_validate_provided_date():
    with pytest.raises(ValueError, match=r"Incorrect data format provided, should be in DD/MM format!"):
        helper_functions.validate_provided_date("32/12")
    with pytest.raises(ValueError, match=r"Incorrect data format provided, should be in DD/MM format!"):
        helper_functions.validate_provided_date("29/02")


def test_correct_number_of_teams_per_group():
    assert helper_functions.correct_number_of_teams_per_group({1:[], 2:[]}) == False
    assert helper_functions.correct_number_of_teams_per_group({1:['d'], 2:['a']}) == False
    assert helper_functions.correct_number_of_teams_per_group({1:['a', 'b', 'c', 'd', 'e', 'f'],
     2:['g', 'h', 'i', 'j', 'k', 'l']}) == True