'''
Code base was provided by basic template
Our stragey was turtle trading more can be learned here: https://bigpicture.typepad.com/comments/files/turtlerules.pdf
Help with coding was provided by these community thred:
- https://www.quantopian.com/posts/turtle-trading-strategy
- https://www.quantopian.com/posts/solved-turtle-trading-strategy
'''
#import statements
import quantopian.algorithm as algo
import math
import talib
import pandas as pd

#main funtion and runs once
def initialize(context):
    context.securities = [
        symbol('QQQ'), #invesco QQQ trust
        ] 
    
    #triggers the rebalance every day 1 hour after market opens
    schedule_function(
        rebalance,
        algo.date_rules.every_day(),
        algo.time_rules.market_open(hours=1),
    )
 
    #initalizing global var that will be used later
    context.portfolio_size = context.portfolio.cash + context.portfolio.positions_value #calculates the portfolio size
    context.recordme = pd.DataFrame({'symbols':[],'add_time':[],'last_buy_price':[]}) #creates a dataframe

#analyzes the assets every day and makes decision
def rebalance(context, data):
    hist = data.history(context.securities, ['high', 'low', 'close'], 200, '1d') #history of security
    account_size = context.portfolio_size #creating local var for account
     
    #actual algo deciding for each security
    for sec in context.securities:
        ATR = talib.ATR(hist['high'][sec], hist['low'][sec], hist['close'][sec], timeperiod=20)[-1] #calculate the atr within 20 days
        cur_price = data.current(sec, 'price') #price of security 1 hour after market opens
        position = context.portfolio.positions[sec].amount #checking if any postions are already owned
        unit = math.floor(account_size*0.01 / ATR) #calculaitng the amout to buy depending on volatility'ATR'
        
        #buying statement
        if cur_price > hist['high'][sec][-20:-1].max() and position is 0:
            order(sec, unit) #orders 'sec' for x 'units'
            context.recordme = context.recordme.append(pd.DataFrame({'symbols':[sec],'add_time':[1],'last_buy_price':[cur_price]})) #record stock 
        
        #what to do if there are already bought the security before
        elif sec in context.portfolio.positions:
            last_price =context.recordme[context.recordme['symbols'] == sec]['last_buy_price'].astype(float) #var for previous price
            add_price =(last_price[0] + 0.5 * ATR) #caluvalting to check if more should be bought
            
            if cur_price > add_price:
                unit = math(account_size*0.01 / ATR) #recalulating the amount to buy
                order(sec,unit) #orders 'sec' for x 'units'
                context.recordme.loc[context.recordme['symbols']== sec,'add_time']=context.recordme[context.recordme['symbols']== sec]['add_time']+1 #update buy time
                context.recordme.loc[context.recordme['symbols']== sec,'last_buy_price']=cur_price #update the last buy price
            
            if cur_price < (last_price[0] - 2*ATR):
                order_target_percent(sec,0) #this means that no orders will be made
                context.recordme = context.recordme[context.recordme['symbols']!=sec] #empty recordme
