from joblib import Memory

# Define the directory where cache files will be stored
cachedir = "./my_cache_dir"
mem = Memory(cachedir, verbose=0)


@mem.cache
def heavy_calculation(x, y):
    print("Computing...")
    return x + y
