'''
Code base was provided by basic template
Our stragey was turtle trading more can be learned here: https://bigpicture.typepad.com/comments/files/turtlerules.pdf
Help with coding was provided by this community thred: https://www.quantopian.com/posts/solved-turtle-trading-strategy
'''
import quantopian.algorithm as algo
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.filters import QTradableStocksUS
import math
import talib
import pandas as pd
from quantopian.pipeline.filters.morningstar import Q1500US, Q500US
from quantopian.algorithm import attach_pipeline, pipeline_output
 
def initialize(context):
    context.securities = [
        symbol('SPY')
        ] 
    
    # Rebalance every day, 1 hour after market open.
    algo.schedule_function(
        rebalance,
        algo.date_rules.every_day(),
        algo.time_rules.market_open(hours=1),
    )
 
    context.trade_percent = 0.01
    context.atrlength = 20
    context.portfolio_size = context.portfolio.cash + context.portfolio.positions_value
    context.recordme = pd.DataFrame({'symbols':[],'add_time':[],'last_buy_price':[]}) 
    
def rebalance(context, data):
 
    hist = data.history(context.securities, ['high', 'low', 'close'], 200, '1d')
    account_size = context.portfolio_size
    #Install a dataframe to hold buying records
 
    for sec in context.securities:
        ATR = talib.ATR(hist['high'][sec], hist['low'][sec], hist['close'][sec], timeperiod=context.atrlength)[-1]
        cur_price = data.current(sec, 'price')
        position = context.portfolio.positions[sec].amount
        unit = math.floor(account_size*0.01 / ATR) 
        
#Buy strategy here:
 
        if cur_price > hist['high'][sec][-20:-1].max() and position is 0:
            order(sec, unit)
            '''
            if len(recordme)!=0:                                                           
               recordme = recordme[recordme['symbols']!=sec] '''
            context.recordme = context.recordme.append(pd.DataFrame({'symbols':[sec],'add_time':[1],'last_buy_price':[cur_price]})) #record stock           
        elif sec in context.portfolio.positions: #buy 1 unit if sec price up 0.5N
            last_price =context.recordme[context.recordme['symbols'] == sec]['last_buy_price'].astype(float)
            #last_price= context.portfolio.positions[symbol('AAPL'),symbol('AMZN')].cost_basis
            add_price =(last_price[0] + 0.5 * ATR)
            add_unit = context.recordme[context.recordme['symbols']  == sec]['add_time'].astype(float)               
            log.info(context.recordme) 
            log.info(add_price)         
            
            if cur_price > add_price and add_unit[0] < 4:  #this is the point strategy stopped because nothing in it?
                unit = account_size*0.01 / ATR
                order(sec,unit) 
                context.recordme.loc[context.recordme['symbols']== sec,'add_time']=context.recordme[context.recordme['symbols']== sec]['add_time']+1
                context.recordme.loc[context.recordme['symbols']== sec,'last_buy_price']=cur_price
            
            if cur_price < (last_price[0] - 2*ATR):
                order_target_percent(sec,0)
                #After sell the stock, empty recordme
                context.recordme = context.recordme[context.recordme['symbols']!=sec]
    
