import decimal as d
from datetime import timedelta
from Alphas.RsiAlphaModel import RsiAlphaModel

class MovingAverageCrossAlgorithm(QCAlgorithm):

    def __init__(self):
        #self.sec = ["AAPL", "FB", "GOOGL"]
        self.symbol = "GOOGL"
        self.previous = None
        self.fast = None
        self.slow = None
    
    
    def Initialize(self):
        '''Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''

        self.SetStartDate(2018, 1, 1)    #Set Start Date
        self.SetEndDate(2018, 10, 1)      #Set End Date
        self.SetCash(100000)             #Set Strategy Cash
        
        self.AddSecurity(SecurityType.Equity, self.symbol, Resolution.Minute)
        
        
        self.slow = self.EMA(self.symbol, 50, Resolution.Daily)
        self.fast = self.EMA(self.symbol, 30, Resolution.Daily)
        
        self.rsi = self.RSI(self.symbol, 14)
      
    
        self.SetWarmUp(timedelta(days=50))
       

    def OnData(self, data):
        if not self.slow.IsReady:
            return
        
        if self.previous is not None and self.previous.date() == self.Time.date():
            return
    
        tolerance = 0.00015
    
        holdings = self.Portfolio[self.symbol].Quantity
    
        if not self.rsi.IsReady:
            return
        
        # finna long 
        if holdings <=0:
            if self.fast.Current.Value > self.slow.Current.Value * float(1+tolerance):
                    if self.rsi.Current.Value < 30:
                        self.Log("Buy >> {0}".format(self.Securities[self.symbol].Price))
                        self.SetHoldings(self.symbol, 1.0)
        #finna short 
        if holdings > 0 and self.fast.Current.Value < self.slow.Current.Value:
            if self.rsi.Current.Value > 70:
                self.Log("SELL >> {0}".format(self.Securities[self.symbol].Price))
                self.Liquidate(self.symbol)
            
        
        
        self.previous = self.Time
