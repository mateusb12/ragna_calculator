from typing import List, Tuple

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import sys
import os
import math

from main.exporter import jbl
from model.build_model import PlayerBuild


class InterfaceGenerator:
    def __init__(self, input_player: PlayerBuild):
        self.input_player = input_player

    @staticmethod
    def adjustment(x_stat: int) -> int:
        if x_stat >= 10:
            return 52
        else:
            return 56

    @staticmethod
    def stat_required(input_stat: int) -> int:
        return math.ceil((input_stat / 10)) + 1

    def generate_interface(self):
        p1 = self.input_player
        build = p1.export_build()

        in_file = (os.path.abspath(os.path.join(os.path.dirname(__file__), 'blank_interface.png')))
        out_file = (os.path.abspath(os.path.join(os.path.dirname(__file__), 'custom.png')))
        font_file = (os.path.abspath(os.path.join(os.path.dirname(__file__), 'Sans-serif.ttf')))

        font = ImageFont.truetype(font_file, 10)
        font_tahoma_bold = ImageFont.truetype((os.path.abspath(os.path.join(os.path.dirname(__file__), 'Tahoma-bold.ttf'))),
                                          10)

        img = Image.open(in_file)
        draw = ImageDraw.Draw(img)
        x = 38
        y = 6

        draw.text((x, y), "{} +{}".format(p1.core_str, p1.str_bonus), "black", font=font)
        draw.text((x, y + 16), "{} +{}".format(p1.core_agi, p1.agi_bonus), "black", font=font)
        draw.text((x, y + 32), "{} +{}".format(p1.core_vit, p1.vit_bonus), "black", font=font)
        draw.text((x, y + 48), "{} +{}".format(p1.core_int, p1.int_bonus), "black", font=font)
        draw.text((x, y + 64), "{} +{}".format(p1.core_dex, p1.dex_bonus), "black", font=font)
        draw.text((x, y + 80), "{} +{}".format(p1.core_luk, p1.luk_bonus), "black", font=font)

        draw.text((x + self.adjustment(self.stat_required(p1.core_str)), y),
                  str(self.stat_required(p1.core_str)), "black", font=font)
        draw.text((x + self.adjustment(self.stat_required(p1.core_agi)), y + 16),
                  str(self.stat_required(p1.core_agi)), "black", font=font)
        draw.text((x + self.adjustment(self.stat_required(p1.core_vit)), y + 32),
                  str(self.stat_required(p1.core_vit)), "black", font=font)
        draw.text((x + self.adjustment(self.stat_required(p1.core_int)), y + 48),
                  str(self.stat_required(p1.core_int)), "black", font=font)
        draw.text((x + self.adjustment(self.stat_required(p1.core_dex)), y + 64),
                  str(self.stat_required(p1.core_dex)), "black", font=font)
        draw.text((x + self.adjustment(self.stat_required(p1.core_luk)), y + 80),
                  str(self.stat_required(p1.core_luk)), "black", font=font)

        draw.text((x + 120, y), "{} +{}".format(build.atk_bonus, build.atk_base), "black", font=font)
        draw.text((x + 125, y + 16), "{}~{}".format(build.matk_min, build.matk_max), "black", font=font)
        draw.text((x + 135, y + 32), "{}".format(build.hit), "black", font=font)
        draw.text((x + 145, y + 48), "{}".format(build.critical), "black", font=font)

        draw.text((x + 200, y), "{} +{}".format(build.def_hard, build.def_soft), "black", font=font)
        draw.text((x + 200, y + 16), "{} +{}".format(build.mdef_hard, build.mdef_soft), "black", font=font)
        draw.text((x + 200, y + 32), "{} +{}".format(build.flee, build.perfect_dodge), "black", font=font)
        draw.text((x + 215, y + 48), "177".format(build.aspd), "black", font=font)

        draw.text((x + 220, y + 64), "{}".format(build.attribute_balance), "black", font=font)

        draw.text((x + 242, y - 1), "MaxHP", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x + 242, y + 15), "MaxSP", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x + 242, y + 31), "HP_Regen", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x + 242, y + 47), "SP_Regen", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x + 242, y + 63), "Mov_speed", (68, 91, 131), font=font_tahoma_bold)

        draw.text((x + 290, y), "{}".format(build.max_hp), "black", font=font)
        draw.text((x + 290, y + 16), "{}".format(build.max_sp), "black", font=font)
        draw.text((x + 300, y + 32), "{}".format(build.hp_regen), "black", font=font)
        draw.text((x + 300, y + 48), "{}".format(build.sp_regen), "black", font=font)
        draw.text((x + 300, y + 64), "100%", "black", font=font)
        img.show()
        img.save(out_file)


# p1 = PlayerBuild(jbl, 99, 50, 'dancer', [30, 10, 91, 99, 1, 1])
# build = p1.export_build()

igen = InterfaceGenerator(PlayerBuild(jbl, 99, 50, 'dancer', [30, 10, 91, 99, 1, 1]))
igen.generate_interface()
