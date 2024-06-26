import argparse


from importlib.metadata import entry_points

from llm_merging.evaluation import * 
from llm_merging.data import * 

def all_merge_handlers():
    """Enumerate and Load (import) all merge methods."""
    discovered_merges = entry_points(group="llm_merging.merging.Merges")
    loaded_merges = {ep.name: ep.load() for ep in discovered_merges}
    return loaded_merges

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--merging_method", type=str, required=True)
    parser.add_argument("-b", "--eval_batch_size", type=int, default=2)
    parser.add_argument("-d", "--dataset_filepaths", type=str, default=None, nargs='+')
    args = parser.parse_args()

    # Load correct merging method 
    loaded_merges = all_merge_handlers()
    merge_method = loaded_merges[args.merging_method]()

    # Call the merge function. The merged model is stored under merging_method object 
    merge_method.merge()

    if args.dataset_filepaths is not None:
        # Evaluate method on datsets passed in (used for testing)
        evaluate_model(
            merge_method,
            None,
            args.dataset_filepaths,
            args.eval_batch_size
        )
    else:
        # Evaluate method on fixed datasets (used for developing method)
        evaluate_model(
            merge_method,
            ["boolq", "mawps"],
            None,
            args.eval_batch_size
        )

