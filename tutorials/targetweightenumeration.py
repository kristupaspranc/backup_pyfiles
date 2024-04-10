import ROOT


def fill_tree(treeName, fileName):
    df = ROOT.RDataFrame(10000)
    df.Define("b1", "(double) rdfentry_")\
      .Define("b2", "(int) rdfentry_ * rdfentry_")\
      .Define("b3", "(int) rdfentry_")\
      .Define("b4", "(double) rdfentry_").Snapshot(treeName, fileName)
 
# We prepare an input tree to run on
fileName = "df001_introduction_py.root"
treeName = "myTree"
fill_tree(treeName, fileName)
 
 
# We read the tree from the file and create a RDataFrame, a class that
# allows us to interact with the data contained in the tree.
d = ROOT.RDataFrame(treeName, fileName)

batch_size = 128
chunk_size = 5_000
 
# ds_train, ds_validation = ROOT.TMVA.Experimental.CreateTFDatasets(
#     treeName,
#     fileName,
#     batch_size,
#     chunk_size,
#     target=["b2","b4"], 
#     weights="b3",
#     validation_split=0.3,
#     shuffle=True,
# )
 
# # Loop through training set
# for i, (b, t, w) in enumerate(ds_train):
#     print(f"Training batch {i} => {b.shape} => weight {w.shape} => target {t.shape}")
 
 
# # Loop through Validation set
# for i, (b, t, w) in enumerate(ds_validation):
#     print(f"Validation batch {i} => {b.shape} => weight {w.shape} => target {t.shape}")


print(d.GetColumnNames())