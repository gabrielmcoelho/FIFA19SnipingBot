from utils import *

class FilterController():
    def __init__(self, alt_positions=0, alt_chem_styles=0, pos_mod_price=False, target_min_price=0, target_max_price=0):
        self.alt_positions = alt_positions
        self.alt_chem_styles = alt_chem_styles
        self.pos_mod_price = pos_mod_price
        self.min_price_direction = "up"
        self.target_min_price = target_min_price
        self.target_max_price = target_max_price

    def _next_value(self, value, direction):
        if direction == "up":
            if value < 1000:
                return 50
            elif value >= 1000 and value < 10000:
                return 100
            else:
                return 250
        elif direction == "down":
            if value <= 1000:
                return 50
            elif value > 1000 and value <= 10000:
                return 100
            else:
                return 250

    def manage_filter(self, d, counter, cur_filter):
        updated_filters = {}
        if self.alt_chem_styles != 0:
            if counter != 0 and counter % self.alt_chem_styles == 0:
                if cur_filter.chem_style:
                    updated_filters["chem_style"] = ("Estilos Entrosam.", None)
                else:
                    updated_filters["chem_style"] = ("Estilos Entrosam.", "BÁSICO")

        if self.alt_positions != 0:
            if counter != 0 and counter % self.alt_positions == 0:
                if cur_filter.position:
                    updated_filters["position"] = ("Posição", None)
                else:
                    updated_filters["position"] = ("Posição", "Defensores")

                if self.pos_mod_price:
                    cur_max = get_max_price_textbox(d)
                    if cur_max == self.target_max_price:
                        retry_cmd(find_click_inc_max_price, 0.02, 0, d)
                    elif cur_max == self.target_max_price + self._next_value(cur_max, "up"):
                        retry_cmd(find_click_dec_max_price, 0.02, 0, d)
                    else:
                        raise ValueError(f"{cur_max} is not expected to be max_price at any moment.")
        
        cur_min = get_min_price_textbox(d)
        if cur_min == self.target_min_price:
            self.min_price_direction = "up"
        elif cur_min == self.target_max_price - self._next_value(self.target_max_price, direction="down"):
            self.min_price_direction = "down"

        if self.min_price_direction == "up":
            retry_cmd(find_click_inc_min_price, 0.02, 0, d)
        elif self.min_price_direction == "down":
            retry_cmd(find_click_dec_min_price, 0.02, 0, d)

        cur_filter.update(d, **updated_filters)