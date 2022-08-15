# Thtagger

<img src="img/thtagger.png" height="64" width="64" alt="图标">

一个简单的，基于 Python3 、 PySide6 和 [Mutagen](https://github.com/quodlibet/mutagen) 的音乐元数据编辑器。

## 格式支持

1. MPEG-1 Audio Layer 3 (mp3)
2. Waveform Audio File Format (wav)
3. Free Lossless Audio Codec (flac)

## 特性

1. 支持从 THB Wiki 在线搜索元数据
2. wav 格式元数据在 Windows 资源管理器中可以被正常识别

## 使用 PySide2

由于许多 Linux 发行版并没有开始支持 Qt6 ，所以提供了转换成 PySide2 (Qt5) 代码的 patch ：

```shell
$ git apply doc/patches/to_pyside2.patch
```

## 安装

Python 3.6 及以上都是测试过支持的。

### PyPI

```shell
$ python -m pip install thtagger
$ python -m thtagger
```

### Debian stable

从 [github release](https://github.com/weilinfox/haku-thtagger/releases) 或 [gitee release](https://gitee.com/weilinfox/haku-thtagger/releases) 下载支持全架构的 deb 包安装：

```shell
$ sudo apt-get install ./thtagger_x.x.x_all.deb
```

### Archlinux

从 AUR 安装：

```shell
$ yay -S thtagger
```

### Windows

从 [github release](https://github.com/weilinfox/haku-thtagger/releases) 或 [gitee release](https://gitee.com/weilinfox/haku-thtagger/releases) 下载预打包的 x86 架构应用程序的 zip 包或单文件 exe ，支持 Windows7 及以上。zip 压缩包解压缩后运行 ``thtagger.exe`` 。

## 鸣谢

+ [Mutagen](https://github.com/quodlibet/mutagen) 是一切的基础
+ [Picard](https://github.com/metabrainz/picard) 提供了 wav 格式元数据保存的思路
+ [THB Wiki](https://thwiki.cc/) 提供了开放的 API

## 截图

![主界面](doc/screenshot/Screenshot_0.png)

## TODO

比较赶，写得很粗糙，只是可以实现基本功能。

+ 优化封面缓存
+ 命令行下的自动填写模式
+ 部分 mp3 依旧不识别为 wav 写入的 RIFF INFO 的问题
