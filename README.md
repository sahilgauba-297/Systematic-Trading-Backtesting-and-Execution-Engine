# Systematic Trading Research Engine

Quantitative trading research framework for building, testing, and evaluating rule-based trading strategy with execution modeling.

---

## Overview

This project implements a complete systematic trading pipeline starting from raw market data and ending with performance evaluation under trading conditions. It simulates how a quantitative strategy behaves when transaction costs, slippage, and execution delays are included.

---

## Pipeline Description

- Market data is pulled using Yahoo Finance via yfinance  
- Core features are created including returns, rolling volatility, volume averages, and spread proxies  
- A rule based signal engine generates trading signals using momentum and volatility filters  
- Signals are converted into positions with next-bar execution to avoid lookahead bias  
- A backtesting engine simulates PnL including transaction costs and slippage  
- Walk-forward validation is used to test out-of-sample robustness  
- An execution realism layer models spread costs and volatility-based slippage  

---

## Strategy Logic

- Momentum-based directional signal using short and long window trends  
- Volatility filter to avoid unstable market regimes  
- Discrete positions: long, short, or flat  
- Execution occurs on the next time step to ensure no forward-looking bias  

---

## Execution Model

- Transaction costs based on trade activity  
- Slippage that increases with volatility  
- Spread-based cost approximation  
- Execution delay to simulate real trading behavior  
- Turnover tracking to measure trading frequency  

---

## Performance Summary (On SPY)

- Net Sharpe ratio around 1.1  
- Total return approximately 20%  
- Maximum drawdown around 11% 
- Turnover around 58  

---

## Visualizations

- Equity curve over time  
- Drawdown curve  
- Price with position overlay  

---

## Key Learnings

- Execution costs significantly impact strategy performance  
- Naive backtests overestimate returns  
- Volatility-adjusted slippage improves realism  
- Walk-forward testing reduces overfitting   

---

## Tech Stack

Python  
pandas  
numpy  
yfinance  
matplotlib  
Custom backtesting framework  
