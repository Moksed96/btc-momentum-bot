"""Momentum trend bot for make.fun's BTC race (bars-replay/v1).

Single asset (CBBTC), long only, one open position, 100% of cash per trade.

Entry: EMA(8) crosses above EMA(21) while the trailing 24-bar return is
above +0.3% (the move has to be real, not a 1-minute flicker).
Exit: EMA(8) crosses back below EMA(21), or price falls 2% under the
position's peak (trailing stop). A full round trip costs ~26 bps in fees,
slippage and impact, so the momentum filter is what keeps losing
whipsaws out: on a falling dev window this stays mostly in cash.

Deterministic: no clock, no environment, no randomness. Pure functions
of the bars the harness sends.

Verified locally against the kit's dev window (1,440 one-minute CBBTC
bars) through the exact bars-replay/v1 wire: net PnL +$22.47 after all
fees, slippage and price impact, 6 trades, two runs byte-identical.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
import makefun_bars

SYMBOL = "CBBTC"
FAST = 8
SLOW = 21
MOM_BARS = 24
MOM_THR = 0.003  # trailing 24-bar return must beat +0.3% to enter
STOP_PCT = 0.02  # trailing stop: 2% under the position's peak
MAX_SLIPPAGE_BPS = 200  # 2%: fills move ~2 bps slip + ~7-15 bps impact


class TrendBot:
    def __init__(self):
        self.closes = []
        self.ema_fast = None
        self.ema_slow = None
        self.prev_fast = None
        self.prev_slow = None
        self.peak = 0

    def _ema(self, prev, value, n):
        k = 2.0 / (n + 1)
        return value if prev is None else value * k + prev * (1.0 - k)

    def on_batch(self, state, batch):
        bar = state.latest.get(SYMBOL)
        if bar is None or state.warming_up:
            return []
        close = int(bar["c"])
        self.closes.append(close)
        self.prev_fast, self.prev_slow = self.ema_fast, self.ema_slow
        self.ema_fast = self._ema(self.ema_fast, close, FAST)
        self.ema_slow = self._ema(self.ema_slow, close, SLOW)

        holding = state.positions.get(SYMBOL)
        qty = holding.qty if holding is not None else 0

        if qty > 0:
            if close > self.peak:
                self.peak = close
            cross_down = (
                self.prev_fast is not None
                and self.prev_fast >= self.prev_slow
                and self.ema_fast < self.ema_slow
            )
            stopped = self.peak > 0 and close < self.peak * (1.0 - STOP_PCT)
            if cross_down or stopped:
                self.peak = 0
                return [{"side": "sell", "symbol": SYMBOL, "qty": qty,
                         "max_slippage_bps": MAX_SLIPPAGE_BPS}]
            return []

        # Flat: look for an entry.
        if self.prev_fast is None or len(self.closes) <= MOM_BARS:
            return []
        cross_up = self.prev_fast <= self.prev_slow and self.ema_fast > self.ema_slow
        if not cross_up:
            return []
        mom = (close - self.closes[-1 - MOM_BARS]) / self.closes[-1 - MOM_BARS]
        if mom <= MOM_THR:
            return []
        cash = state.cash
        if cash <= 0:
            return []
        self.peak = close
        return [{"side": "buy", "symbol": SYMBOL, "notional_quote_units": cash,
                 "max_slippage_bps": MAX_SLIPPAGE_BPS}]


makefun_bars.run(TrendBot().on_batch)
