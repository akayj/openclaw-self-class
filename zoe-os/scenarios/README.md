# 🧪 Zoe-OS Scenarios: Cross-Domain Validation

为了验证 Zoe-OS 的通用性，我们设定了三个互不重叠的验证沙盒。

---

## 1. 🛡️ Scenario: Physical Sentry (Hardware/Security)
- **Pressure (P)**: High Disk Usage (>90%) or Unauthorized SSH Attempts.
- **Balance (Bf)**: `zig-native-scanner` -> `bash (cleanup/block)`.
- **Memory (M)**: Store the pattern of "Safe Cleanup" to avoid deleting critical logs.

## 2. 📂 Scenario: Content Curater (Digital Assets)
- **Pressure (P)**: Directory Entropy (Mixed file types in `Downloads/`).
- **Balance (Bf)**: `python-brain` -> `analyze_semantic()` -> `move_file()`.
- **Memory (M)**: Store `.seed` slices of user preference (e.g., "Always group AI papers by Year").

## 3. 📡 Scenario: Market Scout (External API/Intel)
- **Pressure (P)**: Information Stagnation (New Tech Trends undetected).
- **Balance (Bf)**: `zoe-bus` -> `web_search_socket` -> `push_feishu()`.
- **Memory (M)**: Store which type of news the user interacts with most (Priority weighting).

---

## 🏁 Testing Standard
每一个场景必须通过以下测试才算合格：
1. **Sensing Accuracy**: 能否准确捕获对应维度的 Pressure 值。
2. **Execution Integrity**: 执行的 Action 是否能真实降低 Pressure。
3. **Recovery Speed**: 从 Sensing 到 Balance 的端到端时延。

---
*Architected by Xiao Xin | Direction by akayj*
