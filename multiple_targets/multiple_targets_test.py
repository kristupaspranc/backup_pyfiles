import ROOT
import os
import math

def get_df():
    df = ROOT.RDataFrame(4000)\
            .Define("b1", "(Short_t) rdfentry_")\
            .Define("b2", "(UShort_t) b1 * b1")\
            .Define("b3", "(double) rdfentry_ * 10")\
            .Define("b4", "(double) b3 * 10")
    
    return df

file_name1 = "first_half.root"
file_name2 = "second_half.root"
tree_name = "mytree"

def define_rdf(num_of_entries=10):
        df = ROOT.RDataFrame(num_of_entries)\
            .Define("b1", "(int) rdfentry_")\
            .Define("b2", "(double) b1*b1")
        
        return df

def create_file(num_of_entries=10):
        define_rdf(num_of_entries).Snapshot(tree_name, file_name1)
    
def create_5_entries_file():
    df1 = ROOT.RDataFrame(5)\
        .Define("b1", "(int) rdfentry_ + 10")\
        .Define("b2", "(double) b1 * b1")\
        .Snapshot(tree_name, file_name2)

def teardown_file(file):
    os.remove(file)


def create_generators(df, sz_chunk):
    gen_train, gen_validation = ROOT.TMVA.Experimental.CreateNumPyGenerators(
    batch_size=400,
    chunk_size=sz_chunk,
    rdataframe=df,
    target=["b2","b3"],
    weights="b4",
    validation_split=0.3,
    shuffle=False
    )

    print("Train data")
    for x, y, z in gen_train:
        print(x.shape)
        print(y.shape)
        print(z.shape)

    print("Validation data")
    for x, y, z in gen_validation:
        print(x.shape)
        print(y.shape)
        print(z.shape)

def size_of_remainders(num_of_entries=10, batch_size=3, chunk_size=5, validation_split=0.3):
        first = ((num_of_entries // chunk_size) * math.ceil(chunk_size * validation_split))
        second = math.ceil((num_of_entries % chunk_size) * validation_split)
        print("First")
        print(first)
        print("Second")
        print(second)
        val_remainder = first + second
        print("Val remainder 1")
        print(val_remainder)
        val_remainder = ((num_of_entries // chunk_size) * math.ceil(chunk_size * validation_split))\
            + math.ceil((num_of_entries % chunk_size) * validation_split)
        print("Val remainder 2")
        print(val_remainder)
        train_remainder = num_of_entries - val_remainder
        n_of_train_batches = train_remainder // batch_size
        n_of_val_batches = val_remainder // batch_size
        val_remainder %= batch_size
        train_remainder %= batch_size

        return n_of_train_batches, n_of_val_batches, train_remainder, val_remainder

def test09_big_data():
    def define_rdf(num_of_entries):
        df = ROOT.RDataFrame(num_of_entries)\
            .Define("b1", "(int) rdfentry_")\
            .Define("b2", "(double) rb dfentry_ * 2")\
            .Define("b3", "(int) rdfentry_ + 10192")\
            .Define("b4", "(int) -rdfentry_")\
            .Define("b5", "(double) -rdfentry_ - 10192")
        
        return df
    
    def test(size_of_batch, size_of_chunk, num_of_entries):
        gen_train, gen_validation = ROOT.TMVA.Experimental.CreateNumPyGenerators(
        batch_size=size_of_batch,
        chunk_size=size_of_chunk,
        rdataframe=define_rdf(num_of_entries),
        target=["b3","b5"],
        weights="b2",
        validation_split=0.3,
        shuffle=False,
        drop_remainder=False
        )

        collect_x = []
        n_train_batches, n_val_batches, train_remainder, val_remainder =\
            size_of_remainders(num_of_entries=num_of_entries, batch_size=size_of_batch, chunk_size=size_of_chunk)

        print(f"Expected train batches: {n_train_batches}")

        i=0
        for _ in range(n_train_batches):
            try:
                x, y, z = next(gen_train)
                i += 1

                collect_x.extend(list(x[:,0]))
            except:
                 print(f"batches printed: {i}")
        
        print(f"Expected train batches: {n_train_batches}")
        print(f"Train batches: {i}")
        print(f"Train remainder {train_remainder}")

        if train_remainder:
            x, y, z = next(gen_train)
            print(x.shape)
            print(y.shape)
            print(z.shape)

        print("Validation ===================")

        i=0
        for _ in range(n_val_batches):
            x, y, z = next(gen_validation)
            i += 1
            print(x.shape)
            print(y.shape)
            print(z.shape)

            collect_x.extend(list(x[:,0]))
        
        print(f"Expected val batches: {n_val_batches}")
        print(f"Val batches: {i}")
        print(f"Val remainder {val_remainder}")

        if val_remainder:
            x, y, z = next(gen_validation)
            print(x.shape)
            print(y.shape)
            print(z.shape)

        # if val_remainder:
        #     x, y, z = next(gen_validation)
        #     print(x.shape)
        #     print(y.shape)
        #     print(z.shape)
        
    
    test(400, 2000, 100)

if __name__ == "__main__":
    #test09_big_data()

    df = ROOT.RDataFrame(100)
    dff = df.Define("a", "(int) rdfentry_")
    c = dff.Filter("a < 50")
    print(c.Count().GetValue())
    print(type(dff.GetColumnNames()))