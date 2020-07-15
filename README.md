# pypi-proxy

Pypi本地代理。当本地未找到时，从国内pypi镜像网站（目前使用豆瓣pypi镜像）拉取并缓存于本地，下次再访问时直接从本地获取。

## docker镜像制作

        sh build-docker.sh
        
## 拉起pypi-proxy服务

        docker-compose up
        
默认将7979端口映射到宿主机上进行监听，缓存包文件挂载在宿主机的~/mypypi。可以通过修改docker-compose.yml文件来改变映射至宿主机的端口号，以及缓存文件的挂载位置。


## 访问

假定pypi-proxy服务运行于域名/IP地址为<hostname>的主机的7979端口上，通过执行以下命令来安装<package>包：

        pip3 install -i http://<hostname>:7979/pypi/simple/ --trusted-host <hostname> <package-name>[==<版本号>] --timeout 1200
        
注：对于文件体积较大的包，建议在pip命令后面加上--timeout参数，将timeout设为一个比正常下载时间更大的值。
