---
applyTo: "**"
---

# Python テスト設定

## 基本設定
- テストは `pytest` を使用して実行する
- テストファイルは `tests` ディレクトリ内に配置する
- pytestによるテストは関数ベースで記述する
- テスト関数は `test_` で始める
- テスト関数名は `test_{function name}_{condition}` の形式で記述する
    - 例: `test_addition_with_positive_numbers`
- テストが実装されるディレクトリはコードのディレクトリ構造に合わせる
    - コードは `app` ディレクトリに配置
    - テストは `tests` ディレクトリに配置
    - 例: `tests/test_module.py` は `module.py` のテスト
- `tests` ディレクトリに `__init__.py` ファイルを配置し、テストディレクトリをパッケージとして認識させる
- セットアップとティアダウンは `pytest` のフィクスチャを使用して依存関係を管理してクリーンなテスト環境を保つ
- `@pytest.mark.parametrize` を使用して同じテストを異なる入力で実行する
    - 例:
    ```python
    import pytest

    @pytest.mark.parametrize("a, b, expected", [
        (1, 2, 3),
        (2, 3, 5),
        (0, 0, 0)
    ])
    def test_addition(a, b, expected):
        assert a + b == expected
    ```

## AAA (Arrange, Act, Assert) パターン
- 単体テストはAAAパターンに従って記述する
    - Arrange: テストに必要な環境を設定し必要なデータを準備する
    - Act: テスト対象の関数やメソッドを実行する
    - Assert: コードの実行結果が期待通りであることを確認する

    - 例:
    ```python
    def test_addition_with_positive_numbers():
        # Arrange
        a = 1
        b = 2
        expected_result = 3

        # Act
        result = add(a, b)

        # Assert
        assert result == expected_result
    ```
- 過度に使いすぎない､再利用されない場合は直接テスト内に書く
## Fixture Factory
- 値を再利用するときはFixture Factoryを使用を使用してテストデータを作成する
- 例:
    ```python
    import pytest

    @pytest.fixture
    def user_factory():
        def create_user(username, email):
            return {"username": username, "email": email}
        return create_user

    def test_create_user(user_factory):
        user = user_factory("testuser", "test@example.com")
        assert user["username"] == "testuser"
    ```

## TDD (Test-Driven Development)
- 新しい機能を追加する前に、まずその機能のテストを記述する
- テストが失敗することを確認した後、機能の実装を行う
- 実装後、テストが成功することを確認する
- 既存の機能に変更を加える場合も、まずテストを記述し、変更後にテストが成功することを確認する
- テストは常に最新の状態を保つ
