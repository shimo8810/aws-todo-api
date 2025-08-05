---
applyTo: "**"
---

# git 設定

## commit メッセージ
- コミットメッセージは英語で記述する
- commit メッセージは `<type>[optional scope]: <description>` の形式で記載する
- `<type>` は `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore` を使用する
    - `feat`: 新機能の追加
    - `fix`: バグ修正
    - `docs`: ドキュメントの変更
    - `style`: コードのフォーマットやスタイルの変更（機能に影響しない）
    - `refactor`: リファクタリング（機能に影響しないコードの変更）
    - `perf`: パフォーマンス改善
    - `test`: テストの追加や修正
    - `chore`: ビルドプロセスや補助ツールの変更
- `<optional scope>` は省略可能で、変更の範囲を示す
    - 例: `feat(lang): add polish language`
- `<description>` は変更内容を簡潔に記述する
- 例: `feat(auth): add login functionality`
- `<description>` はすべて小文字で記載する
- 破壊的変更がある場合は`<type>`の後に`!`を付ける
    - 例: `feat(api)!: send an email to the customer when a product is shipped`