# 概要

筋トレの回数をAlexa経由でspreadsheetに記録していくためのAlexaスキル

基本的には[音声(Alexa)でSpreadsheetに赤ちゃんのトイレの時間を記録するまで - Qiita](https://qiita.com/waterada/items/ce430180c314ed73a9db)に準じているが、AWS Lambda関数の記述はPythonで行っている。

# 使い始めるまで

使用開始までには以下の手順で準備をする必要がある。

## GCPプロジェクトの作成

[Google Cloud Platform](https://console.cloud.google.com/)から新規にプロジェクトを作成する。

プロジェクト番号が後に必要となる。

次の手順でApp Script APIを有効化し、必要な情報を得る。

- 「APIとサービス > APIとサービスを有効化」から「App Script API」を検索して有効化する。
- 「APIとサービス > 認証情報 > 認証情報を作成 > OAuthクライアントID」とし、次の入力をする。
    - アプリケーションの種類：ウェブアプリケーション
    - 名前: 任意
    - 承認済みのJavaScript生成元: https://developers.google.com
    - 承認済みのリダイレクトURI: https://developers.google.com/oauthplayground


次の情報を控えておく。

- 認証情報中のクライアントIDとクライアントシークレット
- プロジェクトID（プロジェクトホームで確認）

## SpreadsheetとGoogle App Scriptの準備

### Spreadsheetの作成

任意のSpreadsheetを記録用として作成しておく。記録用のシートは`data`という名前にしておく。`data`シート内の左から3列に次の項目が記録されていくことになる。

- updated_at
- 回数
- 種別

### Google App Scriptの記述

ツール→スクリプトエディタからエディタを開き、次の関数を記述して保存する。

```
function appendRecords(data) {
  var number = data.query_result.number;
  var method = data.query_result.method;
  var mySheet = SpreadsheetApp.getActiveSheet();
  mySheet.appendRow([new Date(), number, method])
}
```

次の設定をしておく。

- 「リソース > Claud Platformプロジェクト」から先ほど作成したプロジェクトを指定（プロジェクトIDが必要）
- 「公開 > 実行可能APIとして導入」からAPIを公開する。
    - バージョン: 任意
    - スクリプトにアクセスできるユーザー: 自分のみ

次の情報を控えておく。

- 公開 > 実行可能APIとして導入
    - 現在のAPI ID
- ファイル > プロジェクトのプロパティ
    - プロジェクトキー（サポート終了）
    - スクリプトID

## トークンの発行

https://developers.google.com/oauthplayground にアクセス。

右上の設定ギアより

- Use your own OAuth credentialsをチェック
- GCPのAPIとサービスで控えたクライアントIDとクライアントシークレットを入力
- Step1（OAuthスコープの指定）
    - https://www.googleapis.com/auth/spreadsheets を入力
- Step2
    - Exchange authorization code for tokensをクリック
    - Refresh token及びAccess tokenを控えておく
- Step3
    - HTTP Method: POST
    - Request URL: https://script.googleapis.com/v1/scripts/{プロジェクトキー}:run
        - {プロジェクトキー}は先程控えたもの
    - Enter request body: 以下のJSONを入力
    - Send the requestをクリックしてSpreadsheetに行が追加されればOK

```
{
  "function": "appendRecords",
  "parameters": [{
    "query_result": {
      "number": "5",
      "method": "test"
    }
  }],
  "devMode": true
}
```

### Alexa skillの作成

TODO

### AWS Lambdaの設定

環境変数として以下のものを設定しておく必要がある。

- `ACCESS_TOKEN`
    - 「トークンの発行」で発行したアクセストークン（期限すぐ切れるので本当は不要かも）
- `REFRESH_TOKEN`
    - 「トークンの発行」で発行したリフレッシュトークン
- `CLIENT_ID`
    - GCPプロジェクトの認証情報にあるもの
- `CLIENT_SECRET`
    - GCPプロジェクトの認証情報にあるもの
- `SCRIPT_ID`
    - GASのもの