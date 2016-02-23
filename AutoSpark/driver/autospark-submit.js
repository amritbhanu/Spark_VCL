var prompt= require('prompt');
var exec = require('child_process').exec;
var sys = require('sys')
var fs = require('fs')

// Getting the file directory
BASE_DIR = __dirname
USER = BASE_DIR + "/../../user.txt"

// Starting a new prompt
prompt.start()

// Command Executors
function puts(error, stdout, stderr) { sys.puts(stdout) }

function command_executor(cmd) {

	console.log('Executing :' + cmd);
	var proc = exec(cmd, puts);
	proc.stdout.on('data', function(data) {
	console.log(data);
	});
}

console.log('#########################################');
console.log('##     Welcome to AutoSpark Job Submit   ##');
console.log('#########################################');
console.log('\n')
console.log('Enter provider: vcl');
console.log('\n')

prompt.get(['provider','spark_master_ip', 'spark_context_url', 'job_name_at_destination', 'data_file_name'], function (err, result) {
    
    //vcl
    provider = result.provider
    // just master ip
    spark_master_ip = result.spark_master_ip
    // spark url which is master ip and its connecting ports
    spark_context_url = result.spark_context_url
    // the running scala, or pyspark
    //just the spark python file
    job_name_at_destination = result.job_name_at_destination
    //data file on which it wants to work with
    data_file_name = result.data_file_name

    var user = fs.readFileSync(USER, 'utf-8').split('\n')[0];

    // Executing the spark job
    if (provider === 'vcl') {

        //console.log("Copying the program to the remote spark master...")
        //cmd = "scp " + spark_job_file_path + " "+user+"@" + spark_master_ip + ":/home/"+user+"/" + job_name_at_destination
        //command_executor(cmd)

        console.log("Running spark job on master...")
        cmd = "ssh "+user+ "@"+spark_master_ip + " 'sudo ~/spark/spark_latest/bin/spark-submit --class lda.lda /home/"+user+"/"+ job_name_at_destination + " --master " + spark_context_url + " " + data_file_name " " + spark_master_ip + " " + user+ "'"
        command_executor(cmd)

    }

    // Prompt ends here
    });
