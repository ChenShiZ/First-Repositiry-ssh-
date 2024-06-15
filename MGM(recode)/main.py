from x_transformers_ import TransformerWrapper,Encoder
import torch
from MLM import MLM
from torch.optim import Adam


from Data.dataPrepare import end_trajList
from Data.dataPrepare import end_poiEmbedding



variabley_traj=torch.Tensor(end_trajList).long().cuda()
variabley_poi=torch.Tensor(end_poiEmbedding).long().cuda()
epochs=10
batch=64

transformer=TransformerWrapper(
    num_tokens=501,
    max_seq_len=44,
    attn_layers=Encoder(
        dim=400,
        depth=5,
        heads=8
    )
).cuda()

trainer=MLM(
    transformer,
    mask_token_id=500,
    pad_token_id=500,
    mask_prob=0.25,
    replace_prob=0.90,
    mask_ignore_token_ids=[]
).cuda()

opt=Adam(trainer.parameters(),lr=3e-4)
opt.zero_grad()



for epoch in range(0,epochs):
    contloss=0
    for i in range(len(variabley_traj)):
        trajInput=variabley_traj[i]
        poiInput=variabley_poi[i]



