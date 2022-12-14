import 'dotenv/config';
import express from 'express';
import { MongoClient } from "mongodb";
import { Server } from "socket.io";
import fs from 'fs';
import cors from 'cors';

const app = express();
app.use(cors());

import http from 'http';

const client = new MongoClient(process.env.MONGO_CONN_URL);


const server = http.createServer(app);

const io = new Server(server, { cors: { origin: "*" } })

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
                    "GET /protocols": {
                        "description": "Returns the list of available protocols",
                        "url": `${server_url}/protocols`,
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
    const { page, country, proto, query, sort, private_only } = req.query
    try {
        const db = client.db("servers");
        const collection = db.collection('servers')
        var db_res;

        var sort_by = {}
        sort_by[sort || "updated_at"] = -1

        if (query) {
            db_res = await
                collection
                    .find({ available: true, $text: { $search: query } })
                    .filter({ available: true })
                    .skip(10 * (page || 0))
                    .limit(10)
                    .project({ _id: 0 })
                    .toArray();
        }
        else {
            db_res = await
                collection
                    .find({ available: true })
                    .filter(
                        {
                            available: true,
                            ...(country ? { "data.country": country } : {}),
                            ...(proto ? { proto } : {}),
                            ...(private_only ? { private: true } : {})
                        }
                    )
                    .sort(sort_by)
                    .skip(10 * (page || 0))
                    .limit(10)
                    .project({ _id: 0 })
                    .toArray();
        }
        
        const count = await collection.countDocuments({ available: true })
        return res.status(200).send({
            alive_count: count,
            servers: db_res
        });
    }
    catch (err) {
        console.log(err)
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
                        $match: {
                            available: true
                        }
                    },
                    {
                        $group: {
                            _id: "$id",
                            countries: { $addToSet: "$data.country" },
                        }
                    }
                ])
                .project({ _id: 0, countries: 1 })
                .toArray();
        console.log(collection)
        return res.status(200).send(collection[0].countries.sort());
    }
    catch (err) {
        return res.status(500).send({ error: true, err });
    }
})

app.get('/protocols', async (req, res) => {
    try {
        const db = client.db("servers");
        const collection = await
            db.collection('servers')
                .aggregate([
                    {
                        $match: {
                            available: true
                        }
                    },
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


io.on("connect", (socket) => {
    var { auth } = socket.handshake;

    const user = auth[0];
    const token = auth[1];
    var authenticated = false;

    if (user === "log" && token === process.env.LOG_TOKEN) {
        authenticated = true;
    }

    socket.join("log");

    socket.on("send-log-line", ({ line }) => {
        if (authenticated) {
            console.log("Emitted: ", line);
            socket.broadcast.to("log").emit("receive-message", line);
        }
        else {
            print("Unauthorized")
        }
    });

});

server.listen(process.env.PORT || 8080, () => {
    console.log('Server is running on port 8080');
})