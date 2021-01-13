from typing import List, Tuple

import requests
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import sys
import os
import math

from ragnarok.main.gear_query import dict_name_to_dict_id, is_id_dead_id
from ragnarok.model.equip_model import Armor, PlayerGear
from ragnarok.main.exporter import jbl, equip_db
from ragnarok.model.build_model import PlayerBuild


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
        out_file = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..',
                                                 'pyflask', 'app', 'static', 'assets', 'custom.png')))
        font_file = (os.path.abspath(os.path.join(os.path.dirname(__file__), 'Sans-serif.ttf')))

        font = ImageFont.truetype(font_file, 10)
        font_tahoma_bold = ImageFont.truetype((
            os.path.abspath(os.path.join(os.path.dirname(__file__), 'Tahoma-bold.ttf'))), 10)

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
        draw.text((x + 205, y + 47), "{}".format(build.aspd), "black", font=font)

        if build.attribute_balance > 1000:
            draw.text((x + 205, y + 64), "{}".format(build.attribute_balance), "black", font=font)
        elif build.attribute_balance > 100:
            draw.text((x + 210, y + 64), "{}".format(build.attribute_balance), "black", font=font)
        else:
            draw.text((x + 220, y + 64), "{}".format(build.attribute_balance), "black", font=font)

        draw.text((x + 242, y - 1), "MaxHP", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x + 242, y + 15), "MaxSP", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x + 242, y + 31), "HP_Regen", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x + 242, y + 47), "SP_Regen", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x + 242, y + 63), "Mov_speed", (68, 91, 131), font=font_tahoma_bold)

        draw.text((x + 290, y - 1), "{}".format(build.max_hp), "black", font=font)
        draw.text((x + 290, y + 15), "{}".format(build.max_sp), "black", font=font)
        draw.text((x + 300, y + 32), "{}".format(build.hp_regen), "black", font=font)
        draw.text((x + 300, y + 48), "{}".format(build.sp_regen), "black", font=font)
        draw.text((x + 300, y + 64), "100%", "black", font=font)
        img.save(out_file)

    @staticmethod
    def download_icons(icon_list: List[int]):
        for icon_id in icon_list:
            icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                     'interface', 'icon_{}.png'.format(icon_id)))
            if not os.path.isfile(icon_path):
                # response = requests.get("https://file5s.ratemyserver.net/items/small/{}.gif".format(icon_id))
                response = requests.get("http://db.irowiki.org/image/item/{}.png".format(icon_id))
                icon_path = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), 'icons', 'icon_{}.png'.format(icon_id)))
                file = open(icon_path, "wb")
                file.write(response.content)
                file.close()

    @staticmethod
    def check_icons(icon_list: List[int]):
        need_download = []
        for qw in icon_list:
            icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'icons', 'icon_{}.png'.format(qw)))
            if not os.path.isfile(icon_path):
                need_download.append(qw)
        if not need_download:
            return False
        else:
            return need_download

    def generate_equip_details(self, text_dict: dict, sex: str):
        pe = PlayerGear(text_dict, self.input_player.current_job, self.input_player.base_level)

        in_file = (os.path.abspath(os.path.join(os.path.dirname(__file__), 'equip_window.png')))
        out_file = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..',
                                                 'pyflask', 'app', 'static', 'assets', 'equip_custom.png')))

        img = Image.open(in_file).convert("RGBA")
        img.putalpha(255)
        draw = ImageDraw.Draw(img)

        font_file = (os.path.abspath(os.path.join(os.path.dirname(__file__), 'Sans-serif.ttf')))
        font_db = []
        font_10pt = ImageFont.truetype(font_file, 15)
        for i in range(0, 11):
            font_db.append(None)
        for i in range(10, 21):
            font_db.append(ImageFont.truetype(font_file, i))

        def draw_multiline(textstring: str, tx: int, ty: int, tfont: ImageFont):
            if len(textstring) <= 11:
                lines = [textstring]
            else:
                lines = [textstring[:11], textstring[11:]]
            for line in lines:
                draw.text((tx, ty), line, font=tfont, fill="#000000")
                ty += font_db[12].getsize(line)[1] - 1

        if pe.headtop:
            if not pe.headtop.is_dead_gear():
                draw_multiline('{}'.format(pe.headtop.export_text()), 35, 0, font_db[12])
        if pe.headlow:
            if not pe.headlow.is_dead_gear():
                draw_multiline('{}'.format(pe.headlow.export_text()), 35, 28, font_db[12])
        if pe.weapon:
            if not pe.weapon.is_dead_gear():
                draw_multiline('{}'.format(pe.weapon.export_text()), 35, 52, font_db[12])
        if pe.weapon.two_handed:
            draw_multiline('{}'.format(pe.weapon.export_text()), 175, 53, font_db[12])
        if pe.robe:
            if not pe.robe.is_dead_gear():
                textline = pe.robe.export_text()
                if len(textline) > 11:
                    draw_multiline('{}'.format(textline), 35, 77, font_db[12])
                else:
                    draw_multiline('{}'.format(textline), 35, 83, font_db[12])
        if pe.accessory1:
            if not pe.accessory1.is_dead_gear():
                textline = pe.accessory1.export_text()
                if len(textline) > 11:
                    draw_multiline('{}'.format(textline), 35, 105, font_db[12])
                else:
                    draw_multiline('{}'.format(textline), 35, 110, font_db[12])
        if pe.headmid:
            if not pe.headmid.is_dead_gear():
                draw_multiline('{}'.format(pe.headmid.export_text()), 175, 0, font_db[12])
        if pe.armor:
            if not pe.armor.is_dead_gear():
                draw_multiline('{}'.format(pe.armor.export_text()), 175, 27, font_db[12])
        if pe.shield:
            if not pe.shield.is_dead_gear():
                draw_multiline('{}'.format(pe.shield.export_text()), 175, 53, font_db[12])
        if pe.shoes:
            if not pe.shoes.is_dead_gear():
                textline = pe.shoes.export_text()
                if len(textline) > 11:
                    draw_multiline('{}'.format(pe.shoes.export_text()), 175, 80, font_db[12])
                else:
                    draw_multiline('{}'.format(pe.shoes.export_text()), 175, 82, font_db[12])
        if pe.accessory2:
            if not pe.accessory2.is_dead_gear():
                textline = pe.accessory2.export_text()
                if len(textline) > 11:
                    draw_multiline('{}'.format(textline), 175, 105, font_db[12])
                else:
                    draw_multiline('{}'.format(textline), 175, 110, font_db[12])

        download_queue = self.check_icons(list(pe.export_id_table().values()))
        if download_queue is not False:
            self.download_icons(download_queue)

        gear_ids = pe.export_id_table()

        def draw_icon(icon_id: int, icon_x: int, icon_y: int):
            if icon_id is not None and not is_id_dead_id(icon_id):
                icon_path = (
                    os.path.abspath(os.path.join(os.path.dirname(__file__), 'icons', 'icon_{}.png'.format(icon_id))))
                foreground = Image.open(icon_path).convert("RGBA")
                img.paste(foreground, (icon_x, icon_y), foreground)

        draw_icon(gear_ids['headtop'], 5, 3)
        draw_icon(gear_ids['headmid'], 250, 3)
        draw_icon(gear_ids['headlow'], 5, 25)
        draw_icon(gear_ids['armor'], 250, 25)
        draw_icon(gear_ids['weapon'], 5, 52)
        draw_icon(gear_ids['shield'], 250, 52)
        draw_icon(gear_ids['robe'], 5, 79)
        draw_icon(gear_ids['shoes'], 250, 79)
        draw_icon(gear_ids['accessory1'], 5, 107)
        draw_icon(gear_ids['accessory2'], 248, 107)

        if pe.weapon.two_handed:
            draw_icon(gear_ids['weapon'], 250, 52)

        chosen_sex = sex
        job = pe.job
        sprite_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), 'sprites',
                                                    '{}'.format(chosen_sex), '{}.png'.format(job))))
        sprite = Image.open(sprite_path).convert("RGBA")
        pixel_data = sprite.getdata()
        new_data = []
        for item in pixel_data:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        sprite.putdata(new_data)
        sprite_x = 42
        sprite_y = -27
        img.paste(sprite, (sprite_x, sprite_y), sprite)

        img.save(out_file)

    def generate_resistance_details(self):
        resist_races = {"RC_Formless": 5, "RC_Undead": 100, "RC_Brute": 100, "RC_Plant": 100, "RC_Insect": 100,
                        "RC_Fish": 100, "RC_Demon": 100, "RC_DemiHuman": 100, "RC_Player": 100, "RC_Angel": 100,
                        "RC_Dragon": 100}
        resist_elements = {"Ele_Neutral": 5, "Ele_Water": 100, "Ele_Earth": 100, "Ele_Fire": 100, "Ele_Wind": 100,
                           "Ele_Poison": 100, "Ele_Holy": 100, "Ele_Dark": 100, "Ele_Ghost": 100, "Ele_Undead": 100}
        resist_badstatus = {"Eff_Poison": 100, "Eff_Stun": 5, "Eff_Freeze": 100, "Eff_Curse": 100, "Eff_Blind": 100,
                            "Eff_Sleep": 100, "Eff_Silence": 100, "Eff_Confusion": 100, "Eff_Bleeding": 100,
                            "Eff_Stone": 100}
        resist_sizes = {"Size_Small": 100, "Size_Medium": 100, "Size_Large": 100}
        resist_monstertype = {"Class_Normal": 100, "Class_Boss": 100}
        duration_badstatus = {"Eff_Poison": 0.95, "Eff_Stun": 0.95, "Eff_Freeze": 0.95, "Eff_Curse": 0.95,
                              "Eff_Blind": 0.95, "Eff_Sleep": 0.95, "Eff_Silence": 0.95, "Eff_Confusion": 0.95,
                              "Eff_Bleeding": 0.95, "Eff_Stone": 0.95}

        rd = {"resist_element_%": resist_elements,
              "resist_race_%": resist_races,
              "resist_size_%": resist_sizes,
              "resist_allmonster_%": resist_monstertype,
              "resist_badstatus_%": resist_badstatus,
              "duration_badstatus": duration_badstatus,
              "resist_melee_%": 0,
              "resist_ranged_%": 0}
        p1 = self.input_player

        in_file = (os.path.abspath(os.path.join(os.path.dirname(__file__), 'blank_resistance.png')))
        out_file = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..',
                                                 'pyflask', 'app', 'static', 'assets', 'player_resistance.png')))
        font_file = (os.path.abspath(os.path.join(os.path.dirname(__file__), 'Sans-serif.ttf')))

        font = ImageFont.truetype(font_file, 10)
        font_tahoma_bold = ImageFont.truetype((
            os.path.abspath(os.path.join(os.path.dirname(__file__), 'Tahoma-bold.ttf'))), 11)

        img = Image.open(in_file)
        draw = ImageDraw.Draw(img)

        x = 38
        y = 6

        draw.text((x - 30, y - 1), "Neutral", "DarkSlateGray", font=font_tahoma_bold)
        draw.text((x - 30, y + 15), "Water", "Blue", font=font_tahoma_bold)
        draw.text((x - 30, y + 31), "Earth", "Brown", font=font_tahoma_bold)
        draw.text((x - 30, y + 47), "Fire", "Red", font=font_tahoma_bold)
        draw.text((x - 30, y + 63), "Wind", "Green", font=font_tahoma_bold)
        draw.text((x - 30, y + 79), "Poison", "Purple", font=font_tahoma_bold)
        draw.text((x - 30, y + 95), "Holy", "DarkOrange", font=font_tahoma_bold)
        draw.text((x - 30, y + 111), "Shadow", "Black", font=font_tahoma_bold)
        draw.text((x - 30, y + 127), "Ghost", "SlateBlue", font=font_tahoma_bold)
        draw.text((x - 30, y + 143), "Undead", "Indigo", font=font_tahoma_bold)

        draw.text((x + 25, y), "{}%".format(rd["resist_element_%"]["Ele_Neutral"]), "black", font=font)
        draw.text((x + 25, y + 16), "{}%".format(rd["resist_element_%"]["Ele_Water"]), "black", font=font)
        draw.text((x + 25, y + 32), "{}%".format(rd["resist_element_%"]["Ele_Earth"]), "black", font=font)
        draw.text((x + 25, y + 48), "{}%".format(rd["resist_element_%"]["Ele_Fire"]), "black", font=font)
        draw.text((x + 25, y + 64), "{}%".format(rd["resist_element_%"]["Ele_Wind"]), "black", font=font)
        draw.text((x + 25, y + 80), "{}%".format(rd["resist_element_%"]["Ele_Poison"]), "black", font=font)
        draw.text((x + 25, y + 96), "{}%".format(rd["resist_element_%"]["Ele_Holy"]), "black", font=font)
        draw.text((x + 25, y + 112), "{}%".format(rd["resist_element_%"]["Ele_Dark"]), "black", font=font)
        draw.text((x + 25, y + 128), "{}%".format(rd["resist_element_%"]["Ele_Ghost"]), "black", font=font)
        draw.text((x + 25, y + 144), "{}%".format(rd["resist_element_%"]["Ele_Undead"]), "black", font=font)

        x += 100
        draw.text((x - 30, y - 1), "Formless", "DarkSlateGray", font=font_tahoma_bold)
        draw.text((x - 30, y + 15), "Undead", "Indigo", font=font_tahoma_bold)
        draw.text((x - 30, y + 31), "Brute", "Brown", font=font_tahoma_bold)
        draw.text((x - 30, y + 47), "Plant", "DarkSeaGreen", font=font_tahoma_bold)
        draw.text((x - 30, y + 63), "Insect", "Green", font=font_tahoma_bold)
        draw.text((x - 30, y + 79), "Fish", "Blue", font=font_tahoma_bold)
        draw.text((x - 30, y + 95), "Demon", "Red", font=font_tahoma_bold)
        draw.text((x - 30, y + 111), "Humanoid", "Black", font=font_tahoma_bold)
        draw.text((x - 30, y + 127), "Angel", "DarkOrange", font=font_tahoma_bold)
        draw.text((x - 30, y + 143), "Dragon", "LimeGreen", font=font_tahoma_bold)

        x += 5
        draw.text((x + 25, y), "{}%".format(rd["resist_race_%"]["RC_Formless"]), "black", font=font)
        draw.text((x + 25, y + 16), "{}%".format(rd["resist_race_%"]["RC_Undead"]), "black", font=font)
        draw.text((x + 25, y + 32), "{}%".format(rd["resist_race_%"]["RC_Brute"]), "black", font=font)
        draw.text((x + 25, y + 48), "{}%".format(rd["resist_race_%"]["RC_Plant"]), "black", font=font)
        draw.text((x + 25, y + 64), "{}%".format(rd["resist_race_%"]["RC_Insect"]), "black", font=font)
        draw.text((x + 25, y + 80), "{}%".format(rd["resist_race_%"]["RC_Fish"]), "black", font=font)
        draw.text((x + 25, y + 96), "{}%".format(rd["resist_race_%"]["RC_Demon"]), "black", font=font)
        draw.text((x + 25, y + 112), "{}%".format(rd["resist_race_%"]["RC_DemiHuman"]), "black", font=font)
        draw.text((x + 25, y + 128), "{}%".format(rd["resist_race_%"]["RC_Angel"]), "black", font=font)
        draw.text((x + 25, y + 144), "{}%".format(rd["resist_race_%"]["RC_Dragon"]), "black", font=font)

        x += 100
        draw.text((x - 30, y - 1), "Stun", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x - 30, y + 15), "Curse", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x - 30, y + 31), "Silence", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x - 30, y + 47), "Sleep", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x - 30, y + 63), "Freeze", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x - 30, y + 79), "Stone", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x - 30, y + 95), "Blind", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x - 30, y + 111), "Chaos", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x - 30, y + 127), "Bleeding", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x - 30, y + 143), "Poison", (68, 91, 131), font=font_tahoma_bold)

        draw.text((x + 25, y), "{}%".format(rd["resist_badstatus_%"]["Eff_Stun"]), "black", font=font)
        draw.text((x + 25, y + 16), "{}%".format(rd["resist_badstatus_%"]["Eff_Curse"]), "black", font=font)
        draw.text((x + 25, y + 32), "{}%".format(rd["resist_badstatus_%"]["Eff_Silence"]), "black", font=font)
        draw.text((x + 25, y + 48), "{}%".format(rd["resist_badstatus_%"]["Eff_Sleep"]), "black", font=font)
        draw.text((x + 25, y + 64), "{}%".format(rd["resist_badstatus_%"]["Eff_Freeze"]), "black", font=font)
        draw.text((x + 25, y + 80), "{}%".format(rd["resist_badstatus_%"]["Eff_Stone"]), "black", font=font)
        draw.text((x + 25, y + 96), "{}%".format(rd["resist_badstatus_%"]["Eff_Blind"]), "black", font=font)
        draw.text((x + 25, y + 112), "{}%".format(rd["resist_badstatus_%"]["Eff_Confusion"]), "black", font=font)
        draw.text((x + 25, y + 128), "{}%".format(rd["resist_badstatus_%"]["Eff_Bleeding"]), "black", font=font)
        draw.text((x + 25, y + 144), "{}%".format(rd["resist_badstatus_%"]["Eff_Poison"]), "black", font=font)

        x += 100
        draw.text((x - 30, y - 1), "Stun", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x - 30, y + 15), "Curse", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x - 30, y + 31), "Silence", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x - 30, y + 47), "Sleep", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x - 30, y + 63), "Freeze", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x - 30, y + 79), "Stone", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x - 30, y + 95), "Blind", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x - 30, y + 111), "Chaos", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x - 30, y + 127), "Bleeding", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x - 30, y + 143), "Poison", (68, 91, 131), font=font_tahoma_bold)

        draw.text((x + 25, y), "{}s".format(rd["duration_badstatus"]["Eff_Stun"]), "black", font=font)
        draw.text((x + 25, y + 16), "{}s".format(rd["duration_badstatus"]["Eff_Curse"]), "black", font=font)
        draw.text((x + 25, y + 32), "{}s".format(rd["duration_badstatus"]["Eff_Silence"]), "black", font=font)
        draw.text((x + 25, y + 48), "{}s".format(rd["duration_badstatus"]["Eff_Sleep"]), "black", font=font)
        draw.text((x + 25, y + 64), "{}s".format(rd["duration_badstatus"]["Eff_Freeze"]), "black", font=font)
        draw.text((x + 25, y + 80), "{}s".format(rd["duration_badstatus"]["Eff_Stone"]), "black", font=font)
        draw.text((x + 25, y + 96), "{}s".format(rd["duration_badstatus"]["Eff_Blind"]), "black", font=font)
        draw.text((x + 25, y + 112), "{}s".format(rd["duration_badstatus"]["Eff_Confusion"]), "black", font=font)
        draw.text((x + 25, y + 128), "{}s".format(rd["duration_badstatus"]["Eff_Bleeding"]), "black", font=font)
        draw.text((x + 25, y + 144), "{}s".format(rd["duration_badstatus"]["Eff_Poison"]), "black", font=font)

        x += 100
        draw.text((x - 30, y - 1), "Small", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x - 30, y + 15), "Medium", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x - 30, y + 31), "Large", (68, 91, 131), font=font_tahoma_bold)

        draw.text((x - 30, y + 63), "Normal", (68, 91, 131), font=font_tahoma_bold)
        draw.text((x - 30, y + 79), "Boss", (68, 91, 131), font=font_tahoma_bold)

        draw.text((x - 30, y + 111), "Ranged", (68, 91, 131), font=font_tahoma_bold)

        draw.text((x + 25, y), "{}%".format(rd["resist_size_%"]["Size_Small"]), "black", font=font)
        draw.text((x + 25, y + 16), "{}%".format(rd["resist_size_%"]["Size_Medium"]), "black", font=font)
        draw.text((x + 25, y + 32), "{}%".format(rd["resist_size_%"]["Size_Large"]), "black", font=font)

        draw.text((x + 25, y + 64), "{}%".format(rd["resist_allmonster_%"]["Class_Normal"]), "black", font=font)
        draw.text((x + 25, y + 80), "{}%".format(rd["resist_allmonster_%"]["Class_Boss"]), "black", font=font)

        draw.text((x + 25, y + 112), "{}%".format(rd["resist_ranged_%"]), "black", font=font)

        img.show()
        img.save(out_file)


# tt = {"headgear1": ('(No Headtop)', 0, 0),
#       "headgear2": ('Sunglasses [1]', 0, 'Willow Card'),
#       "headgear3": ('Cigarette', 0, 0),
#       "weapon": None,
#       "shield": ('Buckler [1]', 0, 'Thief Bug Egg Card'),
#       "shoes": ('Sandals [1]', 0, 'Matyr Card'),
#       "armor": ('Formal Suit [1]', 0, 'Dokebi Card'),
#       "robe": ('Hood [1]', 0, 'Condor Card'),
#       "accessory1": ('Clip [1]', 0, 'Sage Worm Card'),
#       "accessory2": ('Silver Ring', 0, 0)}

tt = {"headgear1": ("Ribbon [1]", "4", "Elder Willow Card"),
      "headgear2": ("Sunglasses", 0, "(No Card)"),
      "headgear3": ('Flu Mask', 0, "(No Card)"),
      "shield": ('Guard [1]', '7', "Ambernite Card"),
      "shoes": ('Sandals [1]', '4', "(No Card)"),
      "armor": ("Formal Suit [1]", "7", "(No Card)"),
      "robe": ("Muffler [1]", "7", "Raydric Card"),
      "accessory1": ("Glove [1]", 0, "Mantis Card"),
      'accessory2': ("Earring [1]", 0, "Zerom Card"),
      'weapon': ("Grimtooth", 0, "(No Card)", "(No Card)", "(No Card)", "(No Card)")}

gear_dict = dict_name_to_dict_id(tt)
pg = PlayerGear(gear_dict, 'hunter', 99)
igen = InterfaceGenerator(PlayerBuild(jbl, 96, 50, 'hunter', [9, 1, 99, 1, 99, 1], pg))
# igen.generate_equip_details(tt, 'female')
# igen.generate_interface()

igen.generate_resistance_details()
