mkdir ./build
# remove previous build
rm ./build/daily_quiz_lambda.zip
# get dependency
poetry export -f requirements.txt --without-hashes > requirements.txt
pip install --platform manylinux2014_x86_64 --implementation cp --python-version 3.9 --only-binary=:all: --upgrade -r requirements.txt -t ./package
# zip package with source codes
cd ./package
zip -r ../build/daily_quiz_lambda.zip *
cd ..
zip -r ./build/daily_quiz_lambda.zip daily_quiz
# remove packages
rm -r ./package