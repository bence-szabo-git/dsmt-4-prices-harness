from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from prices import load_prices


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "figures" / "unilever-vs-apple-2025.png"
TICKERS = {
    "AAPL": ("Apple (AAPL)", "#555555"),
    "ULVR.L": ("Unilever (ULVR.L)", "#1F36C7"),
}


def main() -> None:
    fig, ax = plt.subplots(figsize=(10, 5.5), layout="constrained")
    plotted_dates = []

    for ticker, (label, color) in TICKERS.items():
        prices = load_prices(ticker)
        prices = prices.loc["2025-01-01":"2025-12-31", "Close"].dropna()
        if prices.empty:
            raise ValueError(f"No 2025 closing prices found for {ticker}")
        change = (prices / prices.iloc[0] - 1) * 100
        ax.plot(change.index, change, label=label, color=color, linewidth=1.8)
        plotted_dates.extend(change.index)

    start = min(plotted_dates).strftime("%Y-%m-%d")
    end = max(plotted_dates).strftime("%Y-%m-%d")
    ax.set_title(f"Unilever vs Apple: change in closing price ({start} to {end})")
    ax.set_ylabel("Change since first day (%)")
    ax.set_xlabel("Date")
    ax.axhline(0, color="#999999", linewidth=0.8, zorder=0)
    ax.grid(axis="y", color="#DDDDDD", linewidth=0.7)
    ax.legend(frameon=False)
    ax.text(
        1,
        0,
        "Source: Yahoo Finance",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=8,
        color="#666666",
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
