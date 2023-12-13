# remove previous build
rm build_lambda.zip
# get dependency
poetry export -f requirements.txt --without-hashes > requirements.txt
pip install --platform manylinux2014_x86_64 --implementation cp --python-version 3.9 --only-binary=:all: --upgrade -r requirements.txt -t ./package
# zip package with source codes
cd ./package
zip -r ../build_lambda.zip *
cd ..
zip -r ./build_lambda.zip src
# remove files
rm -r ./package