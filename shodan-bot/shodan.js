
// client.on('message', (message) => {
//     if (message.channel.type == 'dm') {
//         if (message.author == client.user) return;
//         console.log(`-${message.author.username} says ${message}`);
//         message.reply("Leave this place, insect. Go pester a moderator instead.")
//     } return;

// });


// client.on('guildMemberAdd', member => {
//     const channel = member.guild.channels.find(channel => channel.name === 'cyberspace');
//     if (!channel) return;
//     channel.send(`Welcome back to the Nightdive Discord, ${member}, We hope your somnolent healing stage went well. Please be sure to refer to the <#373020882492456961> channel.`)
// });


// // Loops through list of banned words //
// client.on('message', async message => {
//     if (message.author.bot) return;
//     let foundInText = false;
//     for (var i in profanityArr) {
//         if (message.content.toLocaleLowerCase().includes(profanityArr[i].toLocaleLowerCase())) foundInText = true
//     }
//     if (foundInText) {
//         message.channel.send("***Watch your mouth, insect.***");
//     }
// });
// client.on('message', message => {
//     if (message.author.bot) return;
//     let found = false;
//     for (var i in politicalList) {
//         if (message.content.toLowerCase().includes(politicalList[i])) found = true
//     }
//     if (found) {
//         message.channel.send("***No politics, insect!***");
//     }
// });
// client.on('message', message => {
//     if (message.author.bot) return;
//     let found = false;
//     for (var i in politicalList) {
//         if (message.content.toLowerCase().includes(epic[i])) found = true
//     }
//     if (found) {
//         message.channel.send("***I tire of this topic, insect! Move along!***");
//     }
// });
// //  Shodan custom emoji ID  //
// const shoEmo = client.emojis.get("243598690344763394");

// client.on('message', message => { // Shoden bot responds with random quotes //
//     if (!message.content.startsWith(config.prefix) || message.author.bot) return;
//     if (message.content.startsWith(config.command)) {
//         message.channel.send("***" + shodenSaying[Math.floor(Math.random() * shodenSaying.length)] + "***");
//     };
//     //  Shodan reacts to !command with custom emoji  //
//     message.react("243598690344763394");
// });