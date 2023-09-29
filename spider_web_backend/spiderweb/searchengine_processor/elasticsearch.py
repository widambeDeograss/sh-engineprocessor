from elasticsearch import Elasticsearch


class ElasticSearchProcessor:
    def __init__(self):
        self.es = Elasticsearch(hosts=["http://127.0.0.1:9200"])
        print(f"Connected to ElasticSearch cluster `{self.es.info().body['cluster_name']}`")

    def search_page_keywords(self, index_name, query, max_size):
        query = query.lower()
        tokens = query.split(" ")

        clauses = [
            {
                "span_multi": {
                    "match": {"fuzzy": {"page_content": {"value": i, "fuzziness": 5,
                                                         "max_expansions": 50,
                                                         "prefix_length": 0,
                                                         "rewrite": "constant_score"}}}
                }
            }
            for i in tokens
        ]

        payload = {
            "bool": {
                "must": [{"span_near": {"clauses": clauses, "slop": 0, "in_order": False}}]
            }
        }

        resp = self.es.search(index=index_name, query=payload, size=max_size)
        print(resp)
        return [result['_source'] for result in resp['hits']['hits']]
