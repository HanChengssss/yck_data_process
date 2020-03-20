from tqdm import tqdm
import time
text = ""

# for char in tqdm(["a", "b", "c", "d"]):
#     text += char
#     time.sleep(1)


pbar = tqdm(total=1000, desc="进度")

for i in range(100):
    pbar.update(1)
    time.sleep(0.1)
pbar.close()