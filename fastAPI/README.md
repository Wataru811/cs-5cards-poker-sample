# 環境

```dotnetcli
$ mkdir server
$ cd server
$ pyenv install 3.11.9
$ pyenv local 3.11.9
$ poetry init
$ poetry config virtualenvs.in-project true
$ poetry env use 3.11.9
```


https://zenn.dev/takuty/articles/b83c70c32820bb



## install

```dotnetcli
$ peotry update

```



# gRPC

まだテストしただけ。サンプルコードはreflection が入っているのでフラグ制御で消えるようにする事。

```
$ poetry add  grpcio grpcio-tools
$ cd ./api/
$ mkproto.sh   # compile pb
$ grpcTest.sh

```




