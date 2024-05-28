import pandas as pd
import ROOT
import torch

class Data():
    def __init__(self):
        self.x = torch.zeros(400, 2)
        self.x[:, 0] = torch.arange(-2, 2, 0.01)
        self.x[:, 1] = torch.arange(-2, 2, 0.01)
        w = torch.tensor([[1.0, 2.0], [2.0, 4.0]])
        b = 1
        func = torch.mm(self.x, w) + b    
        self.y = func + 0.2 * torch.randn((self.x.shape[0],1))

    def torch_to_csv(self, csv_name, column_names, x_and_y):
        if x_and_y:
            df = pd.DataFrame(torch.cat((self.x,self.y),1).numpy())
        else:
            df = pd.DataFrame(self.x.numpy())

        df.to_csv(csv_name,index=False,header=column_names)


def create_df(files):
    df = ROOT.RDataFrame(treeName, files)
    return df


def create_pandas_csv(file_name):
    d = {'col1': [1, 2], 'col2': ["string1", "string2"]}
    df = pd.DataFrame(data=d)
    df.to_csv(file_name, index=False, header=["b1","b2"])


def create_root_files(treeName, fileName1, fileName2, fileName3):
    #Create root data files with 400 rows x and y data and 400 rows with only x data
    #Only needed to run once
    data_creator = Data()
    data_creator.torch_to_csv(fileName1, ["a1","a2","a3","a4"], True)
    data_creator.torch_to_csv(fileName2, ["a1","a2"], False)

    csv_to_root(fileName1, treeName)
    csv_to_root(fileName2, treeName)

    #Create root data file with 2 columns and 2 rows, one column having int type and the other string type
    create_pandas_csv(fileName3)
    csv_to_root(fileName3, treeName)


def csv_to_root(csv_name, tree_name):
    ROOT.RDF.FromCSV(csv_name, True).Snapshot(tree_name, csv_name+".root")


if __name__ == "__main__":
    treeName = "myTree"
    file400xy = "400_rows"
    file400x = "400_xrows"
    fileINS = "ints_and_strings"

    # one run is sufficient
    #create_root_files(treeName, file400xy, file400x, fileINS)

    #create_df = lambda l: ROOT.RDataFrame(treeName, [x + ".root" for x in l])

    #df400 = create_df([file400xy, file400x])

    """clear error, has to be avoided when adding more than one data file"""
    #df400.Display("a3",800).Print()

    """the dataframe gets cut in the middle of processes by Count().GetValue()"""
    # print(df400.GetColumnNames())
    # print(df400.Describe())
    # df400.Display("a3",1).Print()
    # print(df400.GetColumnNames())
    # print(df400.Count().GetValue())
    # print(df400.GetColumnNames())
    # df400.Display("a3",1).Print()
    
    """by initiating first with the list of two columns, any exceeding of the second are cut"""
    # df400_inverted = create_df([file400x, file400xy])
    # print(df400_inverted.Describe())
    # print(df400_inverted.GetColumnNames())
    # print(df400_inverted.Count().GetValue())

    """the second column is typed as double meanwhile including strings
       also pay attention to column names: a1, a2"""
    # df_with_string = create_df([file400x,fileINS])
    # print(df_with_string.Describe())
    # print(df_with_string.Mean("a2").GetValue())
    # print(df_with_string.GetColumnNames())

    """the second type is string but the conversion might make sense if the user is not notified about it
       column names are now b1, b2"""
    # df_with_string_inverted = create_df([fileINS,file400x])
    #print(df_with_string_inverted.Describe())
    # print(df_with_string_inverted.GetColumnNames())

    #df400 = create_df([file400xy])
    #print(type(df400.Range(450).Count().GetValue()))

    gen_train, gen_validation = ROOT.TMVA.Experimental.CreateNumPyGenerators(
    tree_name=treeName,
    file_name=fileINS+".root",
    batch_size=4,
    chunk_size=4,
    target="a1",
    validation_split=0.3,
    shuffle=True,
    drop_remainder=False,
    )

    while True:
        try:
            print(next(gen_train)[0].shape)
        except StopIteration:
            break
    
    while True:
        try:
            print(next(gen_validation)[0].shape)
        except StopIteration:
            break

