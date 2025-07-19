from extract_strat import Extract
# from model import Data


url = 'https://urbangadgets.ph/category/aerial-photography/drone/?srsltid=AfmBOoq2ykFbvAeqBvZOAVZN9OA0nx_RoFbIeE_uoKCTS55CkxhBEHbf'
scraped_data = Extract().execute(url)
print(scraped_data)

# data = Data(
#     title=scraped_data['title'],f
#     url=scraped_data['url']
#     )

# for item in data:    print(item)