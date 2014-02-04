import threading
import cPickle
import redis

class GameData(object):
  def __init__(self):
    self.runner_deck = None
    self.corp_deck = None
    self.game = None
    self.handlers = []


class Data(object):
  """A really dumb in-memory store"""

  REDIS = redis.StrictRedis() # localhost:6379 by default
  GAMES = {}
  GAME_IDX = 0
  GAME_LOCK = threading.Lock()


  @classmethod
  def new_game(cls):
    with cls.GAME_LOCK:
      game_id = cls.REDIS.incr('csrv:games:last_game_id')
      game_data = GameData()
      cls.REDIS.set("csrv:games:{0}".format(game_id), cls.dump(game_id, game_data.game))
    return str(game_id)

  @classmethod
  def get(cls, idx):
    saved_game = cPickle.loads(cls.REDIS.get("csrv:games:{0}".format(idx)))
    game_data = GameData()
    game_data.game = saved_game
    return game_data

  @classmethod
  def dump(cls, idx, game):
    cls.REDIS.set("csrv:games:{0}".format(idx), cPickle.dumps(game))
