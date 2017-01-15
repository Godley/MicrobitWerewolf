def test_register(controller):
    player = {"id": 0}
    controller.add_player(player)
    player1 = controller.get_player()
    assert "channel" in player1
    assert player1["id"] == 0

def test_register_debounce(controller):
    player = {"id": 0}
    controller.add_player(player)
    controller.add_player(player)
    controller.await_registration(period=1.0, limit=0.5)
    assert len(controller.players) == 1

