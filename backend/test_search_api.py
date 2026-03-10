from database.db_init import init_database
from algorithm.search_algorithm import SearchAlgorithm
from database.models.scenic_model import Scenic

_, SessionLocal = init_database()
session = SessionLocal()

scenics = session.query(Scenic).all()
print(f'Total scenics: {len(scenics)}')

# Test search
keyword = '房山'
name_results = SearchAlgorithm.fuzzy_search(scenics, 'name', keyword)
desc_results = SearchAlgorithm.fuzzy_search(scenics, 'description', keyword)
addr_results = SearchAlgorithm.fuzzy_search(scenics, 'address', keyword)

print(f'Name results: {len(name_results)}')
print(f'Description results: {len(desc_results)}')
print(f'Address results: {len(addr_results)}')

# Merge results
seen_ids = set()
search_results = []
for result in name_results + desc_results + addr_results:
    if result.id not in seen_ids:
        search_results.append(result)
        seen_ids.add(result.id)

print(f'Total unique results: {len(search_results)}')
for r in search_results[:10]:
    print(f'  - {r.name} ({r.address})')

session.close()