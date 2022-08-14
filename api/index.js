import 'dotenv/config';
import express from 'express';
import { MongoClient } from "mongodb";
import { Server } from "socket.io";
import fs from 'fs';

const app = express();
import http from 'http';

const client = new MongoClient(process.env.MONGO_CONN_URL);


const server = http.createServer(app);

const io = new Server(server, { cors: { origin: "*" } })


const logfile = "/var/log/oproxy_runner.log"
try {
    fs.watchFile(logfile,
        {
            persistent: true,
            interval: 200
        },
        (curr, prev) => {
            var emit = ""
            fs.readFile(logfile, 'utf-8', (err, data) => {
                if (err) throw err;
                let lines = data.trim().split("\n")
                var emit = (lines[lines.length - 1])
                io.emit('log', { line: emit });
                console.log("Emitted: ", emit)
            })
        }
    );
}
catch (e) {
    console.log(e);
}


app.get('/', (req, res) => {
    const host = req.headers.host
    const protocol = req.protocol
    const server_url = `${protocol}://${host}`
    try {
        return res.status(200).send(
            {
                "endpoints": {
                    "GET /": {
                        "description": "Returns a list of endpoints",
                        "url": `${server_url}/`,
                    },
                    "GET /servers": {
                        "description": "Returns the list of available servers",
                        "url": `${server_url}/servers`,
                    },
                }
            }
        );
    }
    catch (err) {
        return res.status(500).send({ error: true });
    }
});

app.get('/servers', async (req, res) => {
    try {
        const db = client.db("servers");
        const collection = await db.collection('servers').find({ available: true }).project({ _id: 0 }).toArray();
        return res.status(200).send(collection);
    }
    catch (err) {
        return res.status(500).send({ error: true });
    }
})

server.listen(process.env.PORT || 8080, () => {
    console.log('Server is running on port 8080');
})