# VSCodeCodexExtensionCustomizer

VS Code の Codex 拡張に、私個人が使いやすいようにしているローカルカスタマイズを再適用するための Codex Skill です。

このリポジトリは、`vscode-codex-extension-customizer` skill をほかの PC やプロジェクトへ持ち運びやすくするために公開しています。関連ユーティリティとして、複数プロジェクトの VS Code ウィンドウを見分けやすくする `vscode-workspace-add` skill も同梱しています。

## 重要な注意

このカスタマイズは、OpenAI や VS Code Codex 拡張の公式設定・公式機能ではありません。

インストール済み VS Code 拡張の内部ファイルを直接確認・編集するため、利用は自己責任です。拡張の更新、内部実装の変更、ファイル名の変更、配布形式の変更などにより、今後のバージョンで同じ手順が動作する保証はありません。

また、VS Code 拡張ディレクトリ配下の変更は、対象プロジェクトだけでなく、その PC のユーザー環境全体に影響します。作業前に必ずバックアップを作成し、変更内容を理解したうえで使ってください。

## 何をする Skill か

メインの Skill は、VS Code Codex 拡張に対して次の個人カスタマイズを確認・再適用するための手順を Codex に渡します。

- 新規セッション用プロンプトの 1 行目を Task/Thread 見出しとして使う
- Codex サイドバーの Tasks 表示を 20 件にする
- 拡張更新後に、カスタマイズが上書きされていないか確認する
- 変更前に日付付きバックアップを作成する
- Windows / macOS の現在 PC 上の拡張フォルダを確認してから作業する

関連ユーティリティの `vscode-workspace-add` skill は、VS Codeで複数のプロジェクトを並行して作業するときに、どのウィンドウがどのプロジェクトかを見分けやすくするための `.code-workspace` ファイルのベースを作成します。

生成される `.code-workspace` には、指定したプロジェクトを開く `folders.path` と、プロジェクトごとに区別しやすい `window.title` / `window.border` / `workbench.colorCustomizations` が入ります。作成されたファイルは、ダブルクリックするか、VS Code から開いて使う想定です。

## 構成

```text
.
├── README.md
├── vscode-workspace-add/
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   └── scripts/
│       └── create_workspace.py
└── vscode-codex-extension-customizer/
    ├── SKILL.md
    └── agents/
        └── openai.yaml
```

## 使い方

このリポジトリを取得したあと、使いたい skill ディレクトリを Codex が参照できる場所へ配置します。

例:

```text
Use $vscode-codex-extension-customizer at /path/to/vscode-codex-extension-customizer and check the latest VS Code Codex extension on this machine.
```

workspace 作成ユーティリティを使う場合:

```text
Use $vscode-workspace-add at /path/to/vscode-workspace-add and create a VS Code workspace file for /path/to/project.
```

Windows では、既定で次の拡張ディレクトリを確認します。

```text
%USERPROFILE%/.vscode/extensions
```

macOS では、既定で次の拡張ディレクトリを確認します。

```text
$HOME/.vscode/extensions
```

ただし、VS Code の設定やインストール方法によって拡張ディレクトリが異なる場合があります。必ず現在 PC 上の実パスを確認してから編集してください。

## 作業前チェック

- 最新の `openai.chatgpt-*` 拡張フォルダを確認する
- `out/extension.js` と `webview/assets/index-*.js` の存在を確認する
- 変更が必要かどうかを先に確認する
- 変更前に `*.bak-YYYY-MM-DD` 形式でバックアップを作成する
- プロジェクトごとの適用履歴と課題は、スキルを使った対象プロジェクトの `docs/` 配下に文書を作成して追記する
- VS Code 拡張の更新で上書きされる可能性を理解する

`vscode-workspace-add` を使う場合:

- 対象プロジェクトの絶対パスが存在することを確認する
- 既存の `.code-workspace` を上書きする場合は `--overwrite` を明示する
- 生成先の `workspaces/` ディレクトリが意図したリポジトリ配下であることを確認する
- 作成された `.code-workspace` は、ダブルクリックまたは VS Code から開いて利用する

## 対応環境の考え方

この Skill は、特定のバージョンや特定のユーザー名に固定しない方針です。

過去の私の環境では Windows の `C:/Users/<user>/.vscode/extensions/openai.chatgpt-<version>-win32-x64` 配下を確認していましたが、Mac では `$HOME/.vscode/extensions/openai.chatgpt-<version>-darwin-*` のようなパスになる可能性があります。

実際の suffix、CPU アーキテクチャ、ファイル名はバージョンや環境で変わるため、固定せずファイルシステムから探索してください。

## 免責

このリポジトリの内容は、私個人の作業環境での利便性を目的としたものです。

この手順を使ったことによる VS Code 拡張の不具合、設定の破損、作業環境への影響について、動作保証はありません。利用する場合は、必ず自己責任でバックアップを取り、必要に応じて拡張の再インストールや VS Code の再読み込みで復旧できるようにしてください。

## ライセンス

MIT License を採用しています。詳細は `LICENSE` を確認してください。

