import ROOT
from ROOT import RDF

df = ROOT.RDataFrame("myTree", "400.root")
df2 = ROOT.RDataFrame(10).Define("b1", "(int) rdfentry_")
df3 = ROOT.RDataFrame("myTree", ["40.root","400.root"])

df_noded = RDF.AsRNode(df)
df2_noded = RDF.AsRNode(df2)
df3_noded = RDF.AsRNode(df3)

print(ROOT.Internal.RDF.TTreeTChainOrigin(df))
print(ROOT.Internal.RDF.TTreeTChainOrigin(df2_noded))
print(ROOT.Internal.RDF.TTreeTChainOrigin(df3_noded))