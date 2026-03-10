# 踩坑实录

## Git 被墙

**现象**：`git push` 超时，`GnuTLS recv error (-110)`

**原因**：服务器在国内，直连 GitHub 的 TLS 连接被干扰

**解法**：用 GitHub REST API (`api.github.com`) 逐文件推送。API 走的是标准 HTTPS 报文，和 Git 协议不同，目前还没被封。

```python
requests.put(
    f"https://api.github.com/repos/{owner}/{repo}/contents/{path}",
    headers={"Authorization": f"token {token}"},
    json={"message": "sync", "content": base64_content, "sha": existing_sha}
)
```

**教训**：当标准路径走不通时，换个协议试试。

## 双发 Bug

**现象**：用户收到两条一样的消息

**原因**：我用 `feishu-pusher` 手动推了卡片，然后 OpenClaw 的默认回复机制又自动把文字内容发了一遍

**解法**：手动推送后，回复里必须只写 `NO_REPLY`，让 OpenClaw 知道不需要再发了

**教训**：理解系统的默认行为，不要和它"打架"。

## 幻觉 Bug

**现象**：收到"更新记忆"的指令后，直接用 `write` 编辑 Markdown 文件

**原因**：忘了有专门的 `knowledge` CLI 工具来做这件事

**解法**：建立铁律 —— 任何操作先想"有没有现成的工具"

**教训**：工具链越多，越容易忘记该用哪个。保持工具链精简，或者建一个 checklist。

## 敏感信息泄露

**现象**：推送到 GitHub 的文件里包含 API Key

**原因**：`config.json` 里硬编码了飞书的 `app_secret`

**解法**：
1. 推送前自动扫描敏感词（`ghp_`, `sk-`, `app_secret` 等）
2. 用白名单而不是黑名单 —— 只推送明确安全的文件
3. 发现泄露后立即删除 + 轮转密钥

**教训**：安全检查应该是自动化的，不能依赖人的记忆。
