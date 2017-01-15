from src.classes.controller import Controller
import pytest


@pytest.fixture()
def controller():
    return Controller()