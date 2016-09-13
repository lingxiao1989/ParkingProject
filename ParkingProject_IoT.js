var PythonShell = require('python-shell');
var awsIot = require('aws-iot-device-sdk');

const thingShadow = awsIot.thingShadow;
const isUndefined = require('/home/pi/node_modules/aws-iot-device-sdk/common/lib/is-undefined');

mythingstate = {
  "state": {
    "reported": {
      "ip": "unknown"
    }
  }
}

function processTest( arguments ) {

	if (arguments.Mode===1){
		var options={
			args: ['--train']
		};
	}
	else{
		var options={
            args: ['--detect','/home/pi/Workspace/ParkMe/HaarCarsXML/parking-no-car.png']
        };

	}

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
	
	var loop = setInterval(function(){
		if (looptime===0){clearInterval(loop);}
		else{
		console.log('Starting new loop');
		looptime--;
		PythonShell.run('TopologyTraining.py',options, function(err,result){
			if (err) throw err;
			//camera.start();
			//setTimeout(function(){
				//camera.stop();
			//}, 10000);
			//if(Object.keys(result).length > 0){
			if(result!==null){
				console.log('results: %j', result);
				
				mythingstate = {
				"state": {
					"reported": {
						"carsDetected" : result
								}
						}
				};
				thingShadows.update('raspberry_pi',  mythingstate);
				thingShadows.publish('topic/carDetection', 'Someone is using your parking lot!');
			}
		})}
	}, 10000);
	
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
		console.log('received timeout for '+ clientToken)
    	});
    	return;
}




//module.exports = cmdLineProcess;



if (require.main === module) {
	processTest({Mode : 1, Circle : 5});
  /*cmdLineProcess('connect to the AWS IoT service and demonstrate thing shadow APIs, test modes 1-2',
                 process.argv.slice(2), processTest );*/
}
