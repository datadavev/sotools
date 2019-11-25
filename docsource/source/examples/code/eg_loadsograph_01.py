# Load a Dataset from json-ld, normalize schema.org namespace, and dump as ttl.
import sotools
import json
json_source = "source/examples/data/ds_bad_namespace.json"
g = sotools.loadSOGraph(filename=json_source,
                        publicID="https://my.data.net/data/",
                        normalize=True,
                        deslop=True)

print("Loaded JSON:")
print(json.dumps(json.load(open(json_source, 'r')), indent=2))
print("\nNormalized schema.org namespace and serialized to ttl:\n")
print(g.serialize(format="ttl").decode())
