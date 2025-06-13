from extract_strat import Extract

url = 'https://geeksforgeeks.org'
data = Extract().execute(url)
print(str(data))