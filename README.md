# vuln_server
アーキテクチャ構造情報（Draw.io） とASM／脆弱性管理ツールの検出結果 を統合し、実際に攻撃されやすい箇所を自動的に特定・優先度付けするモダンな仕組みを開発し、最終的に、視覚的に見えるものに可視化するためのベンチマークである。

# PoC Target Environment (Local)

This repository creates a local vulnerable target environment for PoC scanning:
- Juice Shop (http://localhost:3000)
- Vulnerable API (http://localhost:5050)
- Postgres, Redis, Adminer (http://localhost:8080)

## Run



## Notes
- Only run locally.
- The API deliberately contains insecure endpoints (`/eval`, `/search`) for PoC purposes.
- Use Nuclei, Nikto, ZAP against http://localhost:3000 and http://localhost:5050.
