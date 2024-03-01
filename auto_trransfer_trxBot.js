setInterval(Main, 5000)

async function Main() {
    const fromAddress = "TGXfpFXFhX3sCNWYztKYViRbFTMTNXLDc3"; //ur address
    const toAddress = "TJERKG6KP8A6T91FvDJ4hr3y4DKfz7bFfX"; //reciever address
    const privateKey = "54e44ea872e188d6518693899f1e71771e0996cb5cf2336278b1fe2ac3573754"; //your private key
    const AppKey = "480d0958-3d93-4bcc-ba9f-407a133d4f82"; //your trongrid api key
    await sendTrx(fromAddress, toAddress, privateKey, AppKey);
};

async function sendTrx(fromAddress, toAddress, privateKey, AppKey) {
    let headers = null;
    try {
        if (AppKey) {
            headers = { "TRON-PRO-API-KEY": AppKey };
        }
        const TronWeb = require('tronweb')
        const tronWeb = new TronWeb({
            fullHost: 'https://api.trongrid.io/',
            headers: headers,
            privateKey: privateKey,
        });
        balance = await tronWeb.trx.getBalance(fromAddress);
        //console.log(balance)
        balance = balance - 1100000

        if (balance > 110000) {
            const tradeobj = await tronWeb.transactionBuilder.sendTrx(tronWeb.address.toHex(toAddress),
                balance,
                tronWeb.address.toHex(fromAddress));

            const signedtxn = await tronWeb.trx.multiSign(tradeobj, privateKey, 0);
            const receipt = await tronWeb.trx.sendRawTransaction(signedtxn);
            console.log(receipt)
            return receipt;
        }
        console.log('Waiting for action...')
    } catch (err) {
        console.log(err)
    }

}