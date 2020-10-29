import pandas as pd
import quantopian.algorithm as algo
import math
import talib
import numpy
 
def initialize(context):
    context.securities = [
        symbol('AMZN'),
        symbol('GOOG'),
        symbol('FB')
        ]
    context.spy = sid(8554)
    context.trends = []
    context.portfolio_size = context.portfolio.cash + context.portfolio.positions_value
    schedule_function(
        handle_trading,
        date_rules.every_day(),
        time_rules.market_open(hours=1),
    )
    
def get_uptrend(context, data):
    spy_hist = data.history(context.spy, 'price', 200, '1d')
    spy_sma = spy_hist.mean()
    if spy_hist[-1] > spy_sma:
        return True
    return False

def handle_trading(context, data):
    hist_2 = data.history(context.securities, ['price','high', 'low', 'close'], 200, '1d')
    for sec in context.securities:
        open_orders = get_open_orders()
        trend = get_uptrend(context, data)
        cur_price = data.current(sec, 'price')
        context.trends.append(trend)
        hist = data.history(sec, 'price', 50, '1d')
        ATR = talib.ATR(hist_2['high'][sec], hist_2['low'][sec], hist_2['close'][sec], timeperiod = 20)[-1]
        sma_50 = hist.mean()
        sma_20 = hist[-20:].mean()
        log.info('Price: %s'%(hist[-1]))
        log.info('Moving 50: %d'%(sma_50))
        log.info('Moving 20: %d'%(sma_20))
        log.info('ATR: %d'%(ATR))
        
        #if hist[-1]<
        
        if context.trends[-1] == False and context.trends[-2] == False:
            # it is a downtrend.
            order_target_percent(sec, -1.0/len(context.securities))
        else:
            # it is an uptrend.
            if sma_20 > sma_50 and not sec in open_orders:
                if cur_price < (sma_50+ATR*0.5):
                    order_target_percent(sec, 1)
                    
            elif sma_50 > sma_20 and sec not in open_orders:
                if cur_price < (sma_20-ATR*2):
                    order_target_percent(sec, -0.5)
