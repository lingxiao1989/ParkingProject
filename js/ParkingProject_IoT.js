var PythonShell = require('python-shell');
var awsIot = require('aws-iot-device-sdk');
//var RaspiCam = require("raspicam");


const thingShadow = awsIot.thingShadow;
const isUndefined = require('/home/pi/node_modules/aws-iot-device-sdk/common/lib/is-undefined');

const temp_data='Topology_data.temp';
const topology_knowledge='Topology_knowledge.csv';
const loop_interval=1000;

mythingstate = {
	"SpotID":"unknown",
	"SpotAttribute":"unknown",
	"SpotState":"unknown"
}


function processTest(arguments) {
	var looptime=arguments.Circle;
	if (arguments.Mode===1){
		var options_runningMode={
			args: ['-c',arguments.clear_memory,'-o',temp_data]
		};
	}
	else{
		var options_runningMode={
            		args: ['-i',topology_knowledge]
        	};

	}
	var options_SpotSummarizing={
            args: ['-i',temp_data,'-o',topology_knowledge,'-k',arguments.K_Class]
        };

	var thingShadows = awsIot.thingShadow({
        keyPath: '/home/pi/Workspace/aws-iot/certs/322912f0ad-private.pem.key',
        certPath: '/home/pi/Workspace/aws-iot/certs/322912f0ad-certificate.pem.crt',
        caPath: '/home/pi/Workspace/aws-iot/certs/rootCA.pem',
        clientId: 'pi',
        region: 'us-west-2'
	});
	
	thingShadows.on('connect', function() {
		console.log('connected to things instance, registering thing name');
		thingShadows.register( 'raspberry_pi', { ignoreDeltas: true, persistentSubscribe: true } );
	});
	
	if (arguments.Mode===1){
		var loop = setInterval(function(){
			if (looptime===0){clearInterval(loop);}
			else{
				console.log('Starting new loop..');
				looptime--;
				PythonShell.run('TopologyTraining.py',options_runningMode, function(err,result){
					if (err) throw err;
				//console.log('Training is done');
				})
			}
		}, loop_interval);
		//console.log('Data is collected. Start Summarizing..');
		//PythonShell.run('SpotSummarizing_Clustering.py',options_SpotSummarizing, function(err,result){
			//if (err) throw err;
			//console.log('Summarizing done. Topogy training is done');
		//})
	}
	else{
		var loop = setInterval(function(){
			if (looptime===0){clearInterval(loop);}
			else{
				console.log('Starting new loop');
				looptime--;
				PythonShell.run('SpaceDetecting.py',options_runningMode, function(err,result){
					if (err) throw err;

					if(result!==null){
						console.log('results: %j', result);
						mythingstate = {
							"state": {
								"reported": {
									"SpotState" : result
									}
							}
						};
						console.log(mythingstate);
						//thingShadows.update('raspberry_pi',  mythingstate);
						//thingShadows.publish('topic/Announcement', 'Someone is using your parking lot!');
					}
				})
			}
		}, loop_interval);
	}

	
	thingShadows.on('close', function() {
		console.log('close');
		thingShadows.unregister( 'raspberry_pi' );
	});
	thingShadows.on('reconnect', function() {
    console.log('reconnect');
		thingShadows.register( 'raspberry_pi', { ignoreDeltas: true, persistentSubscribe: true } ); 
	});
	thingShadows.on('offline', function() {
		console.log('offline');
	});
	thingShadows.on('error', function(error) {
		console.log('error', error);
	});
	thingShadows.on('message', function(topic, payload) {
		console.log('message', topic, payload.toString());
	});
	
	thingShadows.on('status',  function(thingName, stat, clientToken, stateObject) {
       console.log('received '+stat+' on '+thingName+': '+
                   JSON.stringify(stateObject));
    });

	thingShadows.on('update',  function(thingName, stateObject) {
         console.log('received update '+' on '+thingName+': '+
                     JSON.stringify(stateObject));
    });

	thingShadows.on('delta',   function(thingName, stateObject) {
         console.log('received delta '+' on '+thingName+': '+
                     JSON.stringify(stateObject));
    });

	thingShadows.on('timeout',  function(thingName, clientToken) {
         console.log('received timeout for '+ clientToken);
    });
	
    return;
}




//module.exports = cmdLineProcess;



if (require.main === module) {
	//var interval = setInterval(processTest({Mode : 1}), 200);
	if(process.argv[2]==='--train'){
		processTest({Mode : 1, Circle : 40, clear_memory : 0});
	}
	if(process.argv[2]==='--detect'){
		processTest({Mode : 2, Circle : 2});
	}
//setInterval("processTest", 200);
	
  /*cmdLineProcess('connect to the AWS IoT service and demonstrate thing shadow APIs, test modes 1-2',
	process.argv.slice(2), processTest );*/
}
