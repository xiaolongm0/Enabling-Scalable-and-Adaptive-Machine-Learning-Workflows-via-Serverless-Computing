import boto3
import base64
import json
import threading
import time
import math
import getlog
import sys

mylambda =  boto3.client('lambda')

def call_parallel_function(data, function_name, responses):

    invoke_response = mylambda.invoke(FunctionName=function_name,
                InvocationType = 'RequestResponse', LogType = 'Tail', 
                Payload=json.dumps(data))

    responses.append(json.loads(invoke_response['Payload'].read().decode()))
    return responses

def call_global_aggregator_function(data, function_name):
    
    invoke_response = mylambda.invoke(FunctionName=function_name,
                InvocationType = 'RequestResponse', LogType = 'Tail', 
                Payload=json.dumps(data))
    return json.loads(invoke_response['Payload'].read().decode())
    
def setup_function(input_data, function_name):
    output_data = []
    threads = []
    for i in range(len(input_data)):
        x = threading.Thread(target = call_parallel_function, args =(input_data[i], 
            function_name,output_data))
        threads.append(x)
        x.start()
    for thread in threads:
        thread.join()

    return output_data


def run_training(num_workers,mini_batch_size , my_epochs):
    batch_size = mini_batch_size
    total_workers = num_workers
    toal_shards = num_workers
    total_epochs = my_epochs
    total_mini_batches = int(math.ceil(50000/float(total_workers*batch_size)))
  
    
    begin = int(time.time()*1000)
    
    data = [{"delay": begin, "miniBatch_count":-1 ,"total_epochs": total_epochs,
        "epoch_count": 0,"total_mini_batches": total_mini_batches, "round_time": 0, 
        "total_clients": total_workers, "num_shards": toal_shards, "shard_aggregator_id": 0, "epoch_time":0,
        "batch_size":batch_size}]
    
    for i in range(total_epochs):
        print("Starting minibatch {} epoch {}".format(i%total_mini_batches, i//total_mini_batches))
        print("Invoking global aggregator")
        response = call_global_aggregator_function(data, 'Mxnet_train_global_aggregator')
        time.sleep(0)
        print("Invoking workers")
        data = setup_function(response["data"], "Mxnet_train")
        time.sleep(0)
        print("invoking shard aggregators")
        data = setup_function(data, "Mxnet_train_shard_aggregator")
        time.sleep(0)
        print("End minibatch {} epoch {}".format(i%total_mini_batches, i//total_mini_batches))
    print("Invoking global aggregator")
    print("End epoch Training")
    

if __name__ == '__main__':

    global_batch_size = int(sys.argv[1])
    user = int(sys.argv[2])
    my_epochs = int(sys.argv[3])
    mini_batch_size = global_batch_size//user
  
    print(mini_batch_size)
    run_training(user, mini_batch_size, my_epochs)
    getlog.collect_logs(user, global_batch_size)
    
    '''global_batch_sizes = [3200]#5000, 2000, 10000]
    users = [320]#, 25, 40, 100]#  
    for global_batch_size in global_batch_sizes:
        for user in users:

            print("Runnig Experiments with global_"\
                "batch_Size {} and users {}"
                .format(global_batch_size, user))

            mini_batch_size = global_batch_size//user
            if mini_batch_size > 32:
                mini_batch_size = 32
            #run_training(user, mini_batch_size)
            #getlog.collect_logs(user, global_batch_size)
    print("Done!!")'''
