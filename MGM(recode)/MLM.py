import torch
from torch import nn
import torch.nn.functional as F
import math
from functools import reduce


# 随机生成一张与t形状相同的布尔张量，其中与prob对比，小于prob的为true其余为false
def prob_mask_like(t,prob):
    return torch.zero_like(t).float().uniform_(0,1)<prob

# 根据传入的token_ids生成与t相同形状的张量，id为true表示掩码
def mask_with_tokens(t,token_ids):
    init_no_mask=torch.full_like(t,False,dtype=torch.bool)
    mask=reduce(lambda acc,el:acc|(t==el),token_ids,init_no_mask)
    return mask

# 根据传入掩码张量mask和prob生成一个新的掩码张量new_mask
# 根据概率prob随机选择一部分位置为true，其余位置为false
def get_mask_subset_with_prob(mask,prob):
    batch,seq_len,device=*mask.shape,mask.device
    max_masked=math.ceil(prob*seq_len)

    # 计算每个样本中的mask个数
    num_tokens=mask.sum(dim=-1,keepdim=True)
    mask_excess=(mask.cumsum(dim=-1)>(num_tokens*prob).ceil())
    mask_excess=mask_excess[:,:max_masked]

    rand_mask=torch.rand((batch,seq_len),device=device).masked_fill(~mask,-1e9)
    _,sampled_indices=rand_mask.topk(max_masked,dim=-1)
    sampled_indices=(sampled_indices+1).masked_fill_(mask_excess,0)

    new_mask=torch.rand((batch,seq_len+1),device=device)
    new_mask.scatter_(-1,sampled_indices,1)

    return new_mask[:,1:].bool()

class MLM(nn.modules):
    def __init__(
            self,
            transformer,
            mask_prob=0.15,
            replace_prob=0.9,
            num_tokens=None,
            random_token_prob=0.,
            mask_token_id=2,

            #这个参数什么含义
            pad_token_id=0,
            mask_ignore_token_ids=[]
    ):
        super.__init__()
        self.transformer = transformer

        # mlm related probabilities

        self.mask_prob = mask_prob
        self.replace_prob = replace_prob

        self.num_tokens = num_tokens
        self.random_token_prob = random_token_prob

        # token ids

        self.pad_token_id = pad_token_id
        self.mask_token_id = mask_token_id
        self.mask_ignore_token_ids = set([*mask_ignore_token_ids, pad_token_id])


    def forward(self,seq,time_seq,**kwargs):
        no_mask=mask_with_tokens(seq,self.mask_ignore_token_ids)
        mask=get_mask_subset_with_prob(~no_mask,self.mask_prob)

        masked_seq=seq.clone().detach()

        lables=seq.masked_fill(~mask,self.pad_token_id)

        if self.random_token_prob>0:
            assert self.num_tokens is not None,"num_tokens"

            random_token_prob=prob_mask_like(seq,self.random_token_prob)
            random_tokens=torch.randint(0,self.num_tokens,seq.shape,device=seq.device)
            random_no_mask = mask_with_tokens(random_tokens, self.mask_ignore_token_ids)
            random_token_prob &= ~random_no_mask
            masked_seq = torch.where(random_token_prob, random_tokens, masked_seq)

            # remove tokens that were substituted by random to be [mask]ed later
            mask = mask & ~random_token_prob

        replace_prob=prob_mask_like(seq,self.replace_prob)
        masked_seq=masked_seq.masked_fill(mask*replace_prob,self.mask_token_id)

        logits=self.transformer(masked_seq,time_seq,**kwargs)

        mlm_loss=F.cross_entropy(
            logits.transpose(1,2),
            lables,
            ignore_index=self.pad_token_id
        )

        return mlm_loss
