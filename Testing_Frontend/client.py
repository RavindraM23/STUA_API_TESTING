import stua

stua.keyBus("6f064d4d-ed7d-415a-9d4a-c01204897506")
stua.keyLIRR("p4G33OQzU8acTdI6FbwCQ3C4bXKbmLFla5ZSDvdc")


li = []
for x in range(5):
    li.append(stua.gtfsLIRR())
    li[x].get("102", 0, x+1)

for x in range(5):
    li.append(stua.gtfsLIRR())
    li[x+5].get("102", 1, x+1)
    
stua.sort(li)
for info in li:
    print(f'{info.time} minutes ({info.service_description} with {info.vehicle})')