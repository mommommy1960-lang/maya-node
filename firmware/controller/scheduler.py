# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
# 
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

import time
class PowerScheduler:
    def __init__(self, sensors, actuators):
        self.s = sensors; self.a = actuators
        self.last_forecast = 0

    def update_forecasts(self):
        if time.time() - self.last_forecast < 5:
            return
        self.gen_forecast = self.s.irradiance_forecast(6*60)  # 6h horizon
        self.load_forecast = self.s.load_forecast(6*60)
        self.last_forecast = time.time()

    def dispatch(self):
        soc = self.s.battery_soc()
        p_load = self.s.load_now()
        p_gen = self.s.gen_now()
        reserve = self.s.reserve_kw()

        # Priority tiers: P1 critical, P2 important, P3 deferrable
        p1, p2, p3 = self.s.load_breakdown()
        headroom = p_gen + self.a.inverter_limit_kw() + self.a.genset_kw()- p1

        if soc < 0.15:        # brownout guard
            self.a.shed("P3"); self.a.shed("P2")
            self.a.start_genset(min_kw=p1 + reserve)
        elif headroom >= (p2 + p3):
            self.a.charge_battery(rate_kw=min(headroom, self.a.max_charge_kw()))
            self.a.enable_all_loads()
        else:
            self.a.defer("P3"); self.a.enable("P2")
            if soc < 0.35 and p_gen < p_load:
                self.a.start_genset(min_kw=p1 + p2 + reserve)
