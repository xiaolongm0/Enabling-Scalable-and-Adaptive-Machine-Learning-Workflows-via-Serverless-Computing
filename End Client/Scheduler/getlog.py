import boto3
import sys
import os
def org_get_cloudwatch_logs(my_log_group_name, workers, batch_size, folder_name):
    
    cloudwatch_logs = boto3.client('logs')
    log_groups = cloudwatch_logs.describe_log_groups( )
    myvalues = []

    log_streams = cloudwatch_logs.describe_log_streams(logGroupName='/aws/lambda/{}'.format(my_log_group_name), orderBy='LastEventTime',limit=50)
    my_logstreams = []
    print(len(log_streams['logStreams']))

    while(len(log_streams['logStreams']) > 0):
        for i in range (len(log_streams['logStreams'])):
            my_logstreams.append(log_streams['logStreams'][i]['logStreamName'])#
            stream_name = log_streams['logStreams'][i]['logStreamName']
            #print(stream_name)
            response = cloudwatch_logs.get_log_events(
		    logGroupName = '/aws/lambda/{}'.format(my_log_group_name),
		    logStreamName = stream_name
		    )
            for j in range (len(response['events'])):
                myvalues.append(response['events'][j]['message'])

        response = cloudwatch_logs.delete_log_stream(
            logGroupName='/aws/lambda/{}'.format(my_log_group_name),
            logStreamName= stream_name)

        log_streams = cloudwatch_logs.describe_log_streams(logGroupName='/aws/lambda/{}'
            .format(my_log_group_name), orderBy='LastEventTime',limit=50)	 
    #folder_name='./logs/workers_{}_batchsize_{}'.format(workers,batch_size)
    file_name = '{}/{}_workers_{}_batchsize_{}.log'.format(folder_name,
            my_log_group_name,workers,batch_size)

    with open(file_name, 'w') as f:
        for item in myvalues:
            my_item = item.encode('ascii', 'ignore')
            f.write("%s" % my_item)
            #f.write("%s" % item)

def get_cloudwatch_logs(my_log_group_name, workers, batch_size, folder_name):
    
    cloudwatch_logs = boto3.client('logs')
    log_groups = cloudwatch_logs.describe_log_groups( )
    myvalues = []

    log_streams = cloudwatch_logs.describe_log_streams(logGroupName='/aws/lambda/{}'.format(my_log_group_name), orderBy='LastEventTime',limit=50)
    my_logstreams = []
    print(len(log_streams['logStreams']))
    #folder_name='./logs/workers_{}_batchsize_{}'.format(workers,batch_size)
    file_name = '{}/{}_workers_{}_batchsize_{}.log'.format(folder_name,
            my_log_group_name,workers,batch_size)
    while(len(log_streams['logStreams']) > 0):
        for i in range (len(log_streams['logStreams'])):
            my_logstreams.append(log_streams['logStreams'][i]['logStreamName'])#
            stream_name = log_streams['logStreams'][i]['logStreamName']
            #print(stream_name)
            response = cloudwatch_logs.get_log_events(
		    logGroupName = '/aws/lambda/{}'.format(my_log_group_name),
		    logStreamName = stream_name
		    )
            for j in range (len(response['events'])):
                myvalues.append(response['events'][j]['message'])
        my_item = []
        response = cloudwatch_logs.delete_log_stream(
            logGroupName='/aws/lambda/{}'.format(my_log_group_name),
            logStreamName= stream_name)
        with open(file_name, 'a+') as f:
                for item in myvalues:
                    my_item = item.encode('ascii', 'ignore')
                    f.write("%s" % my_item)
        myvalues = []
        log_streams = cloudwatch_logs.describe_log_streams(logGroupName='/aws/lambda/{}'
            .format(my_log_group_name), orderBy='LastEventTime',limit=50)	 

def collect_memory_logs(num_workers, batch_size, memory):
    workers = num_workers
    folder_name = ('./logs/workers_{}_mem_{}_batchsize_{}'.format
                         (workers, memory,batch_size))
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    my_log_groups = ['Mxnet_train_global_aggregator', 'Mxnet_train', 'Mxnet_train_shard_aggregator']
    for my_log_group_name in my_log_groups:
        get_cloudwatch_logs(my_log_group_name, workers, batch_size, folder_name)

def collect_logs(num_workers, batch_size):
    workers = num_workers
    folder_name = ('./logs/workers_{}_batchsize_{}'.format
                         (workers,batch_size))
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    '''if not os.path.exists('./logs/workers_{}_batchsize_{}'.format
                         (workers,batch_size)):
        os.makedirs('./logs/workers_{}_batchsize_{}'.format(workers,
            batch_size))'''

    my_log_groups = ['Mxnet_train_global_aggregator', 'Mxnet_train', 'Mxnet_train_shard_aggregator']
    for my_log_group_name in my_log_groups:
        get_cloudwatch_logs(my_log_group_name, workers, batch_size, folder_name)


if __name__ =="__main__":
    print("This is main")
    workers = sys.argv[1]
    batch_size = sys.argv[2]
    memory = sys.argv[3]
    folder_name = ('./logs/workers_{}_mem_{}_batchsize_{}'.format
                         (workers, memory,batch_size))
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    '''if not os.path.exists('./logs/workers_{}_batchsize_{}'.format
                         (workers,batch_size)):
        os.makedirs('./logs/workers_{}_batchsize_{}'.format(workers,
            batch_size))'''
    my_log_groups = ['Mxnet_train_global_aggregator', 'Mxnet_train', 'Mxnet_train_shard_aggregator']#[]#
    for my_log_group_name in my_log_groups:
        get_cloudwatch_logs(my_log_group_name, workers, batch_size, folder_name)
