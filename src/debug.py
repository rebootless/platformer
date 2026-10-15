import pyxel

from . import player_view
from .sprites import ANDROMALIUS, GOLEM, HERO, MINION, SWAMP_MONSTER, WARTAUR

on = False
_sheets = {
    "hero": HERO, "andromalius": ANDROMALIUS, "minion": MINION,
    "golem": GOLEM, "swamp monster": SWAMP_MONSTER, "wartaur": WARTAUR,
}
_labels = list(_sheets)
_pick = 0       # index in _labels, 0 = hero
_sheet = HERO
_names = list(HERO.anims)
_slot = 0       # 0 = live animation, 1.. = _names[slot - 1] looped
_tick = 0
_images = {}


def _select(i):
    global _pick, _sheet, _names, _slot, _tick
    _pick = i % len(_labels)
    _sheet = _sheets[_labels[_pick]]
    _names = list(_sheet.anims)
    _slot = 0 if _pick == 0 else 1
    _tick = 0


def _image():
    if _sheet.file not in _images:
        _images[_sheet.file] = pyxel.Image.from_image(str(_sheet.path))
    return _images[_sheet.file]


def update():
    global on, _slot, _tick
    if pyxel.btnp(pyxel.KEY_F3):
        on = not on
        _select(0)
    if not on:
        return
    if pyxel.btnp(pyxel.KEY_F2):
        _select(_pick + 1)
    elif pyxel.btnp(pyxel.KEY_F1):
        lo = 1 if _pick else 0
        _slot = lo + (_slot - lo + 1) % (len(_names) + 1 - lo)
        _tick = 0
    else:
        _tick += 1


def monster():
    return _pick != 0


def preview():
    if not on or _slot == 0 or _pick:
        return None, 0
    name = _names[_slot - 1]
    return name, _tick % HERO.anims[name].length


def _text(x, y, s):
    pyxel.text(x + 1, y + 1, s, 0)
    pyxel.text(x, y, s, 7)


def _monster(player):
    s = _sheet
    name = _names[_slot - 1]
    anim = s.anims[name]
    tick = _tick % anim.length
    f = anim.frame(tick)
    flip = anim.mirror and player.dir != s.faces
    x = int(player.x + player.w / 2 - s.w / 2)
    y = int(player.y + player.h - s.h)
    pyxel.blt(x, y, _image(), f * s.w, anim.row * s.h, -s.w if flip else s.w, s.h, s.colkey)
    pyxel.rectb(x, y, s.w, s.h, 5)
    _text(2, 2, f"{_labels[_pick]}: {name}  frame {f + 1}/{anim.frames}  tick {tick}")


def draw(player):
    if not on:
        return
    state, tick = preview()
    live = state is None
    if live:
        state, tick = player.state, player.anim_tick
    f = player_view.frame(state, tick, player.vy if live else None)
    x, y, _ = player_view.origin(player, state)
    if _pick:
        _monster(player)
    else:
        pyxel.rectb(x, y, HERO.w, HERO.h, 5)                  # sprite cell
        _text(2, 2, f"{'live' if live else 'preview'}: {state}  frame {f + 1}/{HERO.anims[state].frames}  tick {tick}")
    pyxel.rectb(player.x, player.y, player.w, player.h, 11)   # hitbox
    _text(2, 10, f"x {player.x:.1f}  y {player.y:.1f}  vx {player.vx:.1f}  vy {player.vy:.2f}")
    _text(2, 18, (
        f"ground {player.on_ground}  air {player.in_air}  stand {player.standing}  "
        f"move {player.moving}  run {player.running}  block {player.blocking}  atk {player.attacking}"
    ))
    _text(2, 26, "F1 animation  F2 monster  F3 debug")
