import ROOT

df = ROOT.RDataFrame("myTree", "4000.root")
print(df.Describe())

df1 = ROOT.RDataFrame("myTree", ["4000.root", "4000.root"])
print(df1.Describe())

df2 = df.Filter("b1 < 1000")
print(df1.Describe())


