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

INSERT INTO config_che300_major_info (model_id,Initial,brandid,brand_name,series_group_name,series_id,series_name,model_name,model_price,model_year,auto,liter,liter_type,gear_type,discharge_standard,max_reg_year,min_reg_year,car_level,seat_number,short_name,hl_configs,hl_configc,is_green,update_time,add_time) VALUES %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s

model_id,
Initial,
brandid,
brand_name,
series_group_name,
series_id,
series_name,
model_name,
model_price,
model_year,
auto,
liter,
liter_type,
gear_type,
discharge_standard,
max_reg_year,
min_reg_year,
car_level,
seat_number,
short_name,
hl_configs,
hl_configc,
is_green,
update_time,
add_time)
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s,
%s

