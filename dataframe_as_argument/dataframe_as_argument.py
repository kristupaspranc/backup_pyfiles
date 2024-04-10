import ROOT
from ROOT import RDF

def get_df():
    df = ROOT.RDataFrame(4000)\
            .Define("b1", "(Short_t) rdfentry_")\
            .Define("b2", "(UShort_t) rdfentry_ * rdfentry_")
    
    return df


def create_generators(df, sz_chunk):
    gen_train, gen_validation = ROOT.TMVA.Experimental.CreateNumPyGenerators(
    rdataframe=df,
    batch_size=400,
    chunk_size=sz_chunk,
    target="b2",
    validation_split=0.3,
    shuffle=False,
    drop_remainder=False
    )

    i = 0
    print("Train data")
    for x, y in gen_train:
        print(x.shape)
        print(y.shape)
        i += 1

    print("Validation data")
    for x, y in gen_validation:
        print(x.shape)
        print(y.shape)
        pass
    
    print(i)

def snapshot_df(df):
    df.Snapshot("myTree","4000.root")

def get_template(df):
    columns = list()
    if not columns:
        columns = df.GetColumnNames()

    template_dict = {
            "Bool_t": "bool&",
            "bool":"bool&",
            "Double_t": "double&",
            "Double32_t": "double&",
            "double": "double&",
            "Float_t": "float&",
            "Float16_t": "float&",
            "float": "float&",
            "Int_t": "int&",
            "int": "int&",
            "UInt_t": "unsigned int&",
            "unsigned int": "unsigned int&",
            "Long_t": "long&",
            "ULong_t": "unsigned long&",
            "Long64_t": "long long&",
            "ULong64_t": "unsigned long long&",
            "Short_t": "short&",
            "short": "short&",
            "UShort_t": "unsigned short&",
            
            "ROOT::VecOps::RVec<bool>": "ROOT::RVec<bool>",
            "ROOT::VecOps::RVec<double>": "ROOT::RVec<double>",
            "ROOT::VecOps::RVec<float>": "ROOT::RVec<float>",
            "ROOT::VecOps::RVec<int>": "ROOT::RVec<int>",
            "ROOT::VecOps::RVec<long>": "ROOT::RVec<long>",
            "ROOT::VecOps::RVec<Long64_t>": "ROOT::RVec<Long64_t>",
            "ROOT::VecOps::RVec<unsigned int>": "ROOT::RVec<unsigned int>",
            "ROOT::VecOps::RVec<unsigned long>": "ROOT::RVec<unsigned long>",
            "ROOT::VecOps::RVec<ULong64_t>": "ROOT::RVec<ULong64_t>"
        }
    
    template_string = ""

    given_columns = []

    for name in columns:
        name_str = str(name)
        given_columns.append(name_str)
        print(given_columns)
        print(str(df.GetColumnType(name_str)))
        column_type = template_dict[str(df.GetColumnType(name_str))]

        template_string += column_type + ","

    print(template_string)

if __name__ == "__main__":
    # df = get_df()
    # df2 = ROOT.RDataFrame("myTree", "4000.root")

    """template if ROOT.RDF.RInterface<ROOT::Detail::RDF::RLoopManager,void>"""
    # get_template(df)
    # b = get_template(df2)
    # if a==b:
    #     print("EQUAL")
    # print(type(df.Range(1000)))
    #create_generators(df, 2000)

    """if defined then it is not an rdataframe anymore"""
    # print("dataframe type if created on fly")
    # print(type(df))
    # print("dataframe type if created from the root file")
    # print(type(df2))
    # print(isinstance(df2, ROOT.RDataFrame))
    
    """instance"""
    df = ROOT.RDataFrame("myTree", "4000.root")
    dff = ROOT.RDF.AsRNode(df)
    dff = dff.Filter("b1%2==0")
    print("Generating batches")
    create_generators(dff, 1000)
