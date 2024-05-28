import ROOT
from ROOT import RDF

# df = ROOT.RDataFrame(4000).Define("a","(int) rdfentry_")
df = ROOT.RDataFrame("myTree", "4000.root")
filtered_df = df.Filter("b1%2==0")

# filtered_df.Snapshot("myTree", "filtered.root")
# df = ROOT.RDataFrame("myTree", "filtered.root")

print(filtered_df.Count().GetValue())
noded_filtered = RDF.AsRNode(filtered_df)
ROOT.Internal.RDF.ChangeBeginAndEndEntries(noded_filtered, 500, 1000)
print(noded_filtered.Count().GetValue())

# print(df.Count().GetValue())

# df_cached = filtered_df.Cache()

# print(f"Type of df: {df}")
# print(f"Type of filtered df: {filtered_df}")
# print(f"Type of cached df: {df_cached}")

# noded_filtered = RDF.AsRNode(filtered_df)
# noded_cached = RDF.AsRNode(df_cached)

# print(f"Type of noded filtered: {noded_filtered}")
# print(f"Type of noded cached: {noded_cached}")

# print("\n====================================\n")

# ROOT.Internal.RDF.ChangeBeginAndEndEntries(noded_filtered, 500, 1000)
# print(noded_filtered.Count().GetValue())

# print(noded_cached.Count().GetValue())
# ROOT.Internal.RDF.ChangeBeginAndEndEntries(noded_filtered, 50, 100)
# print(noded_filtered.Count().GetValue())

# ROOT.Internal.RDF.ChangeBeginAndEndEntries(noded_cached, 20, 30)
# print(noded_cached.Count().GetValue())

# ROOT.Internal.RDF.ChangeBeginAndEndEntries(noded_cached, 40, 70)
# print(noded_cached.Count().GetValue())

# noded_cached.Snapshot("myTree", "cached_df")

# noded_recreated = ROOT.RDataFrame("myTree", "cached_df")
# print(noded_recreated.Count().GetValue())

# print(noded_recreated)
# nd = RDF.AsRNode(noded_recreated)
# print(nd)

# ROOT.Internal.RDF.ChangeBeginAndEndEntries(nd, 50, 100)
# print(noded_recreated.Count().GetValue())

# print(df.Count().GetValue())
# print(df_cached.Count().GetValue())

# df_cached.Display().Print()
# noded_rdf = RDF.AsRNode(df_cached)

# ROOT.Internal.RDF.ChangeBeginAndEndEntries(noded_rdf, 1000, 2000)

# noded_rdf.Display().Print()
# print(noded_rdf.Describe())
# print(noded_rdf)
# print(df_cached)

# print(noded_rdf.Count().GetValue())



