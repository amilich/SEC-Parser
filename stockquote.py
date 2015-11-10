from yahoo_finance import Share
from parser import parse
import sys

def get_quote(ticker):
	return Share(ticker).get_price()

def get_pe_ratio(ticker):
	return Share(ticker).get_price_earnings_ratio()

def get_ebitda(ticker):
	ebitda = Share(ticker).get_ebitda()
	return float(ebitda[:-1]) * (10**6 if 'M' in ebitda[-1] else 10**9)

def get_fcf(ticker):
	try:
		num = parse(ticker)
		current_assets = num.next()
		ppe = num.next()
		current_liabilities = num.next()
	except StopIteration:
		return 'missing fcf'

	# print current_assets, current_liabilities, ppe
	return get_ebitda(ticker) - (current_assets - current_liabilities) - ppe 

ticker = raw_input('Enter ticker symbol: ').lower()
print get_quote(ticker)
print get_pe_ratio(ticker)
print get_ebitda(ticker)
print get_fcf(ticker)