# Thtagger

<img src="img/thtagger.jpg" height="64" width="64" alt="图标">

一个简单的，基于 Python3 、 PySide6 和 [Mutagen](https://github.com/quodlibet/mutagen) 的音乐元数据编辑器。

## 格式支持

1. MPEG-1 Audio Layer 3 (mp3)
2. Waveform Audio File Format (wav)
3. Free Lossless Audio Codec (flac)

## 特性

1. 支持从 THB Wiki 在线搜索元数据
2. wav 格式元数据在 Windows 资源管理器中可以被正常识别

## 使用 PySide2

由于 Qt6 在许多 Linux 发行版的支持并不好，所以同时提供了转换成 PySide2 （Qt5） 的 patch ：

```shell
$ git apply doc/patches/to_pyside2.patch
```

## 截图

![主界面](doc/screenshot/Screenshot_0.png)
