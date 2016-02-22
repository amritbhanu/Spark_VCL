var prompt= require('prompt');
var exec = require('child_process').exec;
var sys = require('sys')

// Changing directory to the script directory
try {

    // Getting the file directory
    base_dir = __dirname

    // Navigate to driver directory
    process.chdir(base_dir)
    console.log('Current directory: ' + process.cwd());

}
catch (err) {
    console.log('chdir: ' + err);
}

// Output for shell command execution
function puts(error, stdout, stderr) { sys.puts(stdout) }


function command_executor(cmd) {

	console.log('Executing :' + cmd);
	var proc = exec(cmd);
	proc.stdout.on('data', function(data) {
	console.log(data);
	});
}

// Starting a new prompt
prompt.start()


console.log('#########################################');
console.log('##     Welcome to AutoSpark Launcher   ##');
console.log('#########################################');
console.log('\n')
console.log('Enter provider: vcl');
console.log('\n')

prompt.get(['provider'], function (err, result) {

 	provider = result.provider
    if (provider != 'vcl' && provider != 'digitalocean') {
 		console.log('Incorrect provider selected. Exiting process');
 		process.exit(1);
 	}

    // Accept digital ocean and vcl tokens here
    if (provider === "digitalocean") {

            get_spark_cluster_params(provider)

    } else if (provider === "vcl") {

        get_spark_cluster_params(provider)
    }
});

function get_spark_cluster_params(provider) {


    // Accepting input size and name and ssh key pair
    console.log('\n')
    console.log('Cluster Name - User selected name for cluster identification');
    console.log('No of slaves to be in the cluster');
    console.log('Duration for each node reservation ');
    console.log('\n')

    prompt.get([ 'name', 'count', 'duration'], function (err, result) {

        name = result.name
	count= result.count
	duration=result.duration
	if (!count){
		count=1}
	if (!duration){
		duration=60}

        if( name && count && duration) {

            // Delete all file data
            //cmd = 'python truncate.py'
            //command_executor(cmd)


                if(provider === 'vcl') {
                    

                        cmd = 'python launch_vcl.py ' + name +' '+count+' '+duration;
                        command_executor(cmd)

                }

            
        }

    });
}
