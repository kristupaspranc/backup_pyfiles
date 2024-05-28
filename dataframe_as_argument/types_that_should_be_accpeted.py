import ROOT

# df = ROOT.RDataFrame("myTree", "4000.root")
# print(str(df.Describe())[15:21])

# df1 = ROOT.RDataFrame("myTree", ["4000.root", "4000.root"])
# print(df1.Describe())

# df2 = df.Filter("b1 < 1000")
# print(df1.Describe())

tree = ROOT.TTree("tree","title")
df = ROOT.RDataFrame(tree)
# print(str(df.Describe())[15:20])

gen_train, gen_validation = ROOT.TMVA.Experimental.CreateNumPyGenerators(
    rdataframe=df,
    batch_size=400,
    chunk_size=2000,
    target="b2",
    validation_split=0.3,
    shuffle=False,
    drop_remainder=False
    )

