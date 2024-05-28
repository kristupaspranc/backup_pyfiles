from __future__ import annotations

from typing import Any, Callable, Tuple, TYPE_CHECKING
import atexit

if TYPE_CHECKING:
    import numpy as np
    import tensorflow as tf
    import torch

import ROOT

def get_template(
        tree_name: str,
        file_names: list[str],
        columns: list[str] = list(),
        max_vec_sizes: dict[str, int] = dict(),
    ) -> Tuple[str, list[int]]:
        """
        Generate a template for the RBatchGenerator based on the given
        RDataFrame and columns.

        Args:
            file_name (str): name of the root file.
            tree_name (str): name of the tree in the root file.
            columns (list[str]): Columns that should be loaded.
                                 Defaults to loading all columns
                                 in the given RDataFrame
            max_vec_sizes (list[int]): The length of each vector based column.

        Returns:
            template (str): Template for the RBatchGenerator
        """

        # from cppyy.gbl.ROOT import RDataFrame
        from ROOT import RDataFrame

        x_rdf = RDataFrame(tree_name, file_names)

        if not columns:
            columns = x_rdf.GetColumnNames()

        template_dict = {
            "Bool_t": "bool&",
            "Double_t": "double&",
            "Double32_t": "double&",
            "Float_t": "float&",
            "Float16_t": "float&",
            "Int_t": "int&",
            "UInt_t": "unsigned int&",
            "Long_t": "long&",
            "ULong_t": "unsigned long&",
            "Long64_t": "long long&",
            "ULong64_t": "unsigned long long&",
            "Short_t": "short&",
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
        all_columns = []
        # Get the types of the different columns

        max_vec_sizes_list = []

        for name in columns:
            name_str = str(name)
            given_columns.append(name_str)
            column_type = template_dict[str(x_rdf.GetColumnType(name_str))]
            #column_type = template_dict[name_str]
            template_string += column_type + ","

            # if column_type in [
            #     "ROOT::RVec<bool>",
            #     "ROOT::RVec<double>",
            #     "ROOT::RVec<float>",
            #     "ROOT::RVec<int>",
            #     "ROOT::RVec<long>",
            #     "ROOT::RVec<Long64_t>",
            #     "ROOT::RVec<unsigned int>",
            #     "ROOT::RVec<unsigned long>",
            #     "ROOT::RVec<ULong64_t>"
            # ]:
            #     # Add column for each element if column is a vector
            #     if name_str in max_vec_sizes:
            #         max_vec_sizes_list.append(max_vec_sizes[name_str])
            #         for i in range(max_vec_sizes[name_str]):
            #             all_columns.append(f"{name_str}_{i}")

            #     else:
            #         raise ValueError(
            #             f"No max size given for feature {name_str}. \
            #             Given max sizes: {max_vec_sizes}"
            #         )

            # else:
            #     all_columns.append(name_str)

        return template_string[:-1], max_vec_sizes_list


if __name__=="__main__":
    get_template(
        tree_name = "myTree",
        file_names=["sonar.root"]
    )

    df = ROOT.RDataFrame("myTree","sonar.root")
    #print(df.GetColumnNames())
    print(df.GetColumnType("Col0"))
