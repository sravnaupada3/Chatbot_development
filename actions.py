# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import pandas as pd
import requests

# This is a simple example for a custom action which utters "Hello World!"
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionGetPerformance(Action):
    def name(self) -> Text:
        return "action_get_performance"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Implement the logic to fetch the necessary data
        # from your dataset (e.g., dfmf1) based on the user's query.
        # You can use Tracker to get entities from user input.

        # Example: Get the fund_symbol entity from user input
        fund_symbol = next(tracker.get_latest_entity_values("fund_symbol"), None)

        if fund_symbol:
            # Fetch performance data based on the fund_symbol
            performance_data = self.fetch_performance_data(fund_symbol)

            if performance_data:
                # Prepare the response message
                response = f"The performance of {fund_symbol} is as follows:\n"
                response += f"1-Year Return: {performance_data['1_year']}%\n"
                response += f"3-Year Return: {performance_data['3_years']}%\n"
                response += f"5-Year Return: {performance_data['5_years']}%\n"
                response += f"10-Year Return: {performance_data['10_years']}%\n"
                response += f"Last Bull Market Return: {performance_data['last_bull_market']}%\n"
                response += f"Last Bear Market Return: {performance_data['last_bear_market']}%\n"

                # Send the response back to the user
                dispatcher.utter_message(text=response)
            else:
                dispatcher.utter_message(text="I'm sorry, but I couldn't find performance data for that mutual fund.")
        else:
            dispatcher.utter_message(text="Please provide a valid mutual fund symbol.")

        return []
    
    def fetch_performance_data(self, fund_symbol: str) -> Dict[str, float]:
        dfmf1 = pd.read_csv('C:/Users/srava/TMU/wbot/data/mmf1.csv')
        fund_data = dfmf1[dfmf1['fund_symbol'] == fund_symbol]
        if not fund_data.empty:
            performance_data = {
                "1_year": fund_data.iloc[0]['fund_return_1year'],
                "3_years": fund_data.iloc[0]['fund_return_3years'],
                "5_years": fund_data.iloc[0]['fund_return_5years'],
                "10_years": fund_data.iloc[0]['fund_return_10years'],
                "last_bull_market": fund_data.iloc[0]['fund_return_last_bull_market'],
                "last_bear_market": fund_data.iloc[0]['fund_return_last_bear_market']
                }
            return performance_data
        else:
            return None

class ActionGetFundFamily(Action):
    def name(self) -> Text:
        return "action_get_fund_family"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Your logic to fetch the fund family based on the provided fund_symbol
        fund_symbol = tracker.get_slot("fund_symbol")
        fund_family = self.get_fund_family(fund_symbol)  # Replace with your data retrieval logic
        
        if fund_family:
            response = f"The mutual fund {fund_symbol} belongs to the {fund_family} family."
        else:
            response = f"Sorry, I couldn't find the fund family for {fund_symbol}. Please try again later."
        
        # Send the response to the user
        dispatcher.utter_message(text=response)

        return []
    
    def get_fund_family(self, fund_symbol: str) -> Dict[str, float]:
        dfmf1 = pd.read_csv('C:/Users/srava/TMU/wbot/data/mmf1.csv')
        fund_data = dfmf1[dfmf1['fund_symbol'] == fund_symbol]
        if not fund_data.empty:
            return fund_data.iloc[0]['fund_family']
        else:
            return None

class ActionGetFundInfo(Action):
    def name(self) -> Text:
        return "action_get_fund_info"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Implement the logic to fetch the necessary data
        # from your dataset (e.g., dfmf1) based on the user's query.
        # You can use Tracker to get entities from user input.

        # Example: Get the fund_symbol entity from user input
        fund_symbol = next(tracker.get_latest_entity_values("fund_symbol"), None)
        #fund_short_name = tracker.get_latest_entity_value("fund_short_name")

        if fund_symbol:
            # Fetch performance data based on the fund_symbol
            fund_data = self.fetch_fund_info(fund_symbol)

            if fund_data:
                # Prepare the response message
                response = f"The fund info of {fund_symbol} is as follows:\n"
                response += f"Fund category: {fund_data['fund_category']}\n"
                response += f"Fund Family: {fund_data['fund_family']}\n"
            else:
                response = f"I'm sorry, but I couldn't find info for {fund_symbol}."
        else:
            response = f"Please provide a valid mutual fund short name."
            
        dispatcher.utter_message(text=response)
        return []
    
    def fetch_fund_info(self, fund_symbol: str) -> Dict[str, float]:
        dfmf1 = pd.read_csv('C:/Users/srava/TMU/wbot/data/mmf1.csv')
        fund_info = dfmf1[dfmf1['fund_symbol'] == fund_symbol]
        if not fund_info.empty:
            fund_data = {
                "fund_category": fund_info.iloc[0]['fund_category'],
                "fund_family": fund_info.iloc[0]['fund_family']
                }
            return fund_data
        else:
            return None
        
class ActionCompareFunds(Action):
    def name(self) -> Text:
        return "action_compare_funds"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Implement the logic to fetch the necessary data
        # from your dataset (e.g., dfmf1) based on the user's query.
        # You can use Tracker to get entities from user input.

        # Example: Get the fund_symbol entity from user input
        fund_symbol_1 = tracker.get_slot("fund_symbol")
        fund_symbol_2 = next(tracker.get_latest_entity_values("fund_symbol"), None)

        if fund_symbol_1 and fund_symbol_2:
            # Fetch performance data based on the fund_symbol
            fund_data_1 = self.fetch_fund_performance(fund_symbol_1)
            fund_data_2 = self.fetch_fund_performance(fund_symbol_2)

            if fund_data_1 and fund_data_2:
                # Prepare the response message
                response = f"Comparing the performance of {fund_symbol_1} and {fund_symbol_2}:\n"
                response += f"1-Year Return: {fund_data_1['1_year']}% vs. {fund_data_2['1_year']}%\n"
                response += f"3-Year Return: {fund_data_1['3_years']}% vs. {fund_data_2['3_years']}%\n"
                response += f"5-Year Return: {fund_data_1['5_years']}% vs. {fund_data_2['5_years']}%\n"
                response += f"10-Year Return: {fund_data_1['10_years']}% vs. {fund_data_2['10_years']}%\n"
                response += f"Last Bull Market Return: {fund_data_1['last_bull_market']}% vs. {fund_data_2['last_bull_market']}%\n"
                response += f"Last Bear Market Return: {fund_data_1['last_bear_market']}% vs. {fund_data_2['last_bear_market']}%\n"
            else:
                response = f"I'm sorry, but I couldn't find performance data for both {fund_symbol_1} and {fund_symbol_2}."
        else:
            response = "Please provide valid mutual fund symbols to compare."
            
        dispatcher.utter_message(text=response)
        return []
    
    def fetch_fund_performance(self, fund_symbol: str) -> Dict[str, float]:
        dfmf1 = pd.read_csv('C:/Users/srava/TMU/wbot/data/mmf1.csv')
        fund_info = dfmf1[dfmf1['fund_symbol'] == fund_symbol]

        if not fund_info.empty:
            fund_data = {
                    "1_year": fund_info.iloc[0]['fund_return_1year'],
                    "3_years": fund_info.iloc[0]['fund_return_3years'],
                    "5_years": fund_info.iloc[0]['fund_return_5years'],
                    "10_years": fund_info.iloc[0]['fund_return_10years'],
                    "last_bull_market": fund_info.iloc[0]['fund_return_last_bull_market'],
                    "last_bear_market": fund_info.iloc[0]['fund_return_last_bear_market']
                }
            return fund_data
        else:
            return None
        
class ActionGetStockData(Action):
    def name(self) -> Text:
        return "action_get_stock_data"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Fetch stock symbol entity from user input
        stock_symbol = next(tracker.get_latest_entity_values("stock_symbol"), None)

        if stock_symbol:
            # Fetch stock data from Alpha Vantage API
            stock_data = self.fetch_stock_data(stock_symbol)

            if stock_data:
                # Prepare the response message
                response = f"Here is the stock data for {stock_symbol}:\n"
                response += f"Open Price: {stock_data['open']}\n"
                response += f"High Price: {stock_data['high']}\n"
                response += f"Low Price: {stock_data['low']}\n"
                response += f"Close Price: {stock_data['close']}\n"
                response += f"Volume: {stock_data['volume']}\n"
            else:
                response = f"I'm sorry, but I couldn't fetch data for {stock_symbol}."
        else:
            response = f"Please provide a valid stock symbol."

        dispatcher.utter_message(text=response)
        return []
    
    def fetch_stock_data(self, stock_symbol: str) -> Dict[str, Any]:
        # Replace 'YOUR_API_KEY' with your Alpha Vantage API key
        api_key = 'HWH3C73NNZOQSAGV'
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_symbol}&apikey={api_key}'
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if 'Global Quote' in data:
                    stock_data = data['Global Quote']
                    return {
                        "open": stock_data['02. open'],
                        "high": stock_data['03. high'],
                        "low": stock_data['04. low'],
                        "close": stock_data['05. price'],
                        "volume": stock_data['06. volume']
                    }
        except Exception as e:
            # Handle exceptions and errors here
            pass
        
        return None
    
class ActionGetEFTPerformance(Action):
     def name(self) -> Text:
        return "action_get_etf_performance"
    
     def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        etf_symbol = next(tracker.get_latest_entity_values("etf_symbol"), None)

        if etf_symbol:
            performance_data = self.fetch_etf_performance_data(etf_symbol)

            if performance_data:
                response = f"The performance of {etf_symbol} is as follows:\n"
                response += f"1-Year Return: {performance_data['1_year']}%\n"
                response += f"3-Year Return: {performance_data['3_years']}%\n"
                response += f"5-Year Return: {performance_data['5_years']}%\n"
                response += f"10-Year Return: {performance_data['10_years']}%\n"
                response += f"Sharpe Ratio (5 Years): {performance_data['fund_sharpe_ratio_5years']}\n"
                response += f"Treynor Ratio (5 Years): {performance_data['fund_treynor_ratio_5years']}"

                dispatcher.utter_message(text=response)
            else:
                dispatcher.utter_message(text="I'm sorry, but I couldn't find performance data for that ETF.")
        else:
            dispatcher.utter_message(text="Please provide a valid ETF symbol.")

        return []
    
     def fetch_etf_performance_data(self, etf_symbol: str) -> Dict[str, float]:
        # Implement the logic to fetch the necessary data from your dataset (e.g., dfmf1) based on the user's query.
        # Replace the following line with your data retrieval logic for ETF performance data.
        df_etf = pd.read_csv('C:/Users/srava/TMU/wbot/data/metf1.csv')
        etf_data = df_etf[df_etf['fund_symbol'] == etf_symbol]

        if not etf_data.empty:
            performance_data = {
                "1_year": etf_data.iloc[0]['fund_return_1year'],
                "3_years": etf_data.iloc[0]['fund_return_3years'],
                "5_years": etf_data.iloc[0]['fund_return_5years'],
                "10_years": etf_data.iloc[0]['fund_return_10years'],
                "fund_sharpe_ratio_5years": etf_data.iloc[0]['fund_sharpe_ratio_5years'],
                "fund_treynor_ratio_5years": etf_data.iloc[0]['fund_treynor_ratio_5years']
            }
            return performance_data
        else:
            return None

class ActionGetETFFamily(Action):
    def name(self) -> Text:
        return "action_get_etf_family"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        etf_symbol = tracker.get_slot("etf_symbol")
        fund_family = self.get_etf_family(etf_symbol)  # Replace with your data retrieval logic for ETF family
        
        if fund_family:
            response = f"The ETF {etf_symbol} belongs to the {fund_family} family."
        else:
            response = f"Sorry, I couldn't find the ETF family for {etf_symbol}. Please try again later."
        
        dispatcher.utter_message(text=response)

        return []
    
    def get_etf_family(self, etf_symbol: str) -> Dict[str, float]:
        # Implement the logic to fetch the fund family based on the provided ETF symbol.
        # Replace the following line with your data retrieval logic for ETF family.
        df_etf = pd.read_csv('C:/Users/srava/TMU/wbot/data/metf1.csv')
        etf_data = df_etf[df_etf['fund_symbol'] == etf_symbol]

        if not etf_data.empty:
            return etf_data.iloc[0]['fund_family']
        else:
            return None

class ActionGetETFInfo(Action):
    def name(self) -> Text:
        return "action_get_etf_info"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        etf_symbol = next(tracker.get_latest_entity_values("etf_symbol"), None)

        if etf_symbol:
            fund_data = self.fetch_etf_info(etf_symbol)

            if fund_data:
                response = f"Here is some information about {etf_symbol}:\n"
                response += f"Fund Category: {fund_data['fund_category']}\n"
                response += f"Fund Family: {fund_data['fund_family']}"
            else:
                response = f"I'm sorry, but I couldn't find information for {etf_symbol}."
        else:
            response = f"Please provide a valid ETF symbol."
            
        dispatcher.utter_message(text=response)
        return []
    
    def fetch_etf_info(self, etf_symbol: str) -> Dict[str, float]:
        # Implement the logic to fetch the necessary data from your dataset (e.g., dfmf1) based on the user's query.
        # Replace the following line with your data retrieval logic for ETF information.
        df_etf = pd.read_csv('C:/Users/srava/TMU/wbot/data/metf1.csv')
        fund_info = df_etf[df_etf['fund_symbol'] == etf_symbol]

        if not fund_info.empty:
            fund_data = {
                "fund_category": fund_info.iloc[0]['fund_category'],
                "fund_family": fund_info.iloc[0]['fund_family']
            }
            return fund_data
        else:
            return None

class ActionCompareETF(Action):
    def name(self) -> Text:
        return "action_compare_etf"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        fund_symbol_1 = tracker.get_slot("etf_symbol")
        fund_symbol_2 = next(tracker.get_latest_entity_values("etf_symbol"), None)

        if fund_symbol_1 and fund_symbol_2:
            fund_data_1 = self.fetch_fund_performance(fund_symbol_1)
            fund_data_2 = self.fetch_fund_performance(fund_symbol_2)

            if fund_data_1 and fund_data_2:
                response = f"Comparing the performance of {fund_symbol_1} and {fund_symbol_2}:\n"
                response += f"1-Year Return: {fund_data_1['1_year']}% vs. {fund_data_2['1_year']}%\n"
                response += f"3-Year Return: {fund_data_1['3_years']}% vs. {fund_data_2['3_years']}%\n"
                response += f"5-Year Return: {fund_data_1['5_years']}% vs. {fund_data_2['5_years']}%\n"
                response += f"10-Year Return: {fund_data_1['10_years']}% vs. {fund_data_2['10_years']}%"
            else:
                response = f"I'm sorry, but I couldn't find performance data for both {fund_symbol_1} and {fund_symbol_2}."
        else:
            response = "Please provide valid ETF symbols to compare."
            
        dispatcher.utter_message(text=response)
        return []
    
    def fetch_fund_performance(self, fund_symbol: str) -> Dict[str, float]:
        # Implement the logic to fetch the necessary data from your dataset (e.g., dfmf1) based on the user's query.
        # Replace the following line with your data retrieval logic for ETF performance data.
        df_etf = pd.read_csv('C:/Users/srava/TMU/wbot/data/metf1.csv')
        etf_data = df_etf[df_etf['fund_symbol'] == fund_symbol]

        if not etf_data.empty:
            performance_data = {
                "1_year": etf_data.iloc[0]['fund_return_1year'],
                "3_years": etf_data.iloc[0]['fund_return_3years'],
                "5_years": etf_data.iloc[0]['fund_return_5years'],
                "10_years": etf_data.iloc[0]['fund_return_10years']
            }
            return performance_data
        else:
            return None
