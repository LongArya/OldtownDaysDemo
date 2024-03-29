from command import Command
from navigator import Navigator
from persistent_objects.currencies_manager import CurrenciesManager
from game_enums.lvl_stage import LvlStage
from game_enums.coins_kinds import CoinsKinds


class BribeCommand(Command):
    def __init__(self, navigator: Navigator, currencies_manager: CurrenciesManager, bribe_cost):
        self._navigator = navigator
        self._currencies_manager = currencies_manager
        self._bribe_cost = bribe_cost

    def execute(self):
        self._navigator.switch_to_play_state(LvlStage.USUAL_PLAY)
        self._currencies_manager.spend_coins(CoinsKinds.TARGARYEN_COIN, self._bribe_cost)
