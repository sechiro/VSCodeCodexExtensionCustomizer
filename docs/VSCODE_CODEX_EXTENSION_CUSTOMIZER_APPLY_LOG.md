# VS Code Codex Extension Customizer 適用履歴

この文書は、このリポジトリで管理する `vscode-codex-extension-customizer` の適用履歴と、適用ごとの課題を記録するための文書です。

各プロジェクトでこの Skill を使う場合も、プロジェクト固有の作業内容は対象プロジェクトの `docs/` 配下に置き、拡張本体の変更履歴だけでなく、検証結果・課題・再適用時の注意点を追えるようにします。

## 記録ルール

各適用履歴には、次を記録します。

- 実施日
- 対象OS・対象PC
- 対象拡張フォルダ
- 対象拡張バージョン
- 変更ファイル
- 作成したバックアップ
- 概要
- 手順
- 検証
- 適用ごとの課題・注意点

## 2026-04-29. 公開用 Skill の記録方式を `docs/` 配下の適用履歴管理へ汎用化

- 実施日: 2026-04-29
- 対象OS・対象PC: なし（今回は拡張本体へ未適用）
- 対象拡張フォルダ: なし
- 対象拡張バージョン: なし
- 変更ファイル: `README.md` / `vscode-codex-extension-customizer/SKILL.md` / `vscode-codex-extension-customizer/agents/openai.yaml` / `docs/VSCODE_CODEX_EXTENSION_CUSTOMIZER_APPLY_LOG.md`
- 作成したバックアップ: なし

### 概要

`vscode-codex-extension-customizer` の記録先を、特定のプロジェクト文書名に固定せず、各プロジェクトの `docs/` 配下で適用履歴と課題を管理する方針へ変更した。

### 手順

1. `vscode-codex-extension-customizer/SKILL.md` の文書更新手順を、特定ファイル名の更新から `docs/` 配下の適用ログ更新へ変更した。
2. 適用ごとの記録項目として、実施日、対象OS、拡張フォルダ、拡張バージョン、変更ファイル、バックアップ、検証結果、課題・注意点を明記した。
3. README の構成と作業前チェックに `docs/` 配下での適用履歴管理を追加した。
4. この公開リポジトリ自身も同じ形式に準じるため、本ファイルを `docs/` 配下に追加した。

### 検証

- `vscode-codex-extension-customizer/SKILL.md` に、`docs/` 配下で適用履歴を管理する方針が記載されている。
- `docs/VSCODE_CODEX_EXTENSION_CUSTOMIZER_APPLY_LOG.md` が存在する。
- 今回は VS Code 拡張本体への変更を行っていない。

### 適用ごとの課題・注意点

- 今回はスキルと管理文書の更新のみであり、実際の拡張バージョンに対する再適用検証は行っていない。
- 今後、拡張本体へ再適用した場合は、本ファイルへ対象バージョン、バックアップファイル、検証結果、発生した課題を追記する。
- 未確認 / 不確実（公式情報または一次情報が未確認）: Mac 版の実際の拡張フォルダ suffix は、対象PCで確認する必要がある。
