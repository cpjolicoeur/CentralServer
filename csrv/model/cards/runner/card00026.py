from csrv.model import actions
from csrv.model import cost
from csrv.model import timing_phases
from csrv.model.cards import card_info
from csrv.model.cards import program


class ChooseCard00026Target(timing_phases.BasePhase):
  """Choose the target for Card00026."""
  NULL_OK = False

  def __init__(self, game, player, card=None):
    timing_phases.BasePhase.__init__(self, game, player, both_players=False)
    self.card = card

  def resolve(self, choice, response=None):
    timing_phases.BasePhase.resolve(self, choice, response)
    if choice:
      self.end_phase()


class SetCard00026Target(actions.Action):
  """"""
  def __init__(self, game, player, card=None, card00026=None):
    actions.Action.__init__(self, game, player, card=card)
    self.card00026 = card00026

  def resolve(self, response=None, ignore_clicks=False, ignore_all_costs=False):
    actions.Action.resolve(
        self, response,
        ignore_clicks=ignore_clicks,
        ignore_all_costs=ignore_all_costs)
    self.card00026.set_target(self.card)

  @property
  def description(self):
    return 'Target ice with Card00026'


class BypassIce(actions.Action):
  """Bypass ice with Card00026."""

  def __init__(self, game, player, card=None):
    credits = len(game.run.current_ice().subroutines)
    cost_obj = cost.Cost(game, player, card=card, credits=credits)
    actions.Action.__init__(self, game, player, card=card, cost=cost_obj)

  def resolve(self, response=None, ignore_clicks=False, ignore_all_costs=False):
    actions.Action.resolve(
        self, response,
        ignore_clicks=ignore_clicks,
        ignore_all_costs=ignore_all_costs)
    self.game.run.bypass_ice = True
    self.game.current_phase().end_phase()


class Card00026(program.Program):

  NAME = u'Card00026'
  SET = card_info.CORE
  NUMBER = 26
  SIDE = card_info.RUNNER
  FACTION = card_info.CRIMINAL
  INFLUENCE = 1
  UNIQUE = False
  KEYWORDS = set([
      card_info.ICEBREAKER,
      card_info.KILLER,
  ])
  COST = 9
  IMAGE_SRC = '01026.png'
  STRENGTH = 2
  MEMORY = 1

  WHEN_INSTALLED_PROVIDES_CHOICES_FOR = {
      timing_phases.EncounterIce_3_1: 'interact_with_ice_actions',
  }

  def __init__(self, game, player):
    program.Program.__init__(self, game, player)
    self.target = None

  def build_actions(self):
    program.Program.build_actions(self)
    self._boost_strength_action = actions.BoostBreakerStrength(
        self.game, self.player, self, strength=1, credits=2)

  def on_install(self):
    program.Program.on_install(self)
    self.game.register_choice_provider(ChooseCard00026Target, self, 'card00026_targets')
    self.game.insert_next_phase(
        ChooseCard00026Target(self.game, self.player, card=self))

  def on_uninstall(self):
    program.Program.on_uninstall(self)
    self.target = None

  def card00026_targets(self):
    targets = []
    for server in self.game.corp.servers:
      for ice in server.ice.cards:
        targets.append(SetCard00026Target(
            self.game, self.player, card=ice, card00026=self))
    return targets

  def set_target(self, ice):
    self.target = ice

  def interact_with_ice_actions(self):
    actions = []
    if self.game.run and self.game.run.current_ice() == self.target:
      actions.append(BypassIce(self.game, self.player, card=self))
    return (actions + [self._boost_strength_action] +
        [actions.BreakSentrySubroutine(
            self.game, self.player, self, sub, credits=1)
         for sub in self.game.run.current_ice().subroutines])
