import ROOT

tree_name = "myTree"
file_name = "4000_rows.root"
# file_name = "3999_rows.root"

def root_missing_data(sz_chunk):
    gen_train, gen_validation = ROOT.TMVA.Experimental.CreateNumPyGenerators(
    tree_name=tree_name,
    file_name=file_name,
    batch_size=400,
    chunk_size=sz_chunk,
    target="a1",
    validation_split=0.3,
    shuffle=True,
    drop_remainder=False,
    )

    print("Training")
    i = 1
    for x, y in gen_train:
        print(f"{i}. x: {x.shape}, y: {y.shape}")
        i += 1
    print("Validation")
    i = 1
    for x, y in gen_validation:
        print(f"{i}. x: {x.shape}, y: {y.shape}")
        i+=1

    # while True:
    #     try:
    #         print(next(gen_train)[0].shape)
    #     except StopIteration:
    #         break
    
    # while True:
    #     try:
    #         print(next(gen_validation)[0].shape)
    #     except StopIteration:
    #         break


def csv_to_root():
    ROOT.RDF.FromCSV("3999_rows", True).Snapshot(tree_name, "3999_rows.root")

if __name__ == "__main__":
    """
    Here is an example how some data is lost.
    I am uncertain, whether it is a feature or not, though.
    Here a batch generator is loaded with 4000 entries, splitting them into two chunks of 2000,
    with determined batch size of 400, validation split of 0.3.
    If it was a single 4000 chunk, it would generate 7 train batches and 3 validation batches,
    but under given parameters only 6 train batches and 2 validation batches are generated.

    The cause of this can be found in TMVA::Experimental::Internal::RBatchLoader.CreateTrainingBatches
    and TMVA::Experimental::Internal::RBatchLoader.CreateValidationBatches
    """
    # 6 and 2 split
    chunk_size1 = 2000
    root_missing_data(chunk_size1)

    # # 7 and 3 split
    # chunk_size2 = 4000
    # root_missing_data(chunk_size2)

    # given data is 3999, switch file_name to run
    # chunk_size3 = 4000
    # root_missing_data(chunk_size3)

    #csv_to_root()

    # for i in range(1,1000):
    #     try:
    #         print(i)
    #         root_missing_data(i)
    #     except:
    #         print(i)

    #root_missing_data(600)