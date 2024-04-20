#!/bin/bash


creat_function(){
aws lambda create-function \
 --function-name function_name \
 --zip-file fileb://test.zip \
 --handler lambda_function.lambda_handler --runtime python3.7 \
--role $aws_role
}


update_code(){
zip -g $packge_name file1.py file2.py
aws s3 cp simulation_global-aggregator.zip s3://mystep-function-packages
echo "https://mystep-function-packages/stepfunction-global-aggregator-bundle.zip"
aws lambda update-function-code --function-name $function_name --s3-bucket $bucket_name --s3-key $packge_name

}

function_name=$1 #'simulation_global-aggregator'
bucket_name=$2 #'my-s3-bucket'
packge_name=$3 #'simulation_global-aggregator.zip'
aws_role=$4 #'my_aws_role'
#echo $function_name
creat_function()
update_code()
