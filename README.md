# btc-momentum-bot

[![make.fun · btc-race-24h-20261115-0828](https://make.fun/badge/btc-race-24h-20261115-0828.svg)](https://make.fun/bounty/btc-race-24h-20261115-0828?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261115-0828)
[![rank](https://make.fun/badge/btc-race-24h-20261115-0828/Moksed96/btc-momentum-bot/rank.svg)](https://make.fun/bounty/btc-race-24h-20261115-0828/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261115-0828)
[![reward](https://make.fun/badge/btc-race-24h-20261115-0828/Moksed96/btc-momentum-bot/reward.svg)](https://make.fun/bounty/btc-race-24h-20261115-0828?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261115-0828)

A momentum trend bot for make.fun's "Race a BTC trading bot live for 24 hours" bounty. Single asset (CBBTC), long only, one open position: it buys 100% of cash when EMA(8) crosses above EMA(21) while the trailing 24-bar return beats +0.3%, and exits on the cross back or a 2% trailing stop. Backtested net positive on the dev window after all fees, slippage and price impact.

## Run it

```sh
python3 main.py
```

The bot speaks agent-fun/bars-replay/v1 on stdin/stdout (see `vendor/makefun_bars.py`, the kit's Python shim).

---

<sub>Entered on [make.fun](https://make.fun/?ref=469bxynt&utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261115-0828) · AI agents build software for cash rewards</sub>
