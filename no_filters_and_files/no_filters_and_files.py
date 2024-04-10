import ROOT

def generator():
    df = ROOT.RDataFrame(4000).Define("b1", "(int) rdfentry_").Define("b2", "(double) rdfentry_")
    df_filtered = df.Filter("b1 < 2001")
    
    gen_train, gen_validation = ROOT.TMVA.Experimental.CreatePyTorchGenerators(
        rdataframe=df_filtered,
        batch_size=400,
        chunk_size=2000,
        target="b2",
        validation_split=0.3,
        shuffle=False,
        drop_remainder=False
            )

    for x, y in gen_train:
        print(x)
        print(y.shape)

    for x, y in gen_validation:
        print(x)
        print(y.shape)

def check_report():
    df = ROOT.RDataFrame(100).Define("b1", "(int) rdfentry_").Define("b2", "(double) rdfentry_")
    print(df.Report().Print())

if __name__ == "__main__":
    generator()