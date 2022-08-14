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
    var last_read = []
    fs.watchFile(logfile,
        {
            persistent: true,
            interval: 200
        },
        (curr, prev) => {
            fs.readFile(logfile, 'utf-8', (err, data) => {
                const data_split = data.split("\n").slice(-10)
                data_split.forEach(line => {
                    if (!last_read.includes(line)) {
                        console.log("Emitted: ", line)
                    }
                })
                last_read = data.split("\n").slice(-10)
                if (last_read.length >= 100) {
                    last_read.slice(0, 50)
                }
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
                    "GET /countries": {
                        "description": "Returns the list of available countries",
                        "url": `${server_url}/countries`,
                    },
                    "GET /prototypes": {
                        "description": "Returns the list of available prototypes",
                        "url": `${server_url}/prototypes`,
                    },
                    "GET /donate": {
                        "description": "I need funds to keep this project alive in the cloud platform, help is appreciated!",
                        "url": `https://paypal.me/midhunnadh`,
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
    const { page, country, proto, query } = req.query
    try {
        const db = client.db("servers");
        console.log(query)
        const collection = await
            db.collection('servers')
                .find(
                    query ?
                        {
                            $text: { $search: query },
                        }
                        :
                        { available: true }
                )
                .project({ _id: 0 })
                .sort(query ? { url: -1 } : { streak: -1 })
                .filter(
                    {
                        ...(country ? { "data.country": country } : {}),
                        ...(proto ? { proto } : {})
                    }
                )
                .skip(10 * (page || 0))
                .limit(10)
                .toArray();
        const count = await db.collection('servers').countDocuments({ available: true })
        return res.status(200).send({
            alive_count: count,
            servers: collection
        });
    }
    catch (err) {
        return res.status(500).send({ error: true });
    }
})

app.get('/countries', async (req, res) => {
    try {
        const db = client.db("servers");
        const collection = await
            db.collection('servers')
                .aggregate([
                    {
                        $group: {
                            _id: "$id",
                            countries: { $addToSet: "$data.country" },
                        }
                    }
                ])
                .project({ _id: 0, countries: 1 })
                .toArray();
        return res.status(200).send(collection[0].countries.sort());
    }
    catch (err) {
        return res.status(500).send({ error: true, err });
    }
})

app.get('/prototypes', async (req, res) => {
    try {
        const db = client.db("servers");
        const collection = await
            db.collection('servers')
                .aggregate([
                    {
                        $group: {
                            _id: "$id",
                            proto: { $addToSet: "$proto" },
                        }
                    }
                ])
                .project({ _id: 0 })
                .toArray();
        return res.status(200).send(collection[0]["proto"].sort());
    }
    catch (err) {
        return res.status(500).send({ error: true, err });
    }
})

server.listen(process.env.PORT || 8080, () => {
    console.log('Server is running on port 8080');
})