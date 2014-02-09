import unittest
from csrv.model import cards
from csrv.model.cards import corp
from csrv.model import deck
from csrv.model import game
from csrv.model import premade_decks
from csrv.model import test_base
from csrv.model import timing_phases
from csrv.model.cards.runner import card01049


class Card01049Test(test_base.TestBase):

  def setUp(self):
    test_base.TestBase.setUp(self)
    self.card = card01049.Card01049(self.game, self.game.runner)
    self.game.runner.clicks.set(4)
    self.game.runner.credits.set(5)
    self.game.runner.grip.add(self.card)
    self.game.insert_next_phase(
        timing_phases.RunnerTurnActions(self.game, self.game.runner))
    self.ice = cards.Registry.get('Card01103')(self.game, self.game.corp)

  def test_gain_credits(self):
    self.assertIn(
        self.card._gain_credits_action, self.game.current_phase().choices())
    self.game.resolve_current_phase(
        self.card._gain_credits_action, None)
    self.assertEqual(7, self.game.runner.credits.value)

  def test_expose_card(self):
    self.assertIn(
        self.card._expose_card_action, self.game.current_phase().choices())
    response = self.card._expose_card_action.request().new_response()
    self.game.corp.hq.install_ice(self.ice)
    response.card = self.ice
    self.game.resolve_current_phase(
        self.card._expose_card_action, response)
    self.assertIn(self.ice.game_id, self.game.exposed_ids)


if __name__ == '__main__':
  unittest.main()
