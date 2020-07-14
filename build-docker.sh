rm -rf build
mkdir build
cp ./requirements.txt build
cp ./Dockerfile build
cp ./start.py build
cp -rf ./app build

docker image rm pypi-proxy:latest
docker build -t pypi-proxy ./build

rm -rf build
