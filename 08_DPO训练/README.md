# DPO 训练

本目录保存 Thinkers 项目的 DPO 训练配置、日志和过程记录。

## 训练设置
| 项目 | 记录值 |
| --- | --- |
| 基座模型 | Baichuan2-7B-Chat |
| 微调方式 | LoRA |
| LoRA rank / alpha / dropout | 8 / 32 / 0.1 |
| target_modules | W_pack |
| 训练轮数 | 1 epoch |
| 训练步数 | 1,288 |
| 最终 train loss | 0.516 |
| 训练框架 | LLaMA-Factory 0.1.8、PEFT 0.5.0 |

## 复现说明
训练过程依赖相应的模型权重和偏好数据，二者未包含在本仓库。日志中的 loss 用于描述训练过程，不能单独作为最终回答质量的证据；性能评价请结合 `../09_模型推理与评测` 中的评测流程。
