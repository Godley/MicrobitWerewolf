import pytest

def test_register(controller):
    player = {"id": 0}
    controller.add_player(player)
    player1 = controller.get_player()
    assert "id" in player1
    assert player1["id"] == 0

def test_register_debounce(controller):
    player = {"id": 0}
    controller.add_player(player)
    controller.add_player(player)
    controller.await_registration(period=1.0, limit=0.5, enough_players=lambda e: e >= 1)
    assert len(controller.players) == 1

def test_assign_players(controller):
    players = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    orgs = controller.sort_players(players)
    assert len(orgs["wolves"]) == 2
    assert "seer" in orgs
    assert "doctor" in orgs
    assert len(orgs["villagers"]) == len(players) - 4

def test_not_enough_players(controller):
    players = [0, 1, 2, 3]
    with pytest.raises(ValueError):
        orgs = controller.sort_players(players)

def test_not_enough_players_in_time_limit(controller):
    players = [{"id": i} for i in range(4)]
    [controller.add_player({"id": i} for i in range(4))]
    with pytest.raises(ValueError):
        controller.await_registration(period=1.0, limit=0.5)


