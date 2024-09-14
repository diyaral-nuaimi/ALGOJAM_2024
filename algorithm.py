import numpy as np
import pandas as pd
import scipy as sp
import math
# Reading CSV files
df1 = pd.read_csv('data/Coffee_price_history.csv')
df2 = pd.read_csv('data/Coffee Beans_price_history.csv')
df3 = pd.read_csv('data/Milk_price_history.csv')

# Extracting prices
coffee_beans_price = df1['Price'].to_numpy()  
milk_price = df3['Price'].to_numpy()          
coffee_price = df2['Price'].to_numpy()  

class Algorithm():
    ########################################################
    # NO EDITS REQUIRED TO THESE FUNCTIONS
    ########################################################
    # FUNCTION TO SETUP ALGORITHM CLASS
    def __init__(self, positions):
        # Initialise data stores:
        # Historical data of all instruments
        self.data = {}
        # Initialise position limits
        self.positionLimits = {}
        # Initialise the current day as 0
        self.day = 0
        # Initialise the current positions
        self.positions = positions
        # Initialize EMA tracking for Fun Drink
        self.alpha = 0.05
        self.fun_drink_ema = None
    
    # Helper function to fetch the current price of an instrument
    def get_current_price(self, instrument):
        # return most recent price
        return self.data[instrument][-1]
    
    # Function for getting Fun Drink EMA
    def calculate_fun_drink_ema(self, current_price: float):
            """
            Calculate the EMA for Fun Drink prices.
            """
            if self.fun_drink_ema is None:
                # Initialize EMA with the first price
                self.fun_drink_ema = current_price
            else:
                # Update EMA based on the new price
                self.fun_drink_ema = self.alpha * current_price + (1 - self.alpha) * self.fun_drink_ema

    ########################################################
    # RETURN DESIRED POSITIONS IN DICT FORM
    def get_positions(self):
        # Get current position
        currentPositions = self.positions
        # Get position limits
        positionLimits = self.positionLimits
        
        # Declare a store for desired positions
        desiredPositions = {}
         # Function to calculate the EMA for Fun Drink
        
        # Loop through all the instruments you can take positions on.
        for instrument, positionLimit in positionLimits.items():
            # For each instrument initialize desired position to zero
            desiredPositions[instrument] = 0

            # Iterate through the price data
            
            # Coffee
            
            X = self.get_current_price("Coffee") - 0.00794573 * self.get_current_price("Coffee Beans") - 0.15592097 * self.get_current_price("Milk") - 0.34666759 * self.get_current_price("Goober Eats") - 1.0241689
                
            if X < 0:
                desiredPositions['Coffee'] = positionLimits['Coffee']
                # desiredPositions['Coffee Beans'] = -min(0.00794573 * positionLimits['Coffee'], positionLimits['Coffee Beans'])
                # desiredPositions['Milk'] = -min(0.15592097 * positionLimits['Coffee'], positionLimits['Milk'])
            elif X > 0:
                desiredPositions['Coffee'] = -positionLimits['Coffee']
                # desiredPositions['Coffee Beans'] = min(0.00794573 * positionLimits['Coffee'], positionLimits["Coffee Beans"])
                # desiredPositions['Milk'] = min(0.15592097 * positionLimits['Coffee'], positionLimits['Milk'])
            
            
            # Goober Eats

            Y = self.get_current_price("Goober Eats") - 0.17647295 * self.get_current_price("Coffee") + 0.00196047 * self.get_current_price("Coffee Beans") + 0.02582386 * self.get_current_price("Milk") - 1.28366124
            
            if Y < 0:
                desiredPositions["Goober Eats"] = positionLimits["Goober Eats"]
                #desiredPositions["Coffee"]  = -min(math.floor(0.17647295 * positionLimits["Goober Eats"]), positionLimits["Coffee"])
                #desiredPositions["Coffee Beans"] = min(math.floor(0.00196047 * positionLimits["Goober Eats"]), positionLimits["Coffee Beans"])
                #desiredPositions["Milk"] = min(math.floor(0.02582386 * positionLimits["Goober Eats"]), positionLimits["Milk"])
            else:
                desiredPositions["Goober Eats"] = -positionLimits["Goober Eats"]
                #desiredPositions["Coffee"]  = min(math.floor(0.17647295 * positionLimits["Goober Eats"]), positionLimits["Coffee"])
                #desiredPositions["Coffee Beans"] = -min(math.floor(0.00196047 * positionLimits["Goober Eats"]), positionLimits["Coffee Beans"])
                #desiredPositions["Milk"] = -min(math.floor(0.02582386 * positionLimits["Goober Eats"]), positionLimits["Milk"])
            
            # Coffee Beans
            
            Z = self.get_current_price("Coffee Beans") - 54.5995236 * self.get_current_price('Coffee') + 26.46366311 * self.get_current_price('Goober Eats') + 5.18856219 * self.get_current_price('Milk') - 7.100818
            
            if Z < 0:
                desiredPositions['Coffee Beans'] = positionLimits['Coffee Beans']
            else:
                desiredPositions['Coffee Beans'] = -positionLimits['Coffee Beans']
            
            
            # Milk
            W = self.get_current_price('Milk') - 4.96640643 * self.get_current_price('Coffee') + 1.61582382 * self.get_current_price('Goober Eats') + 0.02405081 * self.get_current_price('Coffee Beans') + 5.89756392

            if W < 0:
                desiredPositions['Milk'] = positionLimits['Milk']
            else:
                desiredPositions['Milk'] = -positionLimits['Milk']
            
            
            """
            # Goober Eats
            goober_price = self.get_current_price("Goober Eats")
            
            if goober_price < 1.4960273972602738:
                desiredPositions['Goober Eats'] = positionLimits['Goober Eats']
            else:
                desiredPositions['Goober Eats'] = -positionLimits['Goober Eats']
            """
            
            mu = 100
            delta = 0.1

            if (self.get_current_price("UQ Dollar") - mu > delta):
                desiredPositions["UQ Dollar"] = -positionLimits["UQ Dollar"]
            elif (mu - self.get_current_price("UQ Dollar") > delta):
                desiredPositions["UQ Dollar"] = positionLimits["UQ Dollar"]
            
            # Thrifted Jeans

            #past_n_days = sorted(list(self.data.keys()))[max(self.day-n, 0):self.day+1]
            #ones = np.ones(len(past_n_days))
            #vals = [self.data[day] for day in past_n_days]

            m = 0.0735
            c = 45.267

            p_price = m*self.day + c

            delta = 1.5

            if (self.get_current_price("Thrifted Jeans") - p_price > delta):
                desiredPositions["Thrifted Jeans"] = -positionLimits["Thrifted Jeans"]
            elif (p_price-self.get_current_price("Thrifted Jeans") > delta):
                desiredPositions["Thrifted Jeans"] = positionLimits["Thrifted Jeans"]
            
            # Fintech Token
            n = 9

            past_n_days = range(max(self.day-n, 0), self.day+1)
            past_n_fintech = self.data["Fintech Token"][max(self.day-n, 0):]

            past_data = pd.DataFrame({"Days": past_n_days, "Price": past_n_fintech})

            if (past_data["Price"].std() > 30):
                if past_data["Price"].mean() - self.get_current_price("Fintech Token") > 0:
                    desiredPositions["Fintech Token"] = -positionLimits["Fintech Token"]
                elif past_data["Price"].mean() - self.get_current_price("Fintech Token") < 0:
                    desiredPositions["Fintech Token"] = positionLimits["Fintech Token"]

            else:
                if past_data["Price"].mean() - self.get_current_price("Fintech Token") > 0:
                    desiredPositions["Fintech Token"] = positionLimits["Fintech Token"]
                elif past_data["Price"].mean() - self.get_current_price("Fintech Token") < 0:
                    desiredPositions["Fintech Token"] = -positionLimits["Fintech Token"]
            

            # Fun Drink
            self.calculate_fun_drink_ema(self.get_current_price('Fun Drink'))

            if self.get_current_price('Fun Drink') < self.fun_drink_ema:
                desiredPositions['Fun Drink'] = positionLimits['Fun Drink']
            else:
                desiredPositions['Fun Drink'] = -positionLimits['Fun Drink']
            
        return desiredPositions
 
