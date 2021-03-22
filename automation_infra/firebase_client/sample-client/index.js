#!/usr/bin/env node

rl = require('serverline');

CmdClient = require('./cmd_client');

async function main(args) {
  args.shift(); // Discard node execPath
  args.shift(); // Discard script name
  const commandFile = args.shift();

  if (commandFile) {
    // Scripted
    fs.readFile(commandFile, (err, data) => {
      if (err) {
        console.log(`Problem reading command file: ${err}`);
        process.exit(1);
      }
      // const flow = JSON.parse(data);
      // const cmd_client = new CmdClient(flow.apiUrl);
      // for (const action of flow.actions) {
      //   cmd_client.run(action);
      // }
      console.log('Scripted mode not quite ready yet...')
    });
  } else {
    // Interactive
    rl.init();
    const finish = new Promise(resolve => {
      rl.question('Enter the base URL for the API [http://localhost:8080]: ',
                  answer => {
                    const apiUrl = answer.length === 0 && 'http://localhost:8080' || answer;
                    const cmd_client = new CmdClient(apiUrl);
                    cmd_lient.prompt(rl, resolve);
                  });
    });
    await finish;
    console.log("Client finished!");
  }
  process.exit(0);
}


/*
 * CLI Entry Point
 */
console.log("\n*****\nWelcome to the CoView Sample Client!");
main(process.argv)
