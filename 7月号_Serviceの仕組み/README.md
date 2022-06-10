# Software Design Kubernetes Networkの補足リポジトリ

本リポジトリは 技術評論社が発行している雑誌SoftwareDesignの連載記事「スッキリわかるKubernetesネットワークの仕組み」を補足するためのリポジトリです。

minikubeを使ったKubernetesクラスタの環境構築およびサンプルアプリのビルドについて記載しています。

# Docker環境を構築

本連載のために利用したマシンは AWS の Ubuntu20.04 の EC2インスタンス です。

ただし、Ubuntu環境であればAWS以外の環境（GCPやローカル環境など）でも動くと思います。

スペックは以下です。

|     対象     |          スペック         |
| :----------: | ---------------------: |
|      OS     | Ubuntu Server 20.04 LTS |
|  アーキテクチャ | x86                     |
|      CPU    | 2 core                  |
|     メモリ    | 8GB                     |
|    ディスク   | 20GB                    |


上記スペックは、今回利用するminikubeの要件を満たすものになっています。詳細は公式ページ（※）をご確認ください。

※ https://minikube.sigs.k8s.io/docs/start/

マシンにアクセスしたらDockerをインストールしておきましょう。方法は公式ページ（※）を参照してください。

※ https://docs.docker.com/engine/install/ubuntu/

インストール後は、dockerコマンドをsudoなしで実行できるようにしておきます。

```sh
sudo gpasswd -a ubuntu docker
```

上記コマンドを実行後、マシンを再起動してください。

# minikubeをインストール

続いてminikubeを用いてKubernetesクラスタを構築します。

アーキテクチャやOSの違いによってインストール方法は異なるため、今回の検証環境ではない環境を利用している場合は公式ページ（※）を参照してください。

※ https://minikube.sigs.k8s.io/docs/start/

それではminikubeをインストールします。

```sh
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

# クラスタを構築

インストールが完了したらクラスタを構築します（といってもコマンド１つです）。

```sh
minikube start
```

完了には3分ほどかかります。

「Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default」という文言が出たらインストール完了です。

# エイリアスの設定

kubectlコマンドを使って状況を確認していく前に、minikubeの場合はコマンドが少し長くなるためエイリアスを設定しておきます。

```sh
alias kubectl="minikube kubectl --"
```

これでkubectlと入力するだけで使えるようになります。

# サンプルアプリのビルド

クラスタ内でコンテナとして稼働させるアプリをDockerイメージとして用意しておきます。

本README.mdと同階層に置いている `app.py` と `Dockerfile` を利用して、Dockerイメージをビルドできますが、その前にまずはDocker環境を切り替える必要があります。

minikubeは、Dockerをインストールした時に構築されるDocker環境（デフォルト環境）を利用せず、独自にDocker環境を構築し、そこにクラスタを作っています。そのクラスタにて自分で作成したコンテナイメージをPodとして起動するには、minikubeのDocker環境内にコンテナイメージを用意する必要があります。しかし、初期の設定のままdocker buildのコマンドを実行するとデフォルト環境にコンテナイメージが作成されてしまいます。そこでまずはminikubeのDocker環境に切り替える必要がある、ということです。

以下のコマンドで切り替えます。
```sh
eval $(minikube docker-env)
```

続いてコンテナイメージをビルドします。イメージ名は sample_api としています（※）。
```sh
docker build -t sample_api:1.0 ./
```

※ ここではイメージのバージョンをlastestとせずに数値で明示してください。latestの場合、Kubernetesがローカルイメージではなくリモートリポジトリを確認してしまい、エラーが発生します。

ビルドが完了したらdocker images コマンドで想定通りのイメージが作成されているか確認します。

最後にデフォルトのDocker環境に戻しておきます。
```sh
eval $(minikube docker-env -u)
```

これで、事前の環境構築は完了です。
