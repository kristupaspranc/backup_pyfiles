import ROOT
from ROOT import RDF
import types
from timeit import default_timer as timer

def get_df():
    df = ROOT.RDataFrame(10000)

    for i in range(2):
        df = df.Define(f"b{i}", "(int) rdfentry_")

    df.Snapshot("myTree", "10k.root")
    return df


def snapshot_df(df):
    df.Snapshot("myTree","40.root")

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

def create_generators(df, sz_chunk, sz_batch):
    gen_train, gen_validation = ROOT.TMVA.Experimental.CreateNumPyGenerators(
    rdataframe=df,
    batch_size=sz_batch,
    chunk_size=sz_chunk,
    target="b1",
    validation_split=0.3,
    shuffle=False,
    drop_remainder=False
    )

    for i in range(2):
        print("Training")
        i = 0
        for x, y in gen_train:
            print(x)
            print(y)
            i += 1

        print(f"Number of batches {i}")
        
        print("Validation")
        i = 0
        for x, y in gen_validation:
            print(x)
            print(y)
            i += 1
    
        print(f"Number of batches {i}")

if __name__ == "__main__":
    get_df()
    # snapshot_df(df)
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
    # verbosity = ROOT.Experimental.RLogScopedVerbosity(ROOT.Detail.RDF.RDFLogChannel(), ROOT.Experimental.ELogLevel.kDebug)
    # df = ROOT.RDataFrame("myTree", "60int.root")
    # df2 = ROOT.RDataFrame("myTree", "60int.root")
    # dff = df.Filter("b1 % 2 == 0", "name")

    # print(dff.Count().GetValue())
    # dff.Display(["b1","b2"], 30).Print()

    print("SMTH")

    # timed_list = []
    
    # for i in range(2):
    #     start = timer()
    #     df = ROOT.RDataFrame("myTree", "60int.root")
        
    #     create_generators(df, 20, 4)
    #     end = timer()
    #     timed_list.append(end - start)

    # print(timed_list)

    df = ROOT.RDataFrame("myTree", "20k300.root")
    dff = df.Filter("b1 % 5 == 0", "name")
        
    create_generators(dff, 20, 4)

    # for i in range(2):
    #     create_generators(df, 20 ,4)

    # create_generators(df, 20, 4)
    # create_generators(df2, 20, 4)

    # dff.Display().Print()
