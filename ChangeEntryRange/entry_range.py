import ROOT
from ROOT import RDF

def empty():
    df1 = ROOT.RDataFrame(50)
    dff = RDF.AsRNode(df1)
    ROOT.Internal.RDF.ChangeEmptyEntryRange(dff, (30,40))
    b = dff.Define("a", "rdfentry_")
    print(b.Count().GetValue())

# df = ROOT.RDataFrame(200).Define("a", "rdfentry_")
# df.Snapshot("tree", "file")
df = ROOT.RDataFrame("tree", "file")
print(df.Describe())

noded_rdf = RDF.AsRNode(df)

ROOT.Internal.RDF.ChangeBeginAndEndEntries(noded_rdf, 10, 15)

print(noded_rdf.Count().GetValue())
noded_rdf.Display("a", 20).Print()

ROOT.Internal.RDF.ChangeBeginAndEndEntries(noded_rdf, 20, 30)

print(noded_rdf.Count().GetValue())
noded_rdf.Display("a", 20).Print()
