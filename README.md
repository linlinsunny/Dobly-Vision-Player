使用 MPV 播放电脑上的杜比视界视频。
安装 MPV 
brew install MPV

使用下面的命令测试是否播放正常

mpv --vo=gpu-next doblyvision.mp4

现在原来奇怪的颜色就会变正常。虽然不是非常好。但是最起码能看了。

然后 python DoblyVisionPlayer.py 运行脚本
或者直接下载打包好的可执行文件。
只限于 macos
