## By Diyar Al-Nuaimi and Bailey Clarke

import numpy as np
import pandas as pd
import scipy as sp
import math

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
        # Initialise EMA tracking for Fun Drink, Coffee Beans and Milk
        self.alpha = 0.33
        self.fun_drink_ema = None
        self.coffee_bean_ema = None
        self.milk_ema = None
        self.goober_eats_ema = None
        self.coffee_ema = None
        self.jeans_ema = None
        self.pen_ema = None
        self.pens_going_up = True
        self.use_low = False
        self.use_high = False
        self.pen_start_day = 0
        self.delta = 0
        self.pen_model_works = True
        self.pen_adj_data = []
        self.jump_height = 0.07
        # SMA window for Fun Drink
        self.window_size = 20

        self.pen_data = {        
            "jumps": 3,
            "seasons": 5,
            "jump_diff": 7,
            "period_diff": 14
            }
    
    # Helper function to fetch the current price of an instrument
    def get_current_price(self, instrument):
        # return most recent price
        return self.data[instrument][-1]
    
    def position_expected_value(self, model_price, actual_price):
        if model_price is None:
            model_price = actual_price
        expected_value  = np.abs(model_price - actual_price) / actual_price
        return expected_value
    
    # Function for getting Fun Drink EMA
    def calculate_fun_drink_ema(self, current_price: float):
            """
            Calculate the EMA for Fun Drink prices.
            """
            if self.fun_drink_ema is None:
                # Initialise EMA with the first price
                self.fun_drink_ema = current_price
            else:
                # Update EMA based on the new price
                self.fun_drink_ema = self.alpha * current_price + (1 - self.alpha) * self.fun_drink_ema
            

    def calculate_coffee_bean_ema(self, current_price: float):
            """
            Calculate the EMA for Coffee Bean prices.
            """
            if self.coffee_bean_ema is None:
                # Initialise EMA with the first price
                self.coffee_bean_ema = current_price
            else:
                # Update EMA based on the new price
                self.coffee_bean_ema = self.alpha * current_price + (1 - self.alpha) * self.coffee_bean_ema


    def calculate_milk_ema(self, current_price: float):
            """
            Calculate the EMA for Milk prices.
            """
            if self.milk_ema is None:
                # Initialise EMA with the first price
                self.milk_ema = current_price
            else:
                # Update EMA based on the new price
                self.milk_ema = self.alpha * current_price + (1 - self.alpha) * self.milk_ema

    def calculate_jeans_ema(self, current_price: float):
            """
            Calculate the EMA for jeans prices.
            """
            if self.jeans_ema is None:
                # Initialize EMA with the first price
                self.jeans_ema = current_price
            else:
                # Update EMA based on the new price
                self.jeans_ema = self.alpha * current_price + (1 - self.alpha) * self.jeans_ema

    def calculate_pen_ema(self, current_price: float):
            """
            Calculate the EMA for pens prices.
            """
            if self.pen_ema is None:
                # Initialize EMA with the first price
                self.pen_ema = current_price
            else:
                # Update EMA based on the new price
                self.pen_ema = self.alpha * current_price + (1 - self.alpha) * self.pen_ema

    def is_jump_pens(self):
        if self.day >= 1:
            return abs(self.get_current_price("Red Pens") - self.data["Red Pens"][-2]) > self.jump_height*0.8
        return False
    
    def get_pen_notable_days(self):

        jumps = self.pen_data["jumps"]
        seasons = self.pen_data["seasons"]
        jump_diff = self.pen_data["jump_diff"]
        period_diff = self.pen_data["period_diff"]

        notable_days = []
        
        curr = self.pen_start_day
        for season in range(seasons):
            for jump in range(jumps):
                notable_days.append(curr)
                curr += jump_diff
            curr += jump_diff
            for jump in range(jumps):
                notable_days.append(-curr)
                curr += jump_diff
            curr += jump_diff
        
        return notable_days

    def predicted_delta_pens(self):

        if not self.pen_start_day:
            return 0
        
        notable_days = self.get_pen_notable_days()

        if (self.day + 1) in notable_days:
            return 0.1
        elif -(self.day + 1) in notable_days:
            return -0.1
        return 0
    
    def check_model_valid(self):
        notable_days = self.get_pen_notable_days()
        avg_diff = 0
        n=0
        for i in notable_days:
            if abs(i) <= self.day:
                avg_diff += (self.data["Red Pens"][abs(i)] - self.data["Red Pens"][abs(i)-1])*np.sign(i)
                n += 1
        
        if (avg_diff/n) > self.jump_height:
            self.pen_model_works = True
            return None
        else:
            for i in range(self.day):
                self.pen_start_day = i
                notable_days = self.get_pen_notable_days()
                avg_diff = 0
                n = 0
                for i in notable_days:
                    if abs(i) <= self.day:
                        avg_diff += (self.data["Red Pens"][abs(i)] - self.data["Red Pens"][abs(i)-1])*np.sign(i)
                        n += 1
                if (avg_diff/n) > self.jump_height:
                    self.pen_model_works = True
                    return None
        
        self.pen_model_works = False
    
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
    
        # Fintech Data Analysis
        n = 9

        past_n_days = range(max(self.day-n, 0), self.day+1)
        past_n_fintech = self.data["Fintech Token"][max(self.day-n, 0):]

        past_data = pd.DataFrame({"Days": past_n_days, "Price": past_n_fintech})

        # Thrifted Jeans Data Analysis
        jeans_data = pd.Series(self.data["Thrifted Jeans"])
        jeans_data = jeans_data.iloc[max(0, self.day - 250):self.day]

        m = 0
        c = 0
        if self.day < 10:
            m = 0
            c = jeans_data.mean()
        else:
            ones = np.array(np.ones(jeans_data.size))
            dates = np.array(list(range(jeans_data.size)))

            A = np.transpose(np.stack((ones, dates)))
            b = np.asarray(jeans_data.to_numpy())
            result = sp.optimize.lsq_linear(A, b)
            c, m = result.x

        self.calculate_jeans_ema(self.get_current_price("Thrifted Jeans"))
        lin_price = m*self.day + c
        p_price = self.jeans_ema + 0.006563358*(lin_price-self.get_current_price("Thrifted Jeans"))*abs((lin_price-self.get_current_price("Thrifted Jeans")))

        ### Find all Model Prices and calculate EV

        # Coffee EV
        coffee_model_price = 0.00794573 * self.get_current_price("Coffee Beans") + 0.15592097 * self.get_current_price("Milk") + 0.34666759 * self.get_current_price("Goober Eats") + 1.0241689
        coffee_ev = self.position_expected_value(coffee_model_price, self.get_current_price('Coffee')) 

        # Coffee Beans EV
        coffee_beans_model_price = self.coffee_bean_ema
        coffee_bean_ev = self.position_expected_value(coffee_beans_model_price, self.get_current_price('Coffee Beans')) 

        # Milk EV
        milk_model_price = self.milk_ema
        milk_ev = self.position_expected_value(milk_model_price, self.get_current_price('Milk'))
        
        # Goober Eats EV
        goober_eats_model_price = 0.17647295 * self.get_current_price("Coffee") - 0.00196047 * self.get_current_price("Coffee Beans") - 0.02582386 * self.get_current_price("Milk") + 1.28366124
        goober_eats_ev = self.position_expected_value(goober_eats_model_price, self.get_current_price('Goober Eats'))

        # Fun Drink EV
        fun_drink_model_price = self.fun_drink_ema
        fun_drink_ev = self.position_expected_value(fun_drink_model_price, self.get_current_price('Fun Drink')) 

        # UQ Dollar EV
        uq_dollar_model_price = 100
        uq_dollar_ev = self.position_expected_value(uq_dollar_model_price, self.get_current_price('UQ Dollar'))

        # Thrifted Jeans EV
        thrifted_jeans_model_price = p_price
        thrifted_jeans_ev = self.position_expected_value(thrifted_jeans_model_price, self.get_current_price('Thrifted Jeans'))

        # Fintech Token EV
        fintech_token_model_price = past_data["Price"].mean() 
        fintech_token_ev = self.position_expected_value(fintech_token_model_price, self.get_current_price('Fintech Token'))

        # Red Pens EV
        if (self.pen_model_works and self.predicted_delta_pens() != 0):
            red_pens_ev = self.jump_height / self.get_current_price('Red Pens')
        else:
            red_pens_ev = 0.01 / self.get_current_price('Red Pens')


        # Make Dictionary and order form highest to lowest

        ev_dict = {'Coffee': coffee_ev, 'Coffee Beans': coffee_bean_ev, 'Milk': milk_ev, 'Goober Eats': goober_eats_ev,
                'Fun Drink': fun_drink_ev, 'UQ Dollar': uq_dollar_ev, 'Thrifted Jeans': thrifted_jeans_ev,
                 'Fintech Token': fintech_token_ev, 'Red Pens': red_pens_ev }
        
        sorted_ev_vals = sorted(list(ev_dict.values()))[::-1]
        ev_keys = list(ev_dict.keys())
        sorted_ev_keys = []
        for ev in sorted_ev_vals:
            for key in ev_keys:
                if ev_dict[key] == ev:
                    sorted_ev_keys.append(key)
                    ev_keys.remove(key)
                    break
        

        # Coffee


        X = self.get_current_price("Coffee") - 0.00794573 * self.get_current_price("Coffee Beans") - 0.15592097 * self.get_current_price("Milk") - 0.34666759 * self.get_current_price("Goober Eats") - 1.0241689
          
        if X < 0:
            desiredPositions['Coffee'] = positionLimits['Coffee']

        elif X > 0:
            desiredPositions['Coffee'] = -positionLimits['Coffee']

      
       
        # Goober Eats

        Y = self.get_current_price("Goober Eats") - 0.17647295 * self.get_current_price("Coffee") + 0.00196047 * self.get_current_price("Coffee Beans") + 0.02582386 * self.get_current_price("Milk") - 1.28366124
        
        if Y < 0:
            desiredPositions["Goober Eats"] = positionLimits["Goober Eats"]

        else:
            desiredPositions["Goober Eats"] = -positionLimits["Goober Eats"]
       
        # UQ Dollar
        mu = 100

        if (self.get_current_price("UQ Dollar") - mu > 0):
            desiredPositions["UQ Dollar"] = -positionLimits["UQ Dollar"]
        elif (mu - self.get_current_price("UQ Dollar") > 0):
            desiredPositions["UQ Dollar"] = positionLimits["UQ Dollar"]

        # Thrifted Jeans

        delta = 0.5

        if (self.get_current_price("Thrifted Jeans") - p_price > delta):
            desiredPositions["Thrifted Jeans"] = -positionLimits["Thrifted Jeans"]
        elif (p_price-self.get_current_price("Thrifted Jeans") > delta):
            desiredPositions["Thrifted Jeans"] = positionLimits["Thrifted Jeans"]
        
        # Red Pens

        if self.is_jump_pens():
            if not self.pen_start_day:
                self.pen_start_day = self.day
            self.delta += self.get_current_price("Red Pens") - self.data["Red Pens"][-2]
       
        pen_data = pd.Series(self.data["Red Pens"])

        
        if self.pen_model_works and pen_data.iloc[-5:].mean() - pen_data.min() < 0.1 and pen_data.max() - pen_data.iloc[-5:].mean() > 0.1:
            self.jump_height = (pen_data.max() - pen_data.min() - 0.05)/4
            self.check_model_valid()
        
        if self.pen_model_works:

            self.pen_adj_data.append(self.get_current_price("Red Pens") - self.delta)
            self.calculate_pen_ema(self.pen_adj_data[-1])

            p_price = self.pen_ema + self.predicted_delta_pens()

            if p_price - self.pen_adj_data[-1] > 0:
                desiredPositions["Red Pens"] = positionLimits["Red Pens"]
            elif self.pen_adj_data[-1] - p_price > 0:
                desiredPositions["Red Pens"] = -positionLimits["Red Pens"] 

        else:
            bound = 0.05
            pen_data = pd.Series(self.data["Red Pens"])

            low_price_avg = pen_data[pen_data < pen_data.min() + bound].mean()
            high_price_avg = pen_data[pen_data > pen_data.max() - bound].mean()

            if self.get_current_price("Red Pens") - low_price_avg > 0.1:
                self.use_low = True
            if high_price_avg - self.get_current_price("Red Pens") > 0.1:
                self.use_high = True

            if not self.use_low and self.get_current_price("Red Pens") > 2 and self.get_current_price("Red Pens") < 2.7:
                low_price_avg = 2.21
            if not self.use_high and self.get_current_price("Red Pens") > 2 and self.get_current_price("Red Pens") < 2.7:
                high_price_avg = 2.46

            if self.get_current_price("Red Pens") < low_price_avg + bound:
                self.pens_going_up = True

                if self.get_current_price("Red Pens") > low_price_avg:
                    desiredPositions["Red Pens"] = -positionLimits["Red Pens"]
                elif self.get_current_price("Red Pens") < low_price_avg:
                    desiredPositions["Red Pens"] = positionLimits["Red Pens"]
            
            elif self.get_current_price("Red Pens") > high_price_avg - bound:
                self.pens_going_up = False

                if self.get_current_price("Red Pens") > high_price_avg:
                    desiredPositions["Red Pens"] = -positionLimits["Red Pens"]
                elif self.get_current_price("Red Pens") < high_price_avg:
                    desiredPositions["Red Pens"] = positionLimits["Red Pens"]

            else:
                if self.pens_going_up:
                    desiredPositions["Red Pens"] = positionLimits["Red Pens"]
                else:
                    desiredPositions["Red Pens"] = -positionLimits["Red Pens"]  
        
        # Fintech Token

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
        
        
        #  Fun Drink
     
        self.calculate_fun_drink_ema(self.get_current_price('Fun Drink'))

        if self.get_current_price('Fun Drink') < self.fun_drink_ema - 0.11:
            desiredPositions['Fun Drink'] = positionLimits['Fun Drink']
        elif self.get_current_price('Fun Drink') >= self.fun_drink_ema:
            desiredPositions['Fun Drink'] = -positionLimits['Fun Drink']
        
        

        # Coffe Beans EMA
        self.calculate_coffee_bean_ema(self.get_current_price('Coffee Beans'))

        if self.get_current_price('Coffee Beans') < self.coffee_bean_ema:
            desiredPositions['Coffee Beans'] = positionLimits['Coffee Beans']
        elif self.get_current_price('Coffee Beans') >= self.coffee_bean_ema:
            desiredPositions['Coffee Beans'] = -positionLimits['Coffee Beans']
        
        

        # Milk EMA

        self.calculate_milk_ema(self.get_current_price('Milk'))

        if self.get_current_price('Milk') < self.milk_ema:
            desiredPositions['Milk'] = positionLimits['Milk']
        elif self.get_current_price('Milk') >= self.milk_ema:
            desiredPositions['Milk'] = -positionLimits['Milk']
       

        totalpos = 0
        for instrument in sorted_ev_keys:
            pending = abs(desiredPositions[instrument])*self.get_current_price(instrument)
            if totalpos + pending > 500000:
                desiredPositions[instrument] = int(min(np.sign(desiredPositions[instrument])*((500000-totalpos)//self.get_current_price(instrument)), positionLimits[instrument]))

            totalpos += abs(desiredPositions[instrument])*self.get_current_price(instrument)

     
        return desiredPositions
 
