from database.db_init import init_database
from algorithm.search_algorithm import SearchAlgorithm
from database.models.scenic_model import Scenic

_, SessionLocal = init_database()
session = SessionLocal()

scenics = session.query(Scenic).all()
print(f'Total scenics: {len(scenics)}')

# Test search
keyword = '房山'
results = SearchAlgorithm.fuzzy_search(scenics, 'name', keyword)
print(f'Found {len(results)} results for keyword "{keyword}":')
for r in results[:10]:
    print(f'  - {r.name} ({r.address})')

session.close()